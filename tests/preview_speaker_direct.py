from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=b.new_page(viewport={'width':1280,'height':1100})
    page.goto('http://127.0.0.1:8768');page.evaluate('localStorage.clear()');page.reload()
    page.locator('#screen-record button.topic-card').first.click()
    names=page.locator('#appOverlay [data-action="speaker-menu"]')
    original=names.nth(0).inner_text(); second=names.nth(1).inner_text()
    names.first.click();page.wait_for_timeout(300)
    assert page.locator('#appOverlay').get_attribute('data-sheet-key')=='speaker-correct'
    assert page.locator('#appOverlay .sheet').bounding_box()['height'] < page.locator('.device').bounding_box()['height']*.42
    select=page.locator('#speakerRole');other=select.locator('option').all_text_contents();target=next(x for x in other if x and x!=original and x!='不认识，归入陌生声纹')
    select.select_option(label=target);page.locator('[data-action="speaker-save"]').click()
    assert page.locator('#appOverlay').get_attribute('data-sheet-key')=='transcript'
    names=page.locator('#appOverlay [data-action="speaker-menu"]')
    assert names.nth(0).inner_text()==target and names.nth(1).inner_text()==second
    print('direct correction, short sheet, current sentence only and return: passed')
    b.close()
