import requests

from API_Token.API_Token import TRIPADVISOR_KEY

class Excerpt_From_Dictionary_Nearby:
    def __init__(self, longitude, latitude, key, category, type_info, index_of_place):
        self.index_of_place = index_of_place
        self.longitude = longitude
        self.latitude = latitude
        self.key = key
        self.category = category
        self.type_info = type_info

    def response_nearby(self):
        headers = {"accept": "application/json"}
        url_nearby = f"https://api.content.tripadvisor.com/api/v1/location/nearby_search?latLong={self.longitude}%2C{self.latitude}&key={self.key}&category={self.category}"
        response_nearby = requests.get(url_nearby, headers=headers)
        return response_nearby.json()['data'][self.index_of_place][self.type_info]


class Excerpt_From_Dictionary_Photo:
    def __init__(self, location_id, key, category, type_info):
        self.location_id = location_id
        self.key = key
        self.category = category
        self.type_info = type_info

    def response_photo(self):
        headers = {"accept": "application/json"}
        url_photo = f"https://api.content.tripadvisor.com/api/v1/location/{self.location_id}/photos?key={self.key}"
        response_photo = requests.get(url_photo, headers=headers)
        return response_photo.json()['data'][self.index_of_place]

    def response_details(self):
        headers = {"accept": "application/json"}
        url_details = f"https://api.content.tripadvisor.com/api/v1/location/{self.location_id}/details?key={self.key}"
        response_details = requests.get(url_details, headers=headers)
        return response_details.json()['data'][self.index_of_place]


if __name__ == "__main__":
    longitude = 40.18648563845781
    latitude = 44.51290460485342
    category = "restaurants"
    location_id = "293932"
    type_info = "location_id"

    element1 = Excerpt_From_Dictionary_Nearby(longitude, latitude, TRIPADVISOR_KEY, category, type_info)
    element2 = Excerpt_From_Dictionary_Photo(location_id, TRIPADVISOR_KEY, category, type_info)
    print(element1.response_nearby())

