from config import DATA_PATH
from utils import read_csv


def aff2city(aff):
    city_df = read_csv(DATA_PATH, 'city_name.csv')
    city_names = [city.lower() for city in city_df['City'].values]
    for i in range(len(city_names)):
        if city_names[i] in aff.lower() and city_df['level'][i] == 1:
            return city_names[i]


def aff2country(aff):
    city_df = read_csv(DATA_PATH, 'city_name.csv')
    city_names = [city.lower() for city in city_df['City'].values]
    for i in range(len(city_names)):
        if city_names[i] in aff.lower():
            return city_df['Country'][i].lower()
    country_names = [country.lower() for country in city_df['Country'].values]
    for country in country_names:
        if country in aff.lower():
            return country
