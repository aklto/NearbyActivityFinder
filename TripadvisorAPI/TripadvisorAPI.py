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

        try:
            response_nearby = requests.get(url_nearby, headers=headers)
            response_nearby.raise_for_status()  # Проверка на статус ответа 200 (ОК)
            data = response_nearby.json()

            # Проверяем, содержит ли ответ все необходимые ключи
            if 'data' in data and len(data['data']) > self.index_of_place and self.type_info in data['data'][
                self.index_of_place]:
                return data['data'][self.index_of_place][self.type_info]
            else:
                print("Unexpected response structure.")
                return None  # или возвращаем другое значение по умолчанию

        except requests.RequestException as e:
            print(f"Error fetching nearby places from TripAdvisor: {e}")
            return None  # или возвращаем другое значение по умолчанию

class Excerpt_From_Dictionary_details:
    def __init__(self, location_id, key, category, type_info):
        self.location_id = location_id
        self.key = key
        self.category = category
        self.type_info = type_info

    def response_photo(self):
        headers = {"accept": "application/json"}
        url_photo = f"https://api.content.tripadvisor.com/api/v1/location/{self.location_id}/photos?key={self.key}&language=en"

        try:
            response_photo = requests.get(url_photo, headers=headers)
            response_photo.raise_for_status()  # Бросит исключение, если статус ответа не 200 (ОК)
            data = response_photo.json()
            return data.get('data', [])  # Вернуть данные или пустой список, если 'data' отсутствует
        except requests.RequestException as e:
            print(f"Error fetching photos from TripAdvisor: {e}")
            return []  # Возвращаем пустой список в случае ошибки

    def response_details(self):
        headers = {"accept": "application/json"}
        url_details = f"https://api.content.tripadvisor.com/api/v1/location/{self.location_id}/details?key={self.key}"

        try:
            response_details = requests.get(url_details, headers=headers)
            response_details.raise_for_status()  # Бросит исключение, если статус ответа не 200 (ОК)
            return response_details.json()
        except requests.RequestException as e:
            print(f"Error fetching details from TripAdvisor: {e}")
            return {}  # Возвращаем пустой словарь в случае ошибки


if __name__ == "__main__":
    longitude = 40.18648563845781
    latitude = 44.51290460485342
    category = "restaurants"
    location_id = "20091342"
    type_info = "location_id"

    element1 = Excerpt_From_Dictionary_Nearby(longitude, latitude, TRIPADVISOR_KEY, category, type_info,1)
    element2 = Excerpt_From_Dictionary_details(location_id, TRIPADVISOR_KEY, category, type_info)

    data = element2.response_details()

    name = data['name']
    description = data['description']
    rating = data['rating']

    print(f"Name: {name}")
    print(f"Description: {description}")
    print(f"Rating: {rating}")

    # print(element2.response_details())
