import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("YELP_KEY")

def search_yelp(api_key, search_term, userPrice, latitude, longitude, radius=40000): # after I sort the data, I need to return the top 3 results as a list each time I call this function
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
        for business in data["businesses"]:
            #print(f"{business['name']} ({business['rating']} stars) - {business['location']['address1']}")
            sorted_businesses = sorted(data["businesses"], key=lambda x: x["rating"], reverse=True)
        
        final_sorted = [] #empty list
        for business in sorted_businesses:
            if business["price"] == "$" and userPrice == 1:
                #print(f"{business['name']} ({business['rating']} stars) - {business['location']['address1']} - {business['price']}")
                final_sorted.append(business)
            elif business["price"] == "$$" and userPrice <= 2:
                #print(f"{business['name']} ({business['rating']} stars) - {business['location']['address1']} - {business['price']}")
                final_sorted.append(business)
            elif business["price"] == "$$$" and userPrice <= 3:
                #print(f"{business['name']} ({business['rating']} stars) - {business['location']['address1']} - {business['price']}")
                final_sorted.append(business)
            elif business["price"] == "$$$$" and userPrice <= 4:
                #print(f"{business['name']} ({business['rating']} stars) - {business['location']['address1']} - {business['price']}")
                final_sorted.append(business)
        final_sorted = sorted(final_sorted, key=lambda x: x["price"], reverse=True)
        last_list = []
        # i want to make another list, only containting the top 3 results price, rating, name, address, and coordinates
        for business in final_sorted:
            last_list.append({"name": business["name"], "rating": business["rating"], "price": business["price"], "address": business["location"]["address1"], "coordinates": business["coordinates"], "hours": business["hours"]"})
        for i in last_list[:3]:
            print(i["name"])
            print(type(i))
        return last_list[:3]
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual Yelp API key
    #api_key = 'riko09ZEG7R1wBgMqZbjv4uNtMHGBb-t1-2zFrGjAy7Ka2nRwVqD8t3-6GPJXMTfDJEiuQ0RlM24Qh6umi_rVm2Gs7szTULJDRYPfsBEtPYqo0if4YP1_-RLlb9eZXYx'

    # Define your search term and coordinates
    search_term = "food" #Passed by front end
    latitude = 42.34924366296191  #passed by google maps api
    longitude = -71.10598323136453 #passed by google maps api
    userPrice = 2   #passed by front end

    # this will need to be called AFTER user enters their search_term.
    search_yelp(api_key, search_term, userPrice, latitude, longitude,)
