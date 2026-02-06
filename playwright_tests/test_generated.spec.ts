import { test, expect } from '@playwright/test';

test('Generated test', async ({ page }) => {
    await page.goto('file:///ABSOLUTE_PATH/html_pages/sample.html');
    await expect(page.locator('#title')).toHaveText('Welcome Neha');
});
