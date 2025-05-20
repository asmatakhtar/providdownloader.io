import os
from flask import Flask, render_template, request, redirect, send_file, flash
from yt_dlp import YoutubeDL
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        format_type = request.form.get("format")

        if not url:
            flash("Please enter a video or playlist URL.", "danger")
            return redirect("/")

        try:
            ydl_opts = {
                'format': 'bestaudio/best' if format_type == "mp3" else 'best',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }] if format_type == "mp3" else [],
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                if format_type == "mp3":
                    filename = os.path.splitext(filename)[0] + ".mp3"

            return send_file(filename, as_attachment=True)

        except Exception as e:
            flash(f"Download failed: {str(e)}", "danger")
            return redirect("/")

    return render_template("index.html")
