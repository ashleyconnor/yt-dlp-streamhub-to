from yt_dlp.extractor.common import InfoExtractor


class StreamHubToIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?streamhub\.to/(?P<id>[a-z0-9]+)'
    _TESTS = [{
        'url': 'https://streamhub.to/81hzqbykjnsm',
        'md5': '6ad485cc1b6e53f132771c4c232ace69',
        'info_dict': {
            'id': '81hzqbykjnsm',
            'ext': 'ts',
            'title': 'Chhalla_Mud_Ke_Nahi_Aaya_2022_17844',
            'thumbnail': 'https://v808.streamhub.to/i/03/00018/81hzqbykjnsm.jpg',
            'uploader': 'fikrialarm88',
        }
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        title = self._html_search_regex(r'<h4>(.+?)<\/h4>', webpage, 'title')
        steaming_id = self._html_search_regex(r'urlset\|(.+?)\|hls', webpage, 'streaming_id')
        streaming_subdomain = self._html_search_regex(r'doPlay\|(.+?)\|displayCurrentQuality', webpage, 'streaming_subdomain')
        thumbnail_id = '/'.join(self._html_search_regex(r'jpg\|(.+?)\|poster', webpage, 'thumbnail').split('|')[::-1])
        thumbnail = f"https://{streaming_subdomain}.streamhub.to/i/{thumbnail_id}/{video_id}.jpg"
        media_url = f"https://{streaming_subdomain}.streamhub.to/hls/,{steaming_id},.urlset/master.m3u8"
        ext = "ts" # TODO: Check if it's always ts
        formats = []
        formats.extend(self._extract_m3u8_formats(media_url, video_id, ext, m3u8_id='hls', fatal=False))

        return {
            'id': video_id,
            'title': title,
            'thumbnail': thumbnail,
            'formats': formats,
            'uploader': self._search_regex(r'https:\/\/streamhub.to\/users\/(.+?)\"', webpage, 'uploader', fatal=False),
        }
