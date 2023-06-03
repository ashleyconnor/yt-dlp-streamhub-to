test:
	cp yt_dlp_plugins/extractor/streamhubto.py ~/Projects/yt-dlp/yt_dlp/extractor/
	cd ~/Projects/yt-dlp/ && python test/test_download.py TestDownload.test_StreamHubTo
	rm ~/Projects/yt-dlp/yt_dlp/extractor/streamhubto.py

.PHONY: test
