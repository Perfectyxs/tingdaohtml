"""Browser checks for the review prototype; no ASR/speaker model is tested here.

Serve the repository, then run PREVIEW_URL=http://127.0.0.1:8765 python3 tests/preview_v14.py.
Uses system Chromium and the environment's Playwright installation.
"""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/review-v1.4'
SHOTS = OUT / 'screenshots'
SHOTS.mkdir(parents=True, exist_ok=True)
results = []
screenshots = []

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'), headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1280, 'height': 1100}, device_scale_factor=1)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda err: errors.append(str(err)))
    url = os.environ.get('PREVIEW_URL', 'http://127.0.0.1:8765')

    def fresh():
        page.goto(url, wait_until='networkidle')
        page.evaluate('localStorage.clear()')
        page.reload(wait_until='networkidle')

    def click(action, **data):
        selector = f'[data-action="{action}"]' + ''.join(f'[data-{key}="{value}"]' for key, value in data.items())
        page.locator(selector).filter(visible=True).first.click()
        page.wait_for_timeout(270)

    def nav(name):
        page.locator(f'[data-nav="{name}"]').click()
        page.wait_for_timeout(60)

    def state():
        return page.evaluate('JSON.parse(localStorage.getItem("tingdao-v13")).data')

    def ok(name):
        results.append({'check': name, 'status': 'passed'})

    def capture(name):
        # Expand the actual scroll container for a complete long screenshot.
        page.wait_for_timeout(280)
        height = page.evaluate('''() => {
          const sheet=document.querySelector('.overlay.open .sheet');
          const screen=document.querySelector('.screen.active');
          return Math.max(840, sheet ? sheet.querySelector('.sheet-body').scrollHeight+190 : screen.scrollHeight+60);
        }''')
        style = page.add_style_tag(content=f'''
          .device{{height:{height}px!important;min-height:{height}px!important;max-height:none!important}}
          .screen.active{{overflow:visible!important;height:auto!important;min-height:100%}}
          .overlay.open .sheet{{max-height:none!important;overflow:visible!important;animation:none!important;transform:none!important}}
          .overlay.open .sheet-body{{overflow:visible!important;flex:none!important;max-height:none!important}}
          #toast,#undoBar{{visibility:hidden!important}}
        ''')
        page.locator('.device').screenshot(path=str(SHOTS / (name + '.png')), animations='disabled')
        dimensions = page.locator('.device').bounding_box()
        style.evaluate('(e)=>e.remove()')
        screenshots.append({'file': 'screenshots/' + name + '.png', 'height': round(dimensions['height'])})

    fresh()
    assert page.title().endswith('v1.4')
    ok('Initial render has the v1.4 title and no JavaScript error')
    capture('01-recording-full')
    click('lexicon-session')
    capture('01-01-session-lexicons')
    page.locator('[data-lex-session="finance"]').check()
    click('lexicon-use-session')
    click('toggle-record')
    click('finish-record')
    assert len(state()['sessions'][0]['lexiconSnapshot']['packs']) == 3
    ok('A session override is frozen into the saved recording snapshot')
    nav('history')
    capture('02-history-recordings')
    page.locator('[data-history-tab="复盘"]').click()
    capture('02-01-daily-reviews')
    assert page.locator('#screen-history [data-action="daily-review"]').count() == 1
    click('daily-review')
    capture('02-01-01-daily-review-detail')
    assert page.locator('#appOverlay [data-action="session"]').count() == 2
    click('close')
    click('review-kind', value='复盘录音')
    capture('02-02-review-recordings')
    expect(page.locator('#screen-history')).to_contain_text('每日复盘 · 10月15日')
    click('review-kind', value='计划记录')
    capture('02-03-planning-recordings')
    expect(page.locator('#screen-history')).to_contain_text('明日带看准备计划')
    page.locator('[data-history-tab="经验卡"]').click()
    capture('02-04-experience-cards')
    expect(page.locator('#screen-history')).to_contain_text('手动整理')
    ok('History separates daily reports, review recordings, planning recordings and experience cards')
    nav('review')
    capture('03-review-full')
    assert '经验候选' not in page.locator('#screen-review').inner_text()
    assert '已确认经验卡' not in page.locator('#screen-review').inner_text()
    ok('Review no longer duplicates the experience-card module')
    nav('settings')
    capture('04-settings-full')
    expect(page.locator('#screen-settings')).to_contain_text('复盘与角色')
    click('hotwords')
    capture('04-01-lexicon-library')
    page.locator('[data-lex-pack="finance"]').check()
    click('lexicon-pack', id='finance')
    capture('04-01-01-professional-pack')
    click('lexicon-term', id='fx1')
    capture('04-01-01-01-term-editor')
    page.locator('#lexNotes').fill('测试备注：只维护术语，不强行扩写简称。')
    click('lexicon-save-term')
    assert next(p for p in state()['settings']['lexiconPacks'] if p['id']=='finance')['revision'] == 2
    ok('Pack selection, term editing and revision persistence work independently')
    click('close')
    expect(page.locator('#appOverlay')).to_contain_text('金融专业')
    assert page.locator('[data-lex-pack="finance"]').is_checked()
    ok('Returning from a pack refreshes the library and preserves selected packs')
    page.reload(wait_until='networkidle')
    nav('settings'); click('hotwords'); click('lexicon-new')
    page.locator('#lexName').fill('测试专业');page.locator('#lexDomain').fill('测试领域')
    click('lexicon-save-pack')
    capture('04-01-02-new-pack-empty')
    assert any(p['name']=='测试专业' for p in state()['settings']['lexiconPacks'])
    ok('Creating an empty professional pack persists it without invented terms')
    fresh();nav('roles')
    capture('05-roles-full')
    click('new-role')
    capture('05-01-create-role-paths')
    assert page.locator('#appOverlay .entry-choice').count() == 3
    click('role-name')
    capture('05-01-01-name-enrollment')
    page.locator('#newRoleName').fill('历史认领测试')
    click('role-create-next')
    capture('05-01-01-01-pending-voice')
    expect(page.locator('#appOverlay')).to_contain_text('尚无声纹样本')
    assert not state()['roles'][-1]['autoMatch']
    click('role-history-match')
    capture('05-01-01-02-history-enrollment')
    page.locator('[data-history-voice="v1"]').check()
    page.locator('[data-history-voice="v2"]').check()
    click('role-history-confirm')
    role=state()['roles'][-1]
    assert role['voiceIds'] == ['v1','v2'] and role['autoMatch']
    ok('Name-only creation needs explicit historical enrollment before automatic matching')
    click('voices');click('voice-match-run')
    capture('05-02-04-known-role-matching')
    expect(page.locator('#appOverlay')).to_contain_text('示例规则通过')
    click('voice-match-apply')
    data=state()
    assert {v['id'] for v in data['voices']} == {'v4','v5'}
    assert data['roles'][-1]['voiceIds'] == ['v1','v2']
    ok('Fixture matching assigns only the qualifying voice without training its result back into the template')
    fresh();nav('roles');click('new-role');click('role-sample')
    page.locator('#newRoleName').fill('主动采样测试')
    click('role-create-next')
    capture('05-01-02-sample-enrollment')
    page.clock.install();click('sample-start');page.clock.run_for(8500)
    expect(page.locator('#appOverlay')).to_contain_text('确认声纹样本')
    capture('05-01-02-01-sample-confirmation')
    click('sample-save')
    assert state()['roles'][-1]['autoMatch']
    ok('Explicit sample demonstration proceeds from recording to confirmation and role creation')
    fresh();nav('roles');click('voices')
    capture('05-02-manual-voice-pool')
    page.locator('[data-voice="v1"]').check();page.locator('[data-voice="v2"]').check()
    click('voice-merge')
    capture('05-02-01-synthesize-new-person')
    page.locator('#revealName').fill('保留草稿')
    click('merge-existing')
    capture('05-02-02-merge-existing-person')
    click('merge-new')
    assert page.locator('#revealName').input_value() == '保留草稿'
    click('merge-existing');page.locator('#mergeRole').select_option('r1');click('voice-assign')
    data=state()
    assert {v['id'] for v in data['voices']} == {'v3','v4','v5'}
    assert data['voiceAssignments'][-1]['roleId']=='r1'
    assert next(q for q in data['quotes'] if q['id']=='q4')['role']=='r1'
    ok('Manual merging preserves the name draft, assigns only selected evidence and updates linked quotes')
    page.locator('#undoButton').click()
    assert len(state()['voices']) == 5
    ok('Undo restores voice evidence and quote ownership after a merge')
    fresh();nav('roles');click('voices');page.locator('#voiceAutoGroup').check();click('voice-automatic')
    capture('05-02-03-automatic-clusters')
    assert page.locator('#appOverlay .cluster-card').count() == 2
    click('voice-cluster-split')
    assert page.locator('#appOverlay .cluster-card').count() == 4
    page.reload(wait_until='networkidle');nav('roles');click('voices');click('voice-automatic')
    assert page.locator('#appOverlay .cluster-card').count() == 4
    ok('Automatic clusters can be split and the do-not-merge constraints survive reload')
    # A-B and B-C similarity alone must not bridge incompatible A-C evidence.
    fresh()
    data=state();data['voiceExcludedPairs']=['v1:v3']
    page.evaluate('(d)=>localStorage.setItem("tingdao-v13",JSON.stringify({schema:13,data:d}))',data)
    page.reload(wait_until='networkidle');nav('roles');click('voices');click('voice-automatic')
    groups=page.locator('#appOverlay .cluster-card').all_text_contents()
    assert not any('我上一个顾问话太多' in g and '先看看，别推急售' in g for g in groups)
    ok('A conflict constraint prevents a similarity chain from merging incompatible evidence')
    # Small layouts must stay within the actual phone width.
    for width in (320,390,768):
        page.set_viewport_size({'width':width,'height':950})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
    ok('The page fits 320, 390 and 768 pixel viewports')
    assert not errors, errors
    ok('All covered browser paths finish without uncaught JavaScript errors')
    browser.close()

(OUT/'checks.json').write_text(json.dumps({'scope':'HTML prototype only; fixture similarities, no model/Android validation','results':results,'screenshots':screenshots},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':len(results),'screenshots':len(screenshots),'uncaught_errors':errors},ensure_ascii=False))
