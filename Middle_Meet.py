from flask import Flask, render_template, request
import requests
import json
import math

app = Flask(__name__)

google_maps_api_key = ""

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
        'key': '',
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

    return lat3, lon2
    pass

def find_recommendations(lat, lon, interests):
    #define the google places API endpoint for nearby search
    places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    #define the parameters for the API request
    params = {
        'location': f"{lat}, {lon}", #coordinates in the format "latitude, longitude"
        'radius': 1000, #search radius in meters 
        'type': 'restaurant',
        'key': ''
    }

    #make API request
    response = request.get(places_url, params= params)
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

            # check if the place matches the user's interests (can implmement greater filtering)
            if any(interests.lower() in place_name.lower() for interst in interests):
                recommended_places.append({
                    'name': place_name,
                    'address': place_address,
                    'rating': place_rating,
                })

    return recommended_places
    pass


if __name__ == '__main__':
    #app.run(debug=True)
    user_location = input("Enter a location: ")
    user_interests = input("Enter your interests (comma-separated): ").split(",")

    latitude, longitude = get_coordinates(user_location)
    if latitude is not None and longitude is not None:
        coords = (latitude, longitude)
        find_recommendations(coords, user_interests)
    else:
        print("Invalid location or unable to retrieve coordinates.")
