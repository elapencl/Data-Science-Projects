import json
import requests

'''
    The class YoutubeData will using your api key extract general data about the channel, and it will extract general 
    data about each video the user uploaded. 
    This code is inspired and helped by Python Engineer ^-^
'''


class YoutubeData:

    """
        In order to create our YoutubeData object, we will need the API key and the user's channel id.
        We will throughout this code determine the general channel data, data about the videos and the channel title!
    """

    def __init__(self, API_KEY, channel_id):
        self.API_KEY = API_KEY
        self.channel_id = channel_id
        self.channel_title = None
        self.videos_data = None
        self.channel_data = None

    """
        The first method we can do is the get_channel_data() - it's a simple method that will extract statistics about
        the channel using the URL below!
    """

    def get_channel_data(self):
        channel_url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.API_KEY}'
        json_url = requests.get(channel_url)
        channel_data = json.loads(json_url.text)
        channel_data = channel_data['items'][0]['statistics']
        self.channel_data = channel_data

    """
        The max amount of videos from which we will take info from is 50. In order to get data about each video, it will
         take us the following three methods. If we look at get_videos_data_from_current_page method, it takes in an URL
         and takes video data (i.e. id, title, date published) for videos displayed on the current page/URL.
         The get_videos_data_from_remaining_pages() method calls the earlier mentioned function and feeds it the URL.
         It gets video info from the remaining pages - we determined to have 10 pages, each page displaying 50 total 
         results - these results could be videos or video playlists. We are only interested in videos though. It's
         important to add data about the videos and channel in a json format, that's why we use dictionaries! Once we
         execute these two mentioned functions then we have the videos_data variable which is a dictionary that stored
         data about each video. Since it has their video ids, we use that info in the method
         get_data_about_each_video(). The video id for each video allows us to get into the page for each video and
         extract the statistics about each video.
    """

    def get_data_about_each_video(self):
        videos_data = self.get_videos_data_from_remaining_pages()
        for video_id in videos_data:
            single_video_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={self.API_KEY}"
            json_url = requests.get(single_video_url)
            single_video_data = json.loads(json_url.text)
            statistics = single_video_data['items'][0]['statistics']
            videos_data[video_id]['statistics'] = statistics
        self.videos_data = videos_data

    def get_videos_data_from_remaining_pages(self):
        videos_url = f"https://www.googleapis.com/youtube/v3/search?key={self.API_KEY}&channelId={self.channel_id}&part=snippet,id&order=date&maxResults=100"
        videos_data, next_page_token = self.get_videos_data_from_current_page(videos_url)
        count = 0
        while count < 10 and next_page_token is not None:
            next_page_url = videos_url + "&pageToken=" + next_page_token
            next_page_videos_data, new_next_page_token = self.get_videos_data_from_current_page(next_page_url)
            videos_data.update(next_page_videos_data)
            count += 1
        return videos_data

    def get_videos_data_from_current_page(self, videos_url):
        json_url = requests.get(videos_url)
        videos_data = json.loads(json_url.text)
        next_page_token = videos_data.get('nextPageToken',None)
        channel_videos = {}
        for video in videos_data['items']:
            if video['id']['kind'] == "youtube#video":
                video_id = video['id']['videoId']
                channel_videos[video_id] = {'videoTitle': video['snippet']['title'], 'publishedAt': video['snippet']['publishedAt']}
        self.channel_title = videos_data['items'][0]['snippet']['channelTitle']
        return channel_videos, next_page_token

    """
        create_json_file() method just takes the attributes we acquired with the methods above and turns them into
        a json file!
    """

    def create_json_file(self):
        if self.videos_data is None or self.channel_data is None:
            print("Couldn't get video/channel data!")
        json_format = {self.channel_id:{'channelData': self.channel_data, 'videosData': self.videos_data}}
        filename = self.channel_title.replace(" ", "_").lower() + '.json'
        with open(filename, 'w') as f:
            json.dump(json_format, f, indent=4)



