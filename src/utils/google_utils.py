import re
from googleapiclient.discovery import build

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..')))
from configs import API_YOUTUBE_KEY

class YoutubeAPIUtils:
    parts_default = ["snippet", "status", "contentDetails", "liveStreamingDetails"]

    def __init__(self, api_key=None):
        self.api_key = api_key
        if self.api_key is None:
            self.api_key = API_YOUTUBE_KEY

    def get_youtube_videos_request_url(self, id_list, parts=None, key=None):
        """
        生成 YouTube API 視頻請求的 URL。

        :param id_list: 視頻的 ID 列表
        :param parts: 指定要擷取的視頻部分，預設為類別中的默認部分，可以為 None
        :param key: YouTube API 的開發者金鑰，可以為 None

        :return: YouTube API 視頻請求 URL。
        """
        if parts is None:
            parts = self.parts_default
        if key is None:
            key = self.api_key

        video_ids = ",".join(id_list) if isinstance(id_list, list) else id_list
        requested_parts = ",".join(parts) if isinstance(parts, list) else parts

        return f"https://www.googleapis.com/youtube/v3/videos?part={requested_parts}&id={video_ids}&key={key}&alt=json"

    def get_youtube_videos_response_item_text(self, id_list, parts=None, key=None):
        """
        獲取 YouTube 視頻的 item text

        :param id_list: 視頻的 ID 列表
        :param parts: 指定要擷取的視頻部分，預設為類別中的默認部分，可以為 None
        :param key: YouTube API 的開發者金鑰，可以為 None

        :return: 視頻的 item text
        """
        if parts is None:
            parts = self.parts_default
        if key is None:
            key = self.api_key

        video_ids = ",".join(list(id_list))
        requested_parts = ",".join(list(parts))

        youtube = build('youtube', 'v3', developerKey=key)
        response = youtube.videos().list(
            id=video_ids,
            part=requested_parts
        ).execute()
        items = response.get('items', [])

        return items
    
def get_youtube_id_with_url(url):
    id = re.search(r'v=(.*?)(&|$)', url) or re.search(r'youtu.be/(.*?)(&|$)', url)
    if id:
        return id.group(1)
    return ""

if __name__ == "__main__":
    id = "h0LN2aG05o0"

    youtube = YoutubeAPIUtils()
    print(youtube.get_youtube_videos_request_url(id))