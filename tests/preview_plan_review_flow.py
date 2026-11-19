from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('docs/review-v1.4.3');out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1280,'height':1100});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 for mode in ('计划','复盘'):
  page.goto('http://127.0.0.1:8765/');page.evaluate('localStorage.clear()');page.reload()
  page.locator(f'#modeRow [data-mode="{mode}"]').click();page.locator('[data-action="finish-record"]').click();page.locator('[data-action="flow-demo"]').click();page.locator('.device').screenshot(path=str(out/(mode+'-整理.png')),animations='disabled');page.locator('[data-action="flow-pool"]').click();page.locator('.device').screenshot(path=str(out/(mode+'-确认.png')),animations='disabled')
  assert page.locator('#appOverlay').inner_text().count('示例 · '+mode+'录音')==2
  page.locator('[data-action="pool-approve"]').last.click();page.wait_for_timeout(300)
  data=page.evaluate('JSON.parse(localStorage.getItem("tingdao-v13")).data');assert any(t.get('sourceIds') for t in data['tasks']);assert not errors,errors
 print('plan and review: demo, pending confirmation and linked task passed');b.close()
