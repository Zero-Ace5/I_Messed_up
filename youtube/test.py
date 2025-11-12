import yt_dlp

url = input("Enter YouTube URL: ").strip()

ydl_opts = {
    "ffmpeg_location": r"C:\ffmpeg\bin",   # <— force yt-dlp to use this path
    "format": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "outtmpl": "%(title)s.%(ext)s",
    "merge_output_format": "mp4",
    "postprocessor_args": ["-movflags", "faststart"],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    print(f"\nSaved and optimized for seeking: {ydl.prepare_filename(info)}")
