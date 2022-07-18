import test, { expect } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  await page.goto("https://dev-app1.upstage.live/demo");
})

test.describe('Demo Stage', () => {
  test('should have live status', async ({ page }) => {
    await new Promise(f => setTimeout(f, 3000));
    const status = await page.locator('.status-text').innerText();    
    await expect(status.toUpperCase()).toEqual('LIVE')
  })
})
