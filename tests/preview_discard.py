from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('/workspace/work/alpha11-audit/discard-html');out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1280,'height':1100});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8768');page.evaluate('localStorage.clear()');page.reload()
 page.locator('[data-action="discard"]').click();page.wait_for_timeout(300)
 info=page.evaluate('''()=>{let o=document.querySelector('#appOverlay'),s=o.querySelector('.sheet'),h=s.querySelector('.sheet-head'),body=s.querySelector('.sheet-body');return {key:o.dataset.sheetKey,height:s.getBoundingClientRect().height,device:document.querySelector('.device').getBoundingClientRect().height,body:body.getBoundingClientRect().height,last:body.lastElementChild.getBoundingClientRect().bottom,bottom:s.getBoundingClientRect().bottom}}''')
 assert info['key']=='discard-confirmation' and info['height']<info['device']*.42,info
 page.locator('.device').screenshot(path=str(out/'html-discard.png'),animations='disabled')
 page.locator('[data-action="close"]').filter(visible=True).first.click();page.wait_for_timeout(300)
 assert page.locator('#appOverlay.open').count()==0
 page.locator('[data-action="pool"]').first.click();page.wait_for_timeout(250)
 pool=page.locator('#appOverlay .sheet').bounding_box();assert pool['height']>=info['device']*.42-1
 assert not errors,errors
 print({'discard':info,'pool_height':pool['height'],'errors':errors});b.close()
