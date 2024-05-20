from bs4 import BeautifulSoup
from selenium import webdriver
from flask import jsonify
import time
import re
import pandas as pd

#struggled first with getting selenium to run chromedriver, fixed with port

def fetch_data(url):
    all_data = {}
    dataLST = []

    print("Up and running")
    #target_url = "https://www.expedia.com/Cansaulim-Hotels-Heritage-Village-Resort-Spa-Goa.h2185154.Hotel-Information?=one-key-onboarding-dialog&chkin=2024-05-18&chkout=2024-05-24&destType=MARKET&destination=Goa%2C%20India%20%28GOI-Dabolim%29&latLong=15.383019%2C73.838253&regionId=6028089&rm1=a2"
    #target_url = "https://www.expedia.com/Hotel-Search?destination=Kitty+Hawk%2C+North+Carolina%2C+United+States+of+America&regionId=122251&latLong=36.06461%2C-75.705734&flexibility=0_DAY&d1=2024-05-18&startDate=2024-05-18&d2=2024-05-20&endDate=2024-05-20&adults=2&rooms=1&theme=&userIntent=&semdtl=&useRewards=false&sort=RECOMMENDED"
    #target_url = "https://www.google.com/"

    service = webdriver.ChromeService(port=9515)

    driver = webdriver.Chrome(service=service)
    driver.get(url)

    time.sleep(5) 

    resp = driver.page_source

    soup = BeautifulSoup(resp, 'html.parser')

    priceLST = []
    hotelLST = []
    reviewLST = []
    amenitiesLST = []
    locationLST = []
    imageLST = []
    roomLST = []

    cards = soup.find_all('div', attrs={'data-stid': "lodging-card-responsive"})
    for card in cards:
        # print(card)

        reviews = card.find_all('span')
        if len(reviews) > 3 and reviews[3].text == "Ad":
            continue
        
        # for i in range(len(reviews)):
        #     print("review: ", reviews[i].text, " at: ", i)
        
        startIdx = 5
        for i in range(min(len(reviews), 6)):
            if reviews[i].text.count('.') == 2:
                startIdx = i + 2
                break
        reviewLST.append([reviews[startIdx].text, reviews[startIdx + 2].text, reviews[startIdx + 3].text])

        all_prices = card.find_all('div', attrs={'data-test-id': "price-summary-message-line"})
        priceLST.append(all_prices[-2].text + " price including taxes & fees!")

        hotels = card.find_all('h3')
        try:
            hotelLST.append(hotels[1].text)
        except:
            hotelLST.append("None")

        amenities = card.find_all('div')

        #print("LOCATION: ", amenities[21].text)
        if (amenities[21].text.count(',') > 0):
            roomLST.append(amenities[21].text)
            locationLST.append(amenities[22].text)
            matches = re.split('(?<=.)(?=[A-Z])', amenities[23].text)
        #print("MATCHES: ", matches)
            amenitiesLST.append(matches)
        else:
            roomLST.append("None provided")
            locationLST.append(amenities[21].text)
            matches = re.split('(?<=.)(?=[A-Z])', amenities[22].text)
            amenitiesLST.append(matches)

        images = card.find_all('img')
        try:
            imageLST.append(images[0]['src'])
        except:
            imageLST.append("None")

        # for i in range(len(amenities)):
        #     print("amenities: ", amenities[i].text, " at: ", i)

        # print()

        # print("Hotel: ", hotelLST)
        # print("Price: ", priceLST)
        # print("Reviews: ", reviewLST)
        # print("Amenities: ", amenitiesLST)
        # print("Location: ", locationLST)
        # print("Images: ", imageLST)
        # print("Room: ", roomLST)

        driver.close()

        all_data["hotels"] = hotelLST
        all_data["prices"] = priceLST
        all_data["reviews"] = reviewLST
        all_data["amenities"] = amenitiesLST
        all_data["location"] = locationLST
        all_data["images"] = imageLST
        all_data["rooms"] = roomLST

        #print(resp)
        # with open('data.json', 'w') as f:
        #     json.dump(all_data, f)

        # dataLST.append(hotelLST)
        # dataLST.append(priceLST)
        # dataLST.append(reviewLST)
        # dataLST.append(locationLST)
        # dataLST.append(imageLST)
        # dataLST.append(roomLST)

        df = pd.DataFrame({'hotels': hotelLST, 'prices': priceLST, 'reviews' : reviewLST, 'amenities': amenitiesLST, 'location': locationLST, 'imageURl': imageLST, 'rooms' : roomLST})
        df.to_csv('hotel_data.csv', index=False)

        return all_data
        #return jsonify(dataLST)