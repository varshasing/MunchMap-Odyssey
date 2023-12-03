import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("YELP_KEY")

# going to pass in a list of coordinates, including the start and the end; ignore the first and last entry in the list.
# need to figure out how to return the bset restaurant per location, so the final returned list will ideally have three entries
# still search for the best three restaurants per location, and store these in three separate lists. Will return a fourth list, which will be the best restaurant per location
# if any of the three lists are empty, try to still return a list of three restaurants by appending another restaurant from a different list. If we cannot return a list of three
# then, we will return a smaller list size.

#if we cannot find ANY restaurants, then we will return an empty list. This will be handled by the front end, which will display a message saying that no restaurants were found.



def search_yelp(api_key, search_term, userPrice, latitude, longitude, radius=120):
    #need to call restaurant_search three times, each time with a different set of coordinates
    list_one = restaurant_search(api_key, search_term, userPrice, latitude[1], longitude[1], radius)
    list_two = restaurant_search(api_key, search_term, userPrice, latitude[2], longitude[2], radius)
    list_three = restaurant_search(api_key, search_term, userPrice, latitude[3], longitude[3], radius)

    # most ideal case, where all three lists have at least one entry. append the LAST entry for every list to the final list
    retList = []
    if len(list_one) > 0 and len(list_two) > 0 and len(list_three) > 0:
        retList.append(list_one[-1])
        retList.append(list_two[-1])
        retList.append(list_three[-1])
        return retList
    
    # unideal case, all lists are empty and user has to redo their search
    if len(list_one) == 0 and len(list_two) == 0 and len(list_three) == 0:
        print("No results found, all lists are empty")
        return retList
    
    # check if any of the two lists are empty. If they both are empty, return whatever I have from the non-empty list
    if len(list_one) == 0 and len(list_two) == 0:
        return list_three
    elif len(list_one) == 0 and len(list_three) == 0:
        return list_two
    elif len(list_two) == 0 and len(list_three) == 0:
        return list_one
    
    # three other cases, for each of the lists being empty. Each has 4 different possibilities, depending on how many entries are in the other lists
    # two coming from one list; three coming from one list. Then account for there not being three entries in the other two lists, appending and returning what you can.
    if len(list_one) == 0:
        # if there are less than three entries in the other two lists, return the shorter list
        if (len(list_two) + len(list_three) < 3):
            print("Less that three entries found. returning shorter list")
            retList.append(list_two)
            retList.append(list_three)
            return retList
        # returning two from the second, one from the third
        if len(list_two) >= 2 and len(list_three) >= 1:
            retList.append(list_two[-1])
            retList.append(list_two[-2])
            retList.append(list_three[-1])
            return retList
        # returning one from the second, two from the third
        elif len(list_two) >= 1 and len(list_three) >= 2:
            retList.append(list_two[-1])
            retList.append(list_three[-1])
            retList.append(list_three[-2])
            return retList
    # same as above, but for list_two
    if len(list_two) == 0:
        if (len(list_one) + len(list_three) < 3):
            print("Less that three entries found. returning shorter list")
            retList.append(list_one)
            retList.append(list_three)
            return retList
        # returning two from the first, one from the third
        if len(list_one) >= 2 and len(list_three) >= 1:
            retList.append(list_one[-1])
            retList.append(list_one[-2])
            retList.append(list_three[-1])
            return retList
        # returning one from the first, two from the third
        elif len(list_one) >= 1 and len(list_three) >= 2:
            retList.append(list_one[-1])
            retList.append(list_three[-1])
            retList.append(list_three[-2])
            return retList
    # same as above, but for list_three
    if len(list_three) == 0:
        if (len(list_one) + len(list_two) < 3):
            print("Less that three entries found. returning shorter list")
            retList.append(list_one)
            retList.append(list_two)
            return retList
        # returning two from the first, one from the second
        if len(list_one) >= 2 and len(list_two) >= 1:
            retList.append(list_one[-1])
            retList.append(list_one[-2])
            retList.append(list_two[-1])
            return retList
        # returning one from the first, two from the second
        elif len(list_one) >= 1 and len(list_two) >= 2:
            retList.append(list_one[-1])
            retList.append(list_two[-1])
            retList.append(list_two[-2])
            return retList
    
    print("Instance in which I get to this point should not happen")
    return retList



def restaurant_search(api_key, search_term, userPrice, latitude, longitude, radius): # after I sort the data, I need to return the top 3 results as a list each time I call this function
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
    latitude = [0, 37.7749, 41.8781, 37.7749, 0]  #passed by google maps api
    longitude = [0, -122.4194, 87.6298, -122.4194 ,0] #passed by google maps api
    userPrice = 2   #passed by front end

    # this will need to be called AFTER user enters their search_term.
    search_yelp(api_key, search_term, userPrice, latitude, longitude,)
