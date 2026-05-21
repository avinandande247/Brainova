import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        page.on("console", lambda msg: print(f"CONSOLE: {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"ERROR: {err}"))
        
        print("Navigating to https://brainova-beta.vercel.app/")
        await page.goto("https://brainova-beta.vercel.app/", wait_until="networkidle")
        
        await asyncio.sleep(5)  # Wait for React to crash
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
