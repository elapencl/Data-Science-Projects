from youtube_data import YoutubeData

"""
    Get the Youtube API Key Token from the Google Developer site and choose a channel id from an artist you like.
    The easiest way to access the channel id is to open a video by the artist and then accessing their account through
    that video. Copy the channel id from their page URL. This is Britney Spears' channel id!
"""

API_KEY = 'AIzaSyAM9vit3nwzjhXfts40efb8FRi8Abwhu1Y'
youtube_channel_id = 'UCgffc95YDBlkGrBAJUHUmXQ'

youtube_object = YoutubeData(API_KEY,youtube_channel_id)
youtube_object.get_channel_data()
youtube_object.get_data_about_each_video()
youtube_object.create_json_file()
