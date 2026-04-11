import asyncio
from playwright.async_api import async_playwright
import json

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto("http://localhost:8765/index.html")
        await page.wait_for_timeout(1000)
        
        nav_buttons_html = await page.locator(".sidebar-nav .nav-btn").evaluate_all("elements => elements.map(e => e.innerHTML)")
        
        has_svg = all("<svg" in html for html in nav_buttons_html)
        
        print(json.dumps({
            "has_svg_in_all_buttons": has_svg,
            "nav_buttons_html": nav_buttons_html
        }, indent=2))
        
        await browser.close()

asyncio.run(main())
