from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1280, 'height': 1100})
    page.goto('http://127.0.0.1:8768')
    page.evaluate('localStorage.clear()')
    page.reload()
    page.locator('[data-nav="review"]').click()
    page.locator('[data-action="review-voice"]').click()
    page.locator('#appOverlay [data-action="session"]').first.click()
    page.locator('#appOverlay [data-action="mode-detail"]').click()
    page.wait_for_timeout(300)
    assert page.locator('#appOverlay').get_attribute('data-sheet-key') == 'mode-detail'
    assert page.locator('#appOverlay .sheet').bounding_box()['height'] < page.locator('.device').bounding_box()['height'] * .42
    assert page.locator('#appOverlay [data-action="mode-filter"]').is_visible()
    page.locator('#appOverlay [data-action="close"]').first.click()
    page.wait_for_timeout(300)
    assert page.locator('#appOverlay').get_attribute('data-sheet-key') == 'session'
    browser.close()
print('short mode sheet and return to recording detail passed')
