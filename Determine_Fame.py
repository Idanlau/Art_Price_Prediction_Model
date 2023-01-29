import pandas as pd
import selenium.common.exceptions
from selenium import webdriver
import time
import unicodedata


def remove_diacritics(string):
    nfkd_string = unicodedata.normalize("NFKD", string)
    return "".join([c for c in nfkd_string if not unicodedata.combining(c)])


artists_data = pd.read_csv("artDataset.csv")
artists = artists_data["artist"].tolist()
artists_fame, unavailable_artists = [], []
unique_artists = {}

driver = webdriver.Chrome("C:\\Users\\james\\Downloads\\chromedriver")
driver.implicitly_wait(0.75)


def biography_artsy(artist):
    name = remove_diacritics(str(artist))
    print(f"Artist: {artist} ({name})")
    name = "-".join(name.lower().split())
    url = "https://artsy.net/artist/" + name
    driver.get(url)
    try:
        expand_bio = driver.find_element("xpath", "//button[@class='Clickable-sc-10cr82y-0 dgMPBb']")
        expand_bio.click()
        biography = driver.find_element("xpath", "//div[@class='ReadMore__Container-sc-1bqy0ya-0 hSZzlP']").text
        return biography
    except selenium.common.exceptions.NoSuchElementException:
        unavailable_artists.append(artist)
        return ""


offset = 0
lim = len(artists_data)
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
        temp_fame = artists_fame.copy()
        temp_data = artists_data.copy()
        while len(temp_fame) < len(temp_data):
            temp_fame.append(None)
        temp_data.insert(2, "fame", temp_fame)
        temp_data.to_csv("temp_fame.csv")
while len(artists_fame) < len(artists_data):
    artists_fame.append(None)
artists_data.insert(2, "fame", artists_fame)
artists_data.to_csv("artist_fame.csv")
print(artists_data[["artist", "fame"]].head(lim))
print(unavailable_artists)
