import test, { expect } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  await page.goto("https://dev-app1.upstage.live/demo");
  await new Promise(f => setTimeout(f, 3000));
})

test.describe('Demo Stage', () => {
  test('should have live status', async ({ page }) => {
    const status = await page.locator('.status-text').innerText();    
    await expect(status.toUpperCase()).toEqual('LIVE')
  })
})
