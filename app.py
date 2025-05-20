from flask import Flask, render_template, request, send_file, redirect, url_for, after_this_request
import yt_dlp
import os
import uuid
import logging

app = Flask(__name__)

# Setup download folder and logging
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        file_format = request.form.get("format") or "mp4"

        if not url:
            return render_template("index.html")

        filename = str(uuid.uuid4())
        outtmpl = os.path.join(DOWNLOAD_FOLDER, f"{filename}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best' if file_format == 'mp3' else 'best',
            'outtmpl': outtmpl,
            'noplaylist': True,
            'merge_output_format': 'mp4' if file_format == 'mp4' else None,
            'postprocessors': []
        }

        if file_format == 'mp3':
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded_file = ydl.prepare_filename(info)

                if file_format == 'mp3':
                    downloaded_file = os.path.splitext(downloaded_file)[0] + ".mp3"

            @after_this_request
            def cleanup(response):
                try:
                    os.remove(downloaded_file)
                except Exception as e:
                    app.logger.error(f"Failed to delete file: {e}")
                return response

            return send_file(downloaded_file, as_attachment=True, download_name=os.path.basename(downloaded_file))
        except Exception as e:
            app.logger.error(f"Download error: {e}")
            return render_template("index.html")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
