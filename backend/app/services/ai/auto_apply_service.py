import asyncio
import logging
from playwright.async_api import async_playwright
from playwright_stealth import stealth

logger = logging.getLogger(__name__)

class AutoApplyService:
    @staticmethod
    async def apply_to_job(
        job_url: str,
        user_info: dict,
        resume_path: str | None = None,
        cover_letter_text: str | None = None,
    ) -> bool:
        """
        Attempts to automatically submit a job application.
        Focuses on standard ATS systems like Greenhouse and Lever.
        Skips blocked domains (LinkedIn, Indeed, Handshake).
        """
        blocked_domains = ["linkedin.com", "indeed.com", "joinhandshake.com", "workday.com"]
        
        if any(domain in job_url.lower() for domain in blocked_domains):
            logger.info(f"Skipping auto-apply for blocked domain: {job_url}")
            return False
            
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                await stealth(page)
                
                logger.info(f"Navigating to {job_url}")
                await page.goto(job_url, timeout=30000)
                await page.wait_for_load_state("domcontentloaded")
                
                # Check for Greenhouse
                if "greenhouse.io" in page.url or await page.locator("div#app_body").count() > 0:
                    success = await AutoApplyService._apply_greenhouse(page, user_info, resume_path, cover_letter_text)
                    await browser.close()
                    return success
                
                # Check for Lever
                if "jobs.lever.co" in page.url:
                    success = await AutoApplyService._apply_lever(page, user_info, resume_path, cover_letter_text)
                    await browser.close()
                    return success
                
                logger.warning(f"Unsupported ATS or custom portal for URL: {job_url}")
                await browser.close()
                return False
                
        except Exception as e:
            logger.error(f"Auto-apply failed for {job_url}: {str(e)}")
            return False
            
    @staticmethod
    async def _apply_greenhouse(page, user_info, resume_path, cover_letter_text):
        try:
            logger.info("Applying via Greenhouse pattern...")
            # First name
            if await page.locator("input#first_name").count() > 0:
                await page.fill("input#first_name", user_info.get("first_name", "Test"))
            
            # Last name
            if await page.locator("input#last_name").count() > 0:
                await page.fill("input#last_name", user_info.get("last_name", "User"))
                
            # Email
            if await page.locator("input#email").count() > 0:
                await page.fill("input#email", user_info.get("email", "test@example.com"))
                
            # Phone
            if await page.locator("input#phone").count() > 0:
                await page.fill("input#phone", user_info.get("phone", "1234567890"))
                
            # Resume Upload
            if resume_path and await page.locator("input[type='file'][name='job_application[answers_attributes][0][attachment]']").count() > 0:
                await page.set_input_files("input[type='file'][name='job_application[answers_attributes][0][attachment]']", resume_path)
            elif resume_path and await page.locator("input[type='file']").count() > 0:
                 await page.set_input_files("input[type='file']", resume_path)

            # Submit
            # await page.click("button#submit_app") 
            # We don't click submit in development to avoid spamming companies!
            logger.info("Greenhouse form filled successfully! (Submit prevented for safety)")
            return True
            
        except Exception as e:
            logger.error(f"Greenhouse apply failed: {e}")
            return False

    @staticmethod
    async def _apply_lever(page, user_info, resume_path, cover_letter_text):
        try:
            logger.info("Applying via Lever pattern...")
            
            # Check if we need to click "Apply for this job" first
            apply_btn = page.locator("a.postings-btn.template-btn-submit.venn-info")
            if await apply_btn.count() > 0:
                await apply_btn.first.click()
                await page.wait_for_load_state("domcontentloaded")
            
            # Full name
            if await page.locator("input[name='name']").count() > 0:
                await page.fill("input[name='name']", f"{user_info.get('first_name', 'Test')} {user_info.get('last_name', 'User')}")
                
            # Email
            if await page.locator("input[name='email']").count() > 0:
                await page.fill("input[name='email']", user_info.get("email", "test@example.com"))
                
            # Phone
            if await page.locator("input[name='phone']").count() > 0:
                await page.fill("input[name='phone']", user_info.get("phone", "1234567890"))
                
            # Resume Upload
            if resume_path and await page.locator("input[type='file'][name='resume']").count() > 0:
                await page.set_input_files("input[type='file'][name='resume']", resume_path)

            logger.info("Lever form filled successfully! (Submit prevented for safety)")
            return True
            
        except Exception as e:
            logger.error(f"Lever apply failed: {e}")
            return False
