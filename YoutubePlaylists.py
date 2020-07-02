import os 
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_new.json"

    #Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
      api_service_name, api_version, credentials=credentials)
    
    #Retrieve playlists on your channel 
    request = youtube.playlists().list(
        part="snippet",
        maxResults = 50, 
        mine=True
    )
    
    response = request.execute()
    
    print(response)
    
    for line in response['items']:
        print(line['snippet']['title'])
    
    #Retrieve playlists on next page
    try: 
        while response['nextPageToken']:

            nextPage = response['nextPageToken']  
            request = youtube.playlists().list(
                part="snippet",
                maxResults = 50, 
                pageToken = nextPage,
                mine=True
            )
            response = request.execute()
            for line in response['items']:
                print(line['snippet']['title'])

    except:
        print("No next page")       
            

if __name__ == "__main__":
    main()