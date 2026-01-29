import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChromeController:
    _instance = None
    driver = None

    @classmethod
    def get_driver(cls):
        if cls.driver is None:
            chrome_options = Options()
            # chrome_options.add_argument("--headless") # For invisible browsing
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_experimental_option("detach", True) # Keep open
            
            service = Service(ChromeDriverManager().install())
            cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        return cls.driver

    @classmethod
    def open_url(cls, url):
        try:
            if not url.startswith("http"):
                url = "https://" + url
            driver = cls.get_driver()
            driver.get(url)
            return f"Successfully opened {url}"
        except Exception as e:
            return f"Error opening URL: {e}"

    @classmethod
    def google_search(cls, query):
        try:
            driver = cls.get_driver()
            driver.get("https://www.google.com")
            
            # Wait for search box
            wait = WebDriverWait(driver, 10)
            search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
            
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            return f"Searched Google for: {query}"
        except Exception as e:
            return f"Error during search: {e}"

    @classmethod
    def interact(cls, action, target=None, value=None):
        """
        Generic interaction: click, type, scroll
        """
        try:
            driver = cls.get_driver()
            wait = WebDriverWait(driver, 10)
            
            # List of common ways to find an element
            find_methods = [
                (By.ID, target),
                (By.NAME, target),
                (By.CSS_SELECTOR, target),
                (By.XPATH, f"//*[contains(text(), '{target}')]"),
                (By.XPATH, f"//*[@placeholder='{target}']"),
                (By.XPATH, f"//*[@aria-label='{target}']"),
            ]

            element = None
            if action in ["click", "type"]:
                for method, selector in find_methods:
                    if not selector: continue
                    try:
                        if action == "click":
                            element = wait.until(EC.element_to_be_clickable((method, selector)))
                        else:
                            element = wait.until(EC.presence_of_element_located((method, selector)))
                        if element: break
                    except:
                        continue
            
            if action == "click":
                if element:
                    element.click()
                    return f"Successfully clicked {target}"
                return f"Could not find clickable element: {target}"

            elif action == "type":
                if element:
                    element.clear()
                    element.send_keys(value)
                    element.send_keys(Keys.RETURN)
                    return f"Typed '{value}' into {target}"
                else:
                    # Final fallback: Try to send keys to the active element
                    try:
                        active_element = driver.switch_to.active_element
                        active_element.send_keys(value)
                        active_element.send_keys(Keys.RETURN)
                        return f"Selector '{target}' failed, but I typed '{value}' into the currently focused field."
                    except:
                        return f"Could not find input field: {target}"
            
            elif action == "close":
                if cls.driver:
                    cls.driver.quit()
                    cls.driver = None
                return "Browser closed."
                
        except Exception as e:
            return f"Interaction Error: {e}"

def chrome_control(cmd, url=None, query=None, action=None, target=None, value=None):
    if cmd == "open":
        return ChromeController.open_url(url)
    elif cmd == "search":
        return ChromeController.google_search(query)
    elif cmd == "interact":
        return ChromeController.interact(action, target, value)
    elif cmd == "close":
        return ChromeController.interact("close")
    return "Unknown chrome command"
