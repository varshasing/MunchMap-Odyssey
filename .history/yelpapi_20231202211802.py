import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("YELP_KEY")

def search_yelp(api_key, search_term, userPrice, latitude, longitude, radius=200): # after I sort the data, I need to return the top 3 results as a list each time I call this function
    # Yelp API endpoint for business search
    endpoint = "https://api.yelp.com/v3/businesses/search"

    # Set up the request headers with your API key
    headers = {
        "Authorization": f"Bearer {api_key}"
    }


    # Set up the parameters for the search
    params = {
        "term": search_term,
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius,
        "price": "1,2,3,4"
        #"cuisine": cuisine
    }

    # Make the API call
    response = requests.get(endpoint, headers=headers, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # need to sort the business data by rating
        sorted_businesses = []
        for business in data["businesses"]:
            sorted_businesses = sorted(data["businesses"], key=lambda x: x["rating"], reverse=True)

        numberofbusinesses = 0
        final_sorted = [] #empty list
        if(len(sorted_businesses) == 0):
            print("No results found, no sorted businesses")
            return sorted_businesses
        for business in sorted_businesses:
            if business["price"] == "$" and userPrice == 1:
                numberofbusinesses += 1
                final_sorted.append(business)

            elif business["price"] == "$$" and userPrice <= 2:
                final_sorted.append(business)
                numberofbusinesses += 1

            elif business["price"] == "$$$" and userPrice <= 3:
                final_sorted.append(business)
                numberofbusinesses += 1

            elif business["price"] == "$$$$" and userPrice <= 4:
                final_sorted.append(business)
                numberofbusinesses += 1

        final_sorted = sorted(final_sorted, key=lambda x: x["price"], reverse=True)

        last_list = []
        # i want to make another list, only containting the top 3 results price, rating, name, address, and coordinates; need to keep in mind that we might not be returning 3 results
        currentAppend = 0
        for business in final_sorted:
            last_list.append({"name": business["name"], "rating": business["rating"], "price": business["price"], "address": business["location"]["address1"], "coordinates": business["coordinates"], "id": business["id"]})
            currentAppend += 1
            if currentAppend == 3 and numberofbusinesses >= 3:
                break
            elif currentAppend == 2 and numberofbusinesses == 2:
                break
            elif currentAppend == 1 and numberofbusinesses == 1:
                break

        print("")

        list_of_ids = [] # empty list, has the corresponding IDs for 
        for i in last_list:
            list_of_ids.append(i["id"])
        
        # need to return the last three results, or less depending on how many if ever returns
        if len(last_list) == 3:
            print("three!")
            for i in last_list[:3]:
                print(i["name"])
            return last_list[:3]
        elif len(last_list) == 2:
            print("two!")
            for i in last_list[:2]:
                print(i["name"])
            return last_list[:2]
        elif len(last_list) == 1:
            print("one!")
            for i in last_list[:1]:
                print(i["name"])
            return last_list[:1]
        elif len(last_list) == 0:
            print("No results found, error in final_sorted")
            return last_list
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual Yelp API key
    #api_key = 'riko09ZEG7R1wBgMqZbjv4uNtMHGBb-t1-2zFrGjAy7Ka2nRwVqD8t3-6GPJXMTfDJEiuQ0RlM24Qh6umi_rVm2Gs7szTULJDRYPfsBEtPYqo0if4YP1_-RLlb9eZXYx'

    # Define your search term and coordinates
    search_term = "Italian" #Passed by front end
    latitude = 37.7749  #passed by google maps api
    longitude = -122.4194 #passed by google maps api
    userPrice = 2   #passed by front end

    # this will need to be called AFTER user enters their search_term.
    search_yelp(api_key, search_term, userPrice, latitude, longitude,)
