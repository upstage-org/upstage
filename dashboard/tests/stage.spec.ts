import test, { expect } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  await page.goto("https://dev-app1.upstage.live/demo");
  await new Promise((f) => setTimeout(f, 3000));
});

test.describe("Demo Stage", () => {
  test("should have live status", async ({ page }) => {
    let waitCondition = true;
    let status;
    let waitCount = 3;

    while (waitCondition) {
      await new Promise((f) => setTimeout(f, 1100));
      status = await page.locator(".status-text").innerText();
      waitCondition = status.toUpperCase() != "LIVE";
      waitCount = waitCount - 1;

      if (waitCount == 0) {
        break;
      }
    }
    await expect(status.toUpperCase()).toEqual("LIVE");
  });
});
