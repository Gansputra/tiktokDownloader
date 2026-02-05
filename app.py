import os
import uuid
from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = "static/downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def get_tiktok_info(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

def download_video(url):
    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    ydl_opts = {
        'outtmpl': filepath,
        'format': 'mp4/bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filepath
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        try:
            info = get_tiktok_info(url)
            author_url = info.get("uploader_url")
            if not author_url and info.get("uploader_id"):
                author_url = f"https://www.tiktok.com/@{info.get('uploader_id')}"

            data = {
                "title": info.get("title", "TikTok Video"),
                "thumbnail": info.get("thumbnail"),
                "author": info.get("uploader", "Unknown Creator"),
                "author_url": author_url,
                "duration": info.get("duration_string", "00:00"),
                "views": f"{info.get('view_count', 0):,}",
                "likes": f"{info.get('like_count', 0):,}",
                "original_url": url
            }
            return render_template("index.html", video=data)
        except Exception as e:
            return render_template("index.html", error="Gagal mengambil data!")

    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    try:
        filepath = download_video(url)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return f"Error saat mendownload: {e}"

if __name__ == "__main__":
    app.run(debug=True)