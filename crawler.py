import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Replace with your actual API key
API_KEY = 'AIzaSyB91olCjO0desn4h5SwdxyU50VGcPnNKLQ'

def load_cities():
    with open('cities.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def search_videos(city_name, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    try:
        search_response = youtube.search().list(
            q=f"{city_name} travel",
            type='video',
            part='id,snippet',
            maxResults=10
        ).execute()

        videos = []
        for item in search_response['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            channel_name = item['snippet']['channelTitle']
            published_at = item['snippet']['publishedAt']

            # Get video details
            video_response = youtube.videos().list(
                part='contentDetails,statistics',
                id=video_id
            ).execute()

            duration = video_response['items'][0]['contentDetails']['duration']
            view_count = int(video_response['items'][0]['statistics']['viewCount'])

            videos.append({
                "id": video_id,
                "title": title,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "videoId": video_id,
                "channelName": channel_name,
                "duration": duration,
                "date": published_at.split('T')[0],  # Extract date part
                "views": view_count
            })

        return videos

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return []

def main():
    cities = load_cities()
    all_videos = {}

    for city in cities:
        city_id = city['id']
        city_name = city['name']
        print(f"Searching videos for {city_name}...")
        videos = search_videos(city_name, API_KEY)
        all_videos[city_id] = videos

    with open('videos.json', 'w', encoding='utf-8') as file:
        json.dump(all_videos, file, ensure_ascii=False, indent=2)

    print("Video data has been saved to videos.json")

if __name__ == "__main__":
    main()
