import requests

url = "https://api.yelp.com/v3/businesses/search?sort_by=best_match&limit=20"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)