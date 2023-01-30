from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import pandas as pd
import selenium.common.exceptions
from selenium import webdriver
import time
import unicodedata

nltk.download("stopwords")

from nltk.corpus import stopwords

stopword = stopwords.words('english')


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


artists_data = pd.read_csv("artDataset.csv")
artists = artists_data["artist"].tolist()
artists_fame, unavailable_artists = [], []
unique_artists = {}

driver = webdriver.Chrome("C:\\Users\\james\\Downloads\\chromedriver")
driver.implicitly_wait(1)


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


def store_temp_csv():
    temp_fame = artists_fame.copy()
    temp_data = artists_data.copy()
    while len(temp_fame) < len(temp_data):
        temp_fame.append(None)
    temp_data.insert(2, "fame", temp_fame)
    temp_data.to_csv("temp_fame.csv")


offset = 0
"""
# Find the index of the last valid fame if exception occurs
for fame_ind in range(len(artists_fame)):
    if pd.isna(artists_fame[fame_ind]):
        offset = fame_ind
        break
artists_fame = artists_fame[:offset]
"""
lim = len(artists)
for iter in range(offset):
    artists_fame.append(None)
for artist in artists[offset:lim]:
    if artist not in unique_artists:
        biography = biography_artsy(artist)
        fame = len(biography.split())
        artists_fame.append(fame)
        unique_artists[artist] = fame
    else:
        artists_fame.append(unique_artists[artist])
    if len(artists_fame) % 20 == 0:
        store_temp_csv()

unavailable_artists_file = open("unavailable_artists.txt", "w")
unavailable_artists_file.write(str(unavailable_artists))
while len(artists_fame) < len(artists_data):
    artists_fame.append(None)
artists_data.insert(artists_data.columns.get_loc("artist") + 1, "fame", artists_fame)
artists_data.to_csv("artist_fame.csv")
print(artists_data[["artist", "fame"]].head(lim))
