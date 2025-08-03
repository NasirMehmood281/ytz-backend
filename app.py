from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_video():
    data = request.json
    video_url = data.get('url')
    if not video_url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'format': 'bestvideo+bestaudio/best',
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        formats = []
        for f in info.get('formats', []):
            if f.get('url') and f.get('ext') in ['mp4', 'webm', 'm4a']:
                formats.append({
                    'format_id': f['format_id'],
                    'format_note': f.get('format_note', ''),
                    'ext': f['ext'],
                    'resolution': f.get('resolution') or f.get('height'),
                    'filesize': f.get('filesize'),
                    'url': f['url']
                })

        return jsonify({
            'title': info.get('title'),
            'thumbnail': info.get('thumbnail'),
            'formats': formats
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
