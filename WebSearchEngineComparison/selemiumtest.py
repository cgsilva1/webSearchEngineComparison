from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from urllib.parse import urlparse

def normalize_url(url):
    """
    Normalize URLs to handle the following:
    - Treat 'http' and 'https' schemes as the same.
    - Treat 'www' and non-www URLs as the same.
    - Remove trailing slashes at the end.
    """
    parsed_url = urlparse(url)

    # If scheme is http, change to https
    scheme = 'https' if parsed_url.scheme in ['http', 'https'] else parsed_url.scheme

    # Remove 'www' if present
    netloc = parsed_url.netloc.replace('www.', '')

    # Remove trailing slash from path
    path = parsed_url.path.rstrip('/')

    normalized_url = f"{scheme}://{netloc}{path}{parsed_url.query}"

    return normalized_url

def search_duckduckgo(query):
    # Initialize Safari WebDriver
    driver = webdriver.Safari()
    
    try: 
        driver.set_page_load_timeout(60)

        # Navigate to DuckDuckGo
        driver.get(f"https://duckduckgo.com/?q={query}")

        # Wait for the results to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "result__a")))
        
        # Scrape top 10 search result links
        # Use XPath to select non-ad links (avoid links inside sponsored sections)
        links = driver.find_elements(By.XPATH, "//a[contains(@class, 'result__a') and not(ancestor::*[contains(@class, 'ads')])]")
        results = []
        seen_urls = set()

        for link in links[:10]:
            href = link.get_attribute("href")
            if href:
                normalized_href = normalize_url(href)
                if normalized_href not in seen_urls:  # Avoid duplicates
                    seen_urls.add(normalized_href)
                    results.append(normalized_href)

    except Exception as e:
        print(f"Error with query '{query}': {e}")
        results = []

    finally:
        driver.quit()
    
    return results

def main():
    queries = [
        "A two dollar bill from 1953 is worth what",
        "What is franky jonas 's favorite color",
        "Is there an emergency action plan",
        "How much does medical insurance cost for a single person",
        "What is noah cyrus address so you can send her a fan mail",
        "Have many points did wayne getzky get",
        "How wide can vagina 's get",
        "Calories in a lollipop",
        "Pdf password cracker v 3.1 registration key",
        "Another name for karyokinesis",
        "What continent you indonesia on",
        "Do deers live in savanna",
        "What did lice cause in ww1",
        "What women invented the brush",
        "What is the order of electromagnetic radiation decreasing frequency",
        "New tropicana advert",
        "Where did siddartha Gautama live and teach",
        "2003 GMC yukon ignition",
        "What is the value of 1928 us 50 bill",
        "Where is alpha amylase released",
        "Which Band did Krauss join",
        "What is the use of fruits",
        "Where do sugar gliders like to live",
        "How many championships have lakers",
        "What are china major rivers and deserts",
        "What do dholes eat",
        "Stereo wiring diagram for a 1991 Toyota Camry",
        "Names of divine horses on howrse",
        "What is the population of teachers in the US",
        "How did Fidel V Ramos campaigned",
        "What are this 13 systems of human body",
        "What are the Flickertail 's eating habits",
        "What kind of money does croatia have",
        "What do our circulatory system includes",
        "A vaccination produces what kind of immunity",
        "Where does Justin Timbelake live",
        "Is corllins university a credited legal college",
        "What is a myocaridal infaraction",
        "When did bobsledding first enter",
        "500 mg of cinnamon equal how many teaspoons",
        "How many religions in spain",
        "How many lice did bob marly have",
        "What were the domsetic consequences of world war 1",
        "What is the meaning of multitasking and multiuser operating system",
        "The sun and the celestial bodies that orbit the sunincluding planets satellites asteroids comets dust and gas",
        "Tell you about vampire bats",
        "Specifying categories",
        "How much does a rookie card of babe ruth cost",
        "So what is fair trade",
        "What is the secret ingredient of coke",
        "When and how did Slobodan Milosevic die",
        "What do teardrop tattoos on your eyes symbolize",
        "What colors can a Yorkie be",
        "On neopets how can you put a code in a scroll box without the code being in the same box as another",
        "How much does it cost to rent a limo for the day in Madison WI",
        "Where is the 50 story eiffel tower located",
        "What is the length of an amtrak train",
        "Where to give ideas for an invention",
        "You are a big fan or shakira how you can send her a letter",
        "Code to beanie babies",
        "How much is s in roman numerals",
        "What is the origin of the mineral silver",
        "What is the principle behind the bluetooth",
        "What is transmission spectrum",
        "How many nutrons does radon have",
        "What color is rihanna eyes",
        "Who invented metal coil thermometer",
        "How did Rome really begin",
        "What part of california do corbin live in",
        "What is the instrument called that is used to measure tornado 's",
        "How does the future look on being a lawyer",
        "How do you adjust brightness on your laptop",
        "Whenwhere did william morris die",
        "How do sanction help to keep the global community safe and secure",
        "What is the function of command xargs in linux",
        "How does air pollution affect the food webs",
        "What was the name of the Prime Minister in Fiji in 2009",
        "What kind of meaning do proverbs have",
        "How many planet",
        "What is filters harmful substances from lymph",
        "How did park yong ha died",
        "How did people make dresses in colonial times",
        "How many liters are in a cup of milk",
        "How much does marijuana coast per ounce",
        "What is the purpose of a steak plate",
        "What is the name of the four sperm cells",
        "What is the longitudes of delhi",
        "How is columbia related to venezuela",
        "Fiona wood what is she famous for",
        "What sounds does brakes make",
        "What nationality are the people in germany",
        "What niche do plants have",
        "How many gold medals did mia hamm earn",
        "What did Roger Bannister",
        "How much does a medical abortion cost at three weeks",
        "What is rank 2nd in populated city",
        "What do mexicans houses look like",
        "64 millilitres how many litres",
        "You want to text dirty with your boyfriend what should you say",
        "Can you give me example of anecdotes by the filipino writers",
    ]
    
    results_dict = {}
    for i, query in enumerate(queries, start=1):
        result = search_duckduckgo(query)
        results_dict[f"Query{i}"] = result
        time.sleep(5)  # Avoid triggering bot detection

    # Write results to JSON file
    with open('hw1.json', 'w') as f:
        json.dump(results_dict, f, indent=4)

if __name__ == "__main__":
    main()
