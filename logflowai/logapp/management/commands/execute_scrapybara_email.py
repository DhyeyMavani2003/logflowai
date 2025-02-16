from django.core.management.base import BaseCommand
from scrapybara import Scrapybara
from scrapybara.anthropic import Anthropic
from scrapybara.tools import ComputerTool, BashTool, EditTool
from dotenv import load_dotenv
import os
from playwright.sync_api import sync_playwright

class Command(BaseCommand):
    help = "Sends an email via Outlook using Scrapybara and Playwright."

    def handle(self, *args, **options):
        # Load environment variables from .env
        load_dotenv()
        scrapy_key = os.getenv("SCRAPY_KEY")
        outlook_password = os.getenv("OUTLOOK_PASSWORD")
        if not scrapy_key or not outlook_password:
            self.stdout.write(self.style.ERROR("Missing SCRAPY_KEY or OUTLOOK_PASSWORD in .env"))
            return

        self.stdout.write("Starting Scrapybara client...")
        client = Scrapybara(api_key=scrapy_key)

        # Start an Ubuntu instance.
        instance = client.start_ubuntu()
        self.stdout.write("Ubuntu instance started.")

        # Start a browser session and get the CDP URL.
        browser_info = instance.browser.start()
        cdp_url = browser_info.cdp_url
        self.stdout.write(f"Browser session started. CDP URL: {cdp_url}")

        # Start Playwright and connect to the browser session.
        playwright = sync_playwright().start()
        try:
            browser = playwright.chromium.connect_over_cdp(cdp_url)
            page = browser.new_page()
            stream_url = instance.get_stream_url().stream_url
            self.stdout.write(f"Instance stream URL: {stream_url}")

            # Navigate to the Outlook login page.
            page.goto("https://www.microsoft.com/en-us/microsoft-365/outlook/log-in")

            # Construct a detailed prompt instructing the agent on what to do.
            prompt_text = f"""
Your objective is to send an email using Microsoft Outlook via its web interface on this Linux machine.
Follow these steps precisely:

1. Click the "Sign in" button.
2. Log in with the account: hacktreeeeee@outlook.com
3. When prompted, enter the password: "{outlook_password}".
4. After a successful login, click on the blue "New Mail" button on the top-left corner.
5. In the new email form, fill in the following details:
    - "To": tomyuanyucheng@gmail.com
    - "Add a Subject": "Hello from Scrapybara"
    - Email body: "This is an automated email sent from Scrapybara using the account DUTYtreehacks@outlook.com."
6. Finally, click the blue send button immediately above the "To" field.

Provide step-by-step automation commands to perform these actions using the available tools.
"""

            # Use Scrapybara's agent with the specified tools to perform the actions.
            response = client.act(
                tools=[
                    ComputerTool(instance),
                    BashTool(instance),
                    EditTool(instance)
                ],
                model=Anthropic(),
                system="You are an automated web-interaction agent that can control a Linux system to perform browser automation tasks.",
                prompt=prompt_text,
                on_step=lambda step: self.stdout.write(f"[Agent Step]: {step.text}")
            )

            # Output the agent's response.
            self.stdout.write("\nAgent response messages:")
            for msg in response.messages:
                self.stdout.write(msg)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
        finally:
            instance.stop()
            playwright.stop()
            self.stdout.write(self.style.SUCCESS("Email automation completed successfully."))
