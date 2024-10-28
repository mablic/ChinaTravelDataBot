from connection import db
import json
from google.cloud.firestore_v1.base_query import FieldFilter

def insert_cities_to_firebase(jsonName, collectionName):
    # Read the JSON file
    with open(jsonName, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Get a reference to the collection
    data_ref = db.collection(collectionName)
    
    # Insert each item into Firebase
    for d in data:
        # Use the 'id' field as the document ID
        doc_ref = data_ref.document(d['cityId'])
        doc_ref.set(d)
    
    print(f"Successfully inserted {collectionName} into Firebase.")

def insert_to_places_firebase(jsonName, collectionName):
    # Read the places.json file
    with open(jsonName, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Get a reference to the 'places' collection
    places_ref = db.collection(collectionName)
    
    # Insert places for each city into Firebase
    for city_id, city_data in data.items():
        city_doc_ref = places_ref.document(city_id)
        city_doc = city_doc_ref.get()

        if city_doc.exists:
            # City document exists, check for new places
            existing_places = city_doc.to_dict().get('places', [])
            existing_place_ids = set(place['id'] for place in existing_places)
            new_places = [place for place in city_data['places'] if place['id'] not in existing_place_ids]

            if new_places:
                # Append new places to the existing places
                updated_places = existing_places + new_places
                city_doc_ref.update({'places': updated_places})
                print(f"Added {len(new_places)} new place(s) to {city_id}")
            else:
                print(f"No new places to add for {city_id}")
        else:
            # City document doesn't exist, create it with all places
            city_doc_ref.set(city_data)
            print(f"Created new document for {city_id} with {len(city_data['places'])} place(s)")
    
    print(f"Successfully updated places in Firebase.")

def insert_videos_to_firebase(jsonName, collectionName):
    # Read the videos.json file
    with open(jsonName, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Get a reference to the 'videos' collection
    videos_ref = db.collection(collectionName)
    
    # Insert videos for each city into Firebase
    for city_id, city_videos in data.items():
        city_doc_ref = videos_ref.document(city_id)
        city_doc = city_doc_ref.get()

        if city_doc.exists:
            # City document exists, check for new videos
            existing_videos = city_doc.to_dict().get('videos', [])
            existing_video_ids = set(video['id'] for video in existing_videos)
            new_videos = [video for video in city_videos if video['id'] not in existing_video_ids]

            if new_videos:
                # Append new videos to the existing videos
                updated_videos = existing_videos + new_videos
                city_doc_ref.update({'videos': updated_videos})
                print(f"Added {len(new_videos)} new video(s) to {city_id}")
            else:
                print(f"No new videos to add for {city_id}")
        else:
            # City document doesn't exist, create it with all videos
            city_doc_ref.set({'videos': city_videos})
            print(f"Created new document for {city_id} with {len(city_videos)} video(s)")
    
    print(f"Successfully updated videos in Firebase.")

def insert_apps_to_firebase(jsonName, collectionName):
    # Read the apps.json file
    with open(jsonName, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Get a reference to the 'apps' collection
    apps_ref = db.collection(collectionName)
    
    # Insert or update apps in Firebase
    for app in data['apps']:
        app_doc_ref = apps_ref.document(app['name'])
        app_doc = app_doc_ref.get()

        if app_doc.exists:
            # App document exists, update it
            app_doc_ref.update(app)
            print(f"Updated app: {app['name']}")
        else:
            # App document doesn't exist, create it
            app_doc_ref.set(app)
            print(f"Created new app: {app['name']}")
    
    print(f"Successfully updated apps in Firebase.")

# Call the functions to insert data
if __name__ == "__main__":
    # insert_cities_to_firebase("cities.json", "cities")
    # insert_to_places_firebase("places_temp.json", "places")
    # insert_videos_to_firebase("videos.json", "videos")
    insert_apps_to_firebase("apps.json", "apps")
