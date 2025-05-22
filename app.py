from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download-info", methods=["POST"])
def download_info():
    try:
        url = request.json.get("url")
        
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            formats = []
            for f in info['formats']:
                if f.get('resolution') and f.get('ext'):
                    formats.append({
                        'ext': f['ext'],
                        'resolution': f['resolution'],
                        'url': f['url']
                    })

            return jsonify({
                'title': info['title'],
                'formats': formats
            })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
