from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import yaml
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import unicodedata

artists_data = pd.DataFrame()
artists, artists_fame, unavailable_artists = [], [], []
unique_artists = {}
driver = None


def clean_string(text):
    nfkd_string = unicodedata.normalize("NFKD", str(text))
    text = "".join([c for c in nfkd_string if not unicodedata.combining(c)])
    return text


def cosine_sim_vectors(v1, v2):
    v1 = v1.reshape(1, -1)
    v2 = v2.reshape(1, -1)
    return cosine_similarity(v1, v2)[0][0]


def name_similarity(text1, text2):
    text1 = clean_string(text1)
    text2 = clean_string(text2)
    vector = CountVectorizer().fit_transform([text1, text2])
    return cosine_sim_vectors(vector[0], vector[1])


def start_driver():
    browser_mat = {"name": ["chrome", "firefox", "microsoft edge"],
                   "threshold": [0.6, 0.6, 0.4],
                   "driver": [webdriver.Chrome, webdriver.Firefox, webdriver.Edge],
                   "service": [ChromeService, FirefoxService, EdgeService],
                   "manager": [ChromeDriverManager, GeckoDriverManager, EdgeChromiumDriverManager],
                   "options": [webdriver.ChromeOptions(), webdriver.FirefoxOptions(), webdriver.EdgeOptions()]}
    global driver
    with open("../.project-metadata.yaml") as yaml_config:
        configs = yaml.load(yaml_config, yaml.FullLoader)
        browser = configs["runtimes"][0]["browser-type"]
        headless = configs["runtimes"][0]["headless-browsing"]
    if name_similarity(str(headless), "true") > 0.6:
        for ind in range(len(browser_mat["name"])):
            browser_mat["options"][ind].add_argument("--headless")
    if browser is not None:
        for ind in range(len(browser_mat["name"])):
            if name_similarity(browser, browser_mat["name"][ind]) > browser_mat["threshold"][ind]:
                try:
                    driver = browser_mat["driver"][ind](
                        service=browser_mat["service"][ind](browser_mat["manager"][ind]().install()),
                        options=browser_mat["options"][ind])
                    break
                except selenium.common.exceptions.SessionNotCreatedException:
                    continue
    if driver is None:
        for ind in range(0, len(browser_mat["name"])):
            try:
                driver = browser_mat["driver"][ind](
                    service=browser_mat["service"][ind](browser_mat["manager"][ind]().install()),
                    options=browser_mat["options"][ind])
                break
            except selenium.common.exceptions.SessionNotCreatedException:
                continue
    if driver is not None:
        driver.implicitly_wait(1)
        return
    raise selenium.common.exceptions.SessionNotCreatedException( "Please have Chrome, Firefox, or Microsoft Edge available.")


def end_driver():
    driver.close()


def setup():
    global artists_data
    artists_data = pd.read_csv("https://raw.githubusercontent.com/Idanlau/Cloudera_Hackathon/main/artDataset.csv")
    global artists
    artists = artists_data["artist"].tolist()
    start_driver()


def artsy_link(artist):
    name = clean_string(artist)
    print(f"Artist: {artist} ({name})")
    name = "-".join(name.lower().split())
    url = "https://artsy.net/artist/" + name
    return url


def artsy_search_link(artist):
    driver.get("https://artsy.net/artists/")
    search = driver.find_element("xpath", "//input[@class='Input__StyledInput-bysdh7-0 gFWniP']")
    search.send_keys(artist)
    time.sleep(2)
    results_list = driver.find_element("xpath", "//ul[@class='react-autosuggest__suggestions-list']")
    iteration = 0
    highest_similarity, highest_iteration = 0, 0
    try:
        result = results_list.find_element("xpath", f".//li[@data-suggestion-index='{iteration}']")
        while result:
            iteration += 1
            result = results_list.find_element("xpath", f".//li[@data-suggestion-index='{iteration}']")
            result_type = result.find_element("xpath", ".//div[@class='Box-sc-15se88d-0 Text-sc-18gcpao-0 caIGcn wvERG']").text
            result_name = result.find_element("xpath", ".//div[@class='Box-sc-15se88d-0 Text-sc-18gcpao-0  dYxhVR']").text
            if result_type.lower() == "artist":
                similarity = name_similarity(artist, result_name)
                print(f"{artist}: ({result_name} = {similarity})")
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    highest_iteration = iteration
    except selenium.common.exceptions.NoSuchElementException:
        if highest_similarity >= 0.6:
            artist_result = driver.find_element("xpath", f"//li[@data-suggestion-index='{highest_iteration}']")
            artist_link = artist_result.find_element("xpath", ".//a[@class='RouterLink__RouterAwareLink-sc-1nwbtp5-0 bwxvKP SuggestionItem__SuggestionItemLink-sc-1ivuich-0 bssCjZ']").get_attribute("href")
            return artist_link
        else:
            return ""


def biography_artsy(artist):
    links = [artsy_link, artsy_search_link]
    for num_link in range(len(links)):
        link = links[num_link](artist)
        if len(link) == 0: break
        driver.get(link)
        try:
            driver.find_element("xpath", "//div[@class='Box-sc-15se88d-0 Text-sc-18gcpao-0  bTXFzS']")
            continue
        except selenium.common.exceptions.NoSuchElementException:
            try:
                expand_bio = driver.find_element("xpath", "//button[@class='Clickable-sc-10cr82y-0 dgMPBb']")
                expand_bio.click()
                biography = driver.find_element("xpath", "//div[@class='ReadMore__Container-sc-1bqy0ya-0 hSZzlP']").text
                return biography
            except selenium.common.exceptions.NoSuchElementException:
                return ""
    unavailable_artists.append(artist)
    print(f"{artist} unavailable")
    return ""


def generate_artist_fame():
    for artist in artists:
        if artist not in unique_artists:
            biography = biography_artsy(artist)
            fame = len(biography.split())
            artists_fame.append(fame)
            unique_artists[artist] = fame
        else:
            artists_fame.append(unique_artists[artist])
    driver.close()
    artists_data.insert(artists_data.columns.get_loc("artist") + 1, "fame", artists_fame)
    artists_data.to_csv("artist_fame.csv")


def main():
    setup()
    generate_artist_fame()


if __name__ == "__main__":
    main()
