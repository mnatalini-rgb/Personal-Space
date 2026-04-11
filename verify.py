import asyncio
from playwright.async_api import async_playwright
import json

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        
        await page.goto("http://localhost:8765/index.html")
        await page.wait_for_timeout(2000)
        
        await page.screenshot(path="tmp/index-verification.png", full_page=True)
        
        sidebar_exists = await page.locator(".sidebar").count() > 0
        nav_buttons = await page.locator(".sidebar-nav .nav-btn").count()
        
        result = {
            "sidebar_exists": sidebar_exists,
            "nav_buttons_count": nav_buttons,
            "errors": errors
        }
        
        print(json.dumps(result, indent=2))
        
        await browser.close()

asyncio.run(main())
