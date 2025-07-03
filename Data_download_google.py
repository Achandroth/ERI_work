import requests
import csv

API_KEY = "YOUR API SHOULD GO HERE" #Replace with the API key you have created
location = "38.6573394841923, -87.17922263916101" #This an exmaple location i.e Washington Carnigie Library
radius = 123 #just type in the search radius. Catution distance is in meters, 5 miles ~ 8000 m

place_types = ["hospital","medical_center","medical_clinic"] #This can be updated to add more locations categories of your choice
all_results = {} # a place tp
output_file = "healthcare_facilities_nearby.csv"

def fetch_places(place_type):
    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={location}&radius={radius}&type={place_type}&key={API_KEY}"
    )
    response = requests.get(url)
    data = response.json()

    for result in data.get("results", []):
        place_id = result.get("place_id")
        if place_id not in all_results:
            all_results[place_id] = {
                "Name": result.get("name"),
                "Address": result.get("vicinity"),
                "Latitude": result["geometry"]["location"]["lat"],
                "Longitude": result["geometry"]["location"]["lng"],
                "Place_ID": place_id,
                "Rating": result.get("rating", "N/A"),
                "Type": place_type
            }

# Loop through all desired categories of places
for place_type in place_types:
    fetch_places(place_type)

# Save to CSV, this is so that we can download from google colab
with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Address", "Latitude", "Longitude", "Place_ID", "Rating", "Type"])
    for place in all_results.values():
        writer.writerow([
            place["Name"],
            place["Address"],
            place["Latitude"],
            place["Longitude"],
            place["Place_ID"],
            place["Rating"],
            place["Type"]
        ])

print(f" {len(all_results)} healthcare places saved to '{output_file}'")
