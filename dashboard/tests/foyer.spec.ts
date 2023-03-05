import test, { expect } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  await page.goto("https://dev-app1.upstage.live");
  await new Promise((f) => setTimeout(f, 3000));
});

test.describe("Foyer", () => {
  test("should show logo", async ({ page }) => {
    const navbrand = page.locator(".navbar-brand");
    const logo = navbrand.locator("img");
    await expect(logo).toBeVisible();
  });

  test("should has stages in masonry grid", async ({ page }) => {
    const container = page.locator(".stages");
    await expect(container.locator("> div")).toHaveClass("masonry-wall");
  });

  test("should show some stages", async ({ page }) => {
    const container = await page.locator(".stages");
    await expect(container).toBeVisible();
    expect(await container.locator("img").count()).toBeGreaterThan(0);
  });

  test("should have demo stage", async ({ page }) => {
    const container = await page.locator(".stages");
    expect(await (await container.allTextContents()).join()).toContain("Demo");
  });
});
