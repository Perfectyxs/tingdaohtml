from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page = b.new_page(viewport={'width': 1280, 'height': 1100})
    page.goto('http://127.0.0.1:8768')
    page.evaluate('localStorage.clear()')
    page.reload()
    cards = page.locator('#screen-record button.topic-card')
    assert cards.count() == 2
    assert page.get_by_text('展开转写').count() == 0
    cards.nth(0).click()
    assert page.locator('#appOverlay').is_visible()
    assert '学位名额' in page.locator('#appOverlay').inner_text()
    page.locator('#appOverlay [data-action="close"]').first.click()
    cards.nth(1).click()
    assert '江景夜景' in page.locator('#appOverlay').inner_text()
    b.close()
print('both full topic cards open their own contents')
