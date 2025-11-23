from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException, TimeoutException
from bs4 import BeautifulSoup as BS
from webdriver_manager.chrome import ChromeDriverManager
import os


def scrapee(website):
    print("Launching browser...")

    # Setup options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")

    try:
        # Use webdriver_manager to automatically get the correct driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(20)

        driver.get(website)
        print("Page loaded.")
        html = driver.page_source
        return html

    except TimeoutException:
        raise RuntimeError("⏰ Page load timed out. Try a simpler URL or check your connection.")

    except WebDriverException as e:
        raise RuntimeError(f"❌ WebDriver error occurred: {e}")

    except Exception as e:
        raise RuntimeError(f"❌ Unexpected error: {e}")

    finally:
        try:
            driver.quit()
        except:
            pass


def extractt(html_content):
    soup = BS(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def cleanup(body_content, keep_html=False):
    soup = BS(body_content, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()

    if keep_html:
        return str(soup)

    text = soup.get_text(separator="\n")
    lines = [" ".join(line.split()) for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def split_dom_content(body_content, max_length=6000):
    chunks = []
    current = ""
    for line in body_content.splitlines():
        if len(current) + len(line) + 1 > max_length:
            chunks.append(current)
            current = ""
        current += line + "\n"
    if current:
        chunks.append(current)
    return chunks
