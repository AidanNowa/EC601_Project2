from flask import Flask, render_template, request
import requests
import json
import math

app = Flask(__name__)

google_maps_api_key = "AIzaSyDstmnU4nHl4xfeIYsaCbyDlLPkAmBk-F4"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #get user input
        location1 = request.form['location1']
        location2 = request.form['location2']
        interests = request.form.getlist('interests')

        #use maps geocoding API to get coordinates for locations
        latitude1, longitude1 = get_coordinates(location1)
        latitude2, longitude2 = get_coordinates(location2)

        #calculate midpoint 
        lat3, lon3 = midpoint_coords = calculate_midpoint(latitude1, longitude1, latitude2, longitude2)
        
        #Use google place sAPI to find places of interests near midpoint
        recommended_places = find_recommendations(lat3, lon3, interests)

        return render_template('results.html', recommended_places=recommended_places)
    
    return render_template('index.html')

def get_coordinates(location):
    #define geocoding api endpoint
    geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json"

    #define the parameters for the api request
    params = {
        'address': location,
        'key': 'AIzaSyDstmnU4nHl4xfeIYsaCbyDlLPkAmBk-F4',
    }

    try:
        #Make the API request
        response = requests.get(geocoding_url, params=params)
        data = response.json()

        #Check if the request was successful and contains results
        if response.status_code == 200 and data.get('status') == 'OK':
            #Extract the coordinates (latitude and longitude) from the API response
            first_result = data['results'][0]
            location_coords = first_result['geometry']['location']
            latitude = location_coords['lat']
            longitude = location_coords['lng']
            return latitude, longitude
        
    except Exception as e:
        print(f"Error getting coordinates: {e}")

    return None, None
    pass

def calculate_midpoint(lat1, lon1, lat2, lon2):
    #convert lat and lon from deg to rad
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    #calc midpoint
    Bx = math.cos(lat2) * math.cos(lon2 - lon1)
    By = math.cos(lat2) * math.sin(lon2 - lon1)
    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2), math.sqrt((math.cos(lat1)+Bx) ** 2 + By ** 2))
    lon3 = lon1 + math.atan2(By, math.cos(lat1) + Bx)    
    
    #covert lat and lon back to degrees
    lat3 = math.degrees(lat3)
    lon3 = math.degrees(lon3)

    return lat3, lon3
    pass

def find_recommendations(lat, lon, interests):
    #define the google places API endpoint for nearby search
    places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    #define the parameters for the API request
    params = {
        'location': f"{lat}, {lon}", #coordinates in the format "latitude, longitude"
        'radius': 5000, #search radius in meters 
        'type': 'restaurant',
        'key': 'AIzaSyDstmnU4nHl4xfeIYsaCbyDlLPkAmBk-F4'
    }

    #make API request
    response = requests.get(places_url, params= params)
    data = response.json()

    recommended_places = []

    #check if the request was successful and contains results
    if response.status_code == 200 and data.get('status') == 'OK':
        results = data['results']

        for place in results:
            #extract relevant info about the places
            place_name = place['name']
            place_address = place.get('vicinity', 'N/A')
            place_rating = place.get('rating', 'N/A')

            for interest in interests:
                if interest.lower() in place_name.lower():
                    recommended_places.append({
                        'name': place_name,
                        'address': place_address,
                        'rating': place_rating,
                    })
                    break #to avoid adding the same place multiple times if matches many interests


    return recommended_places
    pass


if __name__ == '__main__':
    #app.run(debug=True)
    user_location_1 = input("Enter first location: ")
    user_location_2 = input("Enter second location: ")
    user_interests = input("Enter your interests (comma-separated): ").split(",")


    latitude_1, longitude_1 = get_coordinates(user_location_1)
    latitude_2, longitude_2 = get_coordinates(user_location_2)
    latitude, longitude = calculate_midpoint(latitude_1, longitude_1, latitude_2, longitude_2)
    print("Latitude, Longitude: ", latitude, ', ', longitude)
    if latitude is not None and longitude is not None:
        #coords = (latitude, longitude)
        recommended_places = find_recommendations(latitude, longitude, user_interests)
        if recommended_places:
            for place in recommended_places:
                print("Name:", place.get('name'))
                print("Address:", place.get('address'))
                print("Rating:", place.get('rating'))
                print('-----------------')
        else:
            print("No recommendations found for the given location and interests.")
    else:
        print("Invalid location or unable to retrieve coordinates.")