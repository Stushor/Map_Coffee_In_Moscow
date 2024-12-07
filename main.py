import json
from geopy.distance import distance
import folium
import fetch_coordinates as ft_coordinates
from dotenv import load_dotenv
import os


def load_coffee_data(file_path):
    with open(file_path, "r", encoding="CP1251") as file:
        coffee_data = json.load(file)
    return coffee_data


def calculate_distances(person_coordinates, coffee_data):
    coffee_info = []
    for coffee_shop in coffee_data:
        shop_coordinates = coffee_shop['geoData']['coordinates']
        shop_coords = (shop_coordinates[1], shop_coordinates[0])
        person_coords = (person_coordinates[1], person_coordinates[0])
        distance_to_person = distance(person_coords, shop_coords).km
        coffee_info.append({
            'Name': coffee_shop['Name'],
            'distance': distance_to_person,
            'latitude': shop_coords[1],
            'longitude': shop_coords[0],
        })
    return coffee_info


def get_distance(coffee):
    return coffee['distance']


def create_map(person_coordinates, coffee_info_sorted, output_file="index.html"):
    m = folium.Map(location=[person_coordinates[1], person_coordinates[0]], zoom_start=12)

    folium.Marker(
        location=[person_coordinates[1], person_coordinates[0]],
        tooltip="Ваше местоположение",
        popup="Вы здесь",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    for coffee_shop in coffee_info_sorted[:5]:
        folium.Marker(
            location=[coffee_shop['longitude'], coffee_shop['latitude']],
            tooltip=coffee_shop['Name'],
            popup=f"{coffee_shop['Name']}\n{coffee_shop['distance']:.2f} км",
            icon=folium.Icon(color="green", icon="info-sign")
        ).add_to(m)

    m.save(output_file)


def main():
    person_location = input('Где вы находитесь? ')
    person_coordinates = ft_coordinates.fetch_coordinates(api_key, person_location)

    if not person_coordinates:
        print("Ошибка получения координат. Убедитесь, что адрес указан корректно.")
        return

    coffee_data = load_coffee_data("coffee.json")

    coffee_info = calculate_distances(person_coordinates, coffee_data)

    coffee_info_sorted = sorted(coffee_info, key=get_distance)

    create_map(person_coordinates, coffee_info_sorted)


if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ['APIKEY_MAP']
    main()
