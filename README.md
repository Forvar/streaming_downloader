# streaming_downloader

This is a simple script to download a streaming video. Here some instructions:

1. Make sure to install ffmpeg, this program needs it.
2. Get the .m3u8 url of the video. You can use the videodownloadhelper extension for that.
3. Start this script by doing:
<pre><code>python main.py <url></code></pre>

This script creates a folder in whitch it will download the .ts files. Once all the .ts files are downloaded, it merges them in a .mp4 file.
