import requests
import os
import time
import pandas as pd
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path


def chrome_driver():
    """Sets up the Chrome WebDriver."""
    driver_path = ChromeDriverManager().install()
    print(f"ChromeDriver installed at: {driver_path}")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    #Check if it is executable
    if not os.access(driver_path, os.X_OK):
        print("Not executable, changing permissions.")
        for root, dirs, files in os.walk(os.path.dirname(driver_path)):
            for file in files:
                if "chromedriver" in file and not file.endswith(".chromedriver"):
                    potential_path = os.path.join(root, file)
                    print("Fund likely chromedriver at:", potential_path)
                    driver_path = potential_path
                    break
    
    return webdriver.Chrome(service=ChromeService(driver_path), options=options)


# Test the requests library
url = "https://www.netflix.com/tudum/top10/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Encoding': 'identity'
}
r = requests.get(url, headers=headers) # Zmień tę linię
print("Status Code:", r.status_code)

driver = chrome_driver()
driver.get(url)


def extract_data(driver):
    """Extracts data from the Netflix Top 10 page."""
    movie_names = []
    views_list = []
    runtime_list = []
    time.sleep(5)  # Wait for the page to load

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    movies = soup.find_all('td', class_='title')
    for movie in movies:
        title = movie.get_text(strip=True)
        movie_names.append(title)

    views = soup.find_all('td', class_='views')
    for view in views:
        view_count = view.get_text(strip=True)
        views_list.append(view_count)

    runtimes = soup.find_all('td', class_='desktop-only', attrs={'data-uia': 'top10-table-row-hours'})
    for runtime in runtimes:
        time_long = runtime.get_text(strip=True)
        runtime_list.append(time_long)

    # Save as .csv using proper CSV writer
    print("Saving data to CSV file...")
    file_path = Path("D:/Programowanie/ETL_Pipelines/Scraping-Netflix-Data/netflix_top10.csv")
    
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Rank", "Movie Name", "Views", "Runtime"])
        for i in range(len(movie_names)):
            writer.writerow([i+1, movie_names[i][2:], views_list[i], runtime_list[i]])

    print("Data saved successfully.")


# Extract data and display the first 10 rows
extract_data(driver)
df = pd.read_csv("D:/Programowanie/ETL_Pipelines/Scraping-Netflix-Data/netflix_top10.csv")
print(df.head(10))


# Exit the driver
driver.quit()
