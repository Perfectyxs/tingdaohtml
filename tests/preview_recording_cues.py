"""Check the HTML recording/cue order, period scope and actual click destinations."""
import hashlib,json,os
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/review-v1.4.2';OUT.mkdir(exist_ok=True)
checks=[];shots=[];errors=[]
def ok(name):checks.append({'check':name,'status':'passed'})
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1280,'height':1100},device_scale_factor=1)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(os.environ.get('PREVIEW_URL','http://127.0.0.1:8765'),wait_until='networkidle')
 page.evaluate('localStorage.clear()');page.reload(wait_until='networkidle')
 page.locator('[data-action="toggle-record"]').click()
 def mode(name):
  page.locator(f'#modeRow [data-mode="{name}"]').click()
  page.locator('#screen-record').evaluate('(e)=>e.scrollTop=0')
 def click(action,**attrs):
  selector=f'[data-action="{action}"]'+''.join(f'[data-{k}="{v}"]' for k,v in attrs.items())
  page.locator(selector).filter(visible=True).first.click()
  page.wait_for_timeout(280)
 def close():
  click('close')
  expect(page.locator('#appOverlay')).not_to_have_class(__import__('re').compile(r'\bopen\b'))
 def longshot(name):
  page.locator('#screen-record').evaluate('(e)=>e.scrollTop=0')
  height=page.evaluate("Math.max(844,document.querySelector('.overlay.open .sheet-body')?.scrollHeight+190||document.querySelector('#screen-record').scrollHeight+60)")
  style=page.add_style_tag(content=f'.device{{height:{height}px!important;min-height:{height}px!important;max-height:none!important}}.screen.active{{overflow:visible!important;height:auto!important;min-height:100%}}.overlay.open .sheet{{max-height:none!important;animation:none!important;transform:none!important}}.overlay.open .sheet-body{{overflow:visible!important;max-height:none!important;flex:none!important}}#toast,#undoBar{{visibility:hidden!important}}')
  page.locator('.device').screenshot(path=str(OUT/(name+'.png')),animations='disabled')
  box=page.locator('.device').bounding_box();style.evaluate('(e)=>e.remove()')
  shots.append({'file':name+'.png','kind':'完整 HTML 内容长图','width':round(box['width']),'height':round(box['height'])})
 def measure():
  return page.locator('#screen-record').evaluate('''e=>{const root=e.getBoundingClientRect();const hero=e.querySelector('.rec-hero').getBoundingClientRect();const cue=e.querySelector('.flow-cue')?.getBoundingClientRect();return {heroTop:hero.top-root.top+e.scrollTop,heroBottom:hero.bottom-root.top+e.scrollTop,cueTop:cue?cue.top-root.top+e.scrollTop:null}}''')
 mode('监听');baseline=measure();longshot('recording-monitor-reference')
 measurements={'监听':baseline}
 for name in ('计划','复盘'):
  mode(name);m=measure();measurements[name]=m
  assert abs(m['heroTop']-baseline['heroTop'])<.5 and m['cueTop']>=m['heroBottom']+11
  ok(name+'录音卡与监听同高，提词器位于录音卡下方')
  expect(page.locator('#flowCue [data-period="日"][data-action="cue-period"]')).to_have_attribute('aria-pressed','true')
  expect(page.locator('.flow-cue-title')).to_contain_text('日计划')
  assert page.locator('.flow-cue-item').count()==3
  longshot('recording-'+('plan' if name=='计划' else 'review')+'-day')
  before=page.locator('.rec-hero').inner_text()
  click('cue-period',mode=name,period='周')
  assert page.locator('.rec-hero').inner_text()==before
  expect(page.locator('.flow-cue-title')).to_contain_text('周计划')
  expect(page.locator('.flow-cue-context')).to_contain_text('完成招商玺楼栋分析')
  expect(page.locator('.flow-cue-context')).not_to_contain_text('带看世茂滨江')
  ok(name+'日周切换使用对应计划，录音状态和计时不变')
  longshot('recording-'+('plan' if name=='计划' else 'review')+'-week')
  click('cue-plans',period='周');expect(page.locator('#appOverlay .sheet-head h3')).to_contain_text('周计划')
  if name=='计划':longshot('cue-week-plans-open')
  close()
  click('cue-period',mode=name,period='日');click('cue-plans',period='日')
  expect(page.locator('#appOverlay .sheet-head h3')).to_contain_text('日计划')
  expect(page.locator('#appOverlay')).to_contain_text('带看世茂滨江，确认江哥需求')
  expect(page.locator('#appOverlay')).not_to_contain_text('完成招商玺楼栋分析')
  if name=='计划':longshot('cue-day-plans-open')
  close()
  ok(name+'日计划打开同日列表，周计划打开原有周计划锚')
  click('cue-step',mode=name,step='1')
  expect(page.locator('.flow-cue-hint')).to_contain_text('当前仍需接入服务')
  click('cue-period',mode=name,period='周')
  expect(page.locator('[data-action="cue-step"][data-step="1"]')).to_have_attribute('aria-current','step')
  click('cue-step',mode=name,step='0')
  ok(name+'流程步骤与提示可切换，日周切换保留当前步骤')
 mode('复盘');click('review-cue-history')
 expect(page.locator('#appOverlay')).to_contain_text('带看世茂滨江');close()
 ok('复盘保留回看当日录音入口')
 mode('计划');click('cue-period',mode='计划',period='日')
 mode('复盘');expect(page.locator('[data-action="cue-period"][data-period="周"]')).to_have_attribute('aria-pressed','true')
 mode('计划');expect(page.locator('[data-action="cue-period"][data-period="日"]')).to_have_attribute('aria-pressed','true')
 ok('计划与复盘分别保持自己的日周选择')
 original=page.evaluate('localStorage.getItem("tingdao-v13")')
 page.evaluate("const saved=JSON.parse(localStorage.getItem('tingdao-v13'));saved.data.tasks.forEach(t=>{if(t.period==='日')t.date='2026-10-20'});localStorage.setItem('tingdao-v13',JSON.stringify(saved))")
 page.reload(wait_until='networkidle');page.locator('[data-action="toggle-record"]').click();mode('计划')
 expect(page.locator('.flow-cue-context')).to_contain_text('还没有日计划')
 click('cue-plans',period='日');expect(page.locator('#appOverlay')).to_contain_text('当天还没有已确认待办');close()
 ok('无同日计划时显示空态，不串用其他日期')
 page.evaluate('(value)=>localStorage.setItem("tingdao-v13",value)',original)
 page.reload(wait_until='networkidle');page.locator('[data-action="toggle-record"]').click()
 for width in (320,390):
  page.set_viewport_size({'width':width,'height':844})
  for name in ('监听','计划','复盘'):
   mode(name);m=measure()
   if name=='监听':reference=m['heroTop']
   else:
    assert abs(m['heroTop']-reference)<.5
    for period in ('日','周'):
     click('cue-period',mode=name,period=period)
     assert page.locator('#flowCue').evaluate('(e)=>e.scrollWidth<=e.clientWidth+1')
  ok(str(width)+'px 窄屏录音卡对齐，提词器两页签无横向溢出')
 assert not errors,errors;ok('浏览器无 JavaScript 运行错误')
 result={'preview':'v1.4.2','html_sha256':hashlib.sha256((ROOT/'index.html').read_bytes()).hexdigest(),'checks':checks,'measurements':measurements,'screenshots':shots,'scope':'HTML 演示交互；未修改 APK，未执行麦克风/ASR/AI/声纹。','errors':errors}
 (OUT/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 browser.close()
print(json.dumps({'checks':len(checks),'screenshots':len(shots),'status':'passed'},ensure_ascii=False))
