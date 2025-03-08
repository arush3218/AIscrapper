import selenium.webdriver as webdriver
from bs4 import BeautifulSoup as BS
from selenium.webdriver.chrome.service import Service

def scrapee(website):
    print("Launching browser")
    
    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    
    try:
        driver.get(website)
        print("Page loaded..")
        html = driver.page_source
        
        return html
    finally:
        driver.quit()
        
def extractt(html_content):
    soup = BS(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def cleanup(body_content):
    soup = BS(body_content, "html.parser")
    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    # Extract text
    text = soup.get_text(separator="\n")
    
    # Process line by line
    lines = []
    for line in text.splitlines():
        if line.strip():
            # Split the line into words and rejoin with a single space
            words = line.split()
            clean_line = " ".join(words)
            lines.append(clean_line)
    
    # Join all lines with newlines
    result = "\n".join(lines)
    return result

def split_dom_content(body_content, max_length=6000):
    return [body_content[i:i+max_length] for i in range(0, len(body_content), max_length)]
