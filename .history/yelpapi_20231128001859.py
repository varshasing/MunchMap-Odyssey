import requests

def search_yelp(api_key, term, location):
    # Yelp API endpoint for business search
    endpoint = "https://api.yelp.com/v3/businesses/search"

    # Set up the request headers with your API key
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # Set up the parameters for the search
    params = {
        "term": term,
        "location": location
    }

    # Make the API call
    response = requests.get(endpoint, headers=headers, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Print the business information
        for business in data["businesses"]:
            print(f"Name: {business['name']}")
            print(f"Rating: {business['rating']}")
            print(f"Address: {', '.join(business['location']['display_address'])}")
            print("\n")
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual Yelp API key
    api_key = 'riko09ZEG7R1wBgMqZbjv4uNtMHGBb-t1-2zFrGjAy7Ka2nRwVqD8t3-6GPJXMTfDJEiuQ0RlM24Qh6umi_rVm2Gs7szTULJDRYPfsBEtPYqo0if4YP1_-RLlb9eZXYx'

    # Define your search term and location
    search_term = "restaurants"
    location = "San Francisco, CA"

    # Perform the Yelp API search
    search_yelp(api_key, search_term, location)
