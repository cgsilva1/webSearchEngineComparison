import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

# Function to normalize URLs and remove the #:~:text= part
def normalize_url(url):
    parsed_url = urlparse(url)
    scheme = 'https' if parsed_url.scheme in ['http', 'https'] else parsed_url.scheme
    netloc = parsed_url.netloc.replace('www.', '')
    path = parsed_url.path.rstrip('/')
    if "#:~:text=" in url:
        url = url.split("#:~:text=")[0]
    normalized_url = f"{scheme}://{netloc}{path}"
    if parsed_url.query:
        normalized_url += f"?{parsed_url.query}"
    return normalized_url

# Function to search Bing and scrape results
def search_bing(query):
    driver = webdriver.Safari()
    driver.get(f"https://www.bing.com/search?q={query}&count=30")

    try:
        # Wait for the search results to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "b_algo"))
        )
        
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Wait for more results to load if applicable

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Break the loop if no new content is loaded
            last_height = new_height

        # Now scrape the first 30 search result links
        links = driver.find_elements(By.CLASS_NAME, "b_algo")
        results = []
        for link in links[:10]:
            try:
                anchor = link.find_element(By.TAG_NAME, "a")
                href = anchor.get_attribute('href')
                if href:
                    normalized_href = normalize_url(href)
                    results.append(normalized_href)
            except Exception as e:
                print(f"Error processing link: {e}")
        return results

    except Exception as e:
        print(f"Error fetching results for query '{query}': {e}")
        # Optional: You can log the page source or HTML content to understand what went wrong
        with open(f"error_page_{i}.html", "w") as error_file:
            error_file.write(driver.page_source)


    finally:
        driver.quit()


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
        print(f"{i}")
        result = search_bing(query)
        results_dict[f"{query}"] = result
        time.sleep(5)  # To avoid rate limits

    with open('hw1.json', 'w') as json_file:
        json.dump(results_dict, json_file, indent=4)

    print("Normalized results written to hw1.json")

if __name__ == "__main__":
    main()
