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
        'skip_download': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

def download_video(url):
    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    ydl_opts = {
        'outtmpl': filepath,
        'format': 'mp4'
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

            preview = info.get("url")
            thumbnail = info.get("thumbnail")
            title = info.get("title")

            return render_template(
                "index.html",
                preview=preview,
                thumbnail=thumbnail,
                title=title,
                original_url=url
            )
        except:
            return render_template("index.html", error="Link tidak valid!")

    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")

    filepath = download_video(url)

    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
