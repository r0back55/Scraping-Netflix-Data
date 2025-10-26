import requests
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def chrome_driver_setup():
    """Sets up the Chrome WebDriver."""
    driver_path = ChromeDriverManager().install()
    print(f"ChromeDriver installed at: {driver_path}")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")

    #Check if it is executable
    if not os.access(driver_path, os.X_OK):
        print("Not executable, changing permissions.")
        os.chmod(driver_path, 0o755)

        for root, dirs, files in os.walk(os.path.dirname(driver_path)):
            for dir in dirs:
                os.chmod(os.path.join(root, dir), 0o755)
            for file in files:
                os.chmod(os.path.join(root, file), 0o755)
                if "chromedriver" in file and not file.endswith(".chromedriver"):
                    potential_path = os.path.join(root, file)
                    print("Fund likely chromedriver at:", potential_path)
                    driver_path = potential_path
                    os.chmod(os.path.join(root, file), 0o755)
                    break
    
    return webdriver.Chrome(service=Service(driver_path), options=options)