# app.py
from flask import Flask, render_template, request, jsonify
from pytubefix import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form['url']
        download_type = request.form.get('type', 'video')  # 'video' or 'audio'
        
        video = YouTube(url)
        
        if download_type == 'audio':
            stream = video.streams.get_audio_only()
        else:
            stream = video.streams.get_highest_resolution()
        
        stream.download()
        
        return render_template('success.html', 
                             title=video.title, 
                             thumbnail=video.thumbnail_url,
                             download_type=download_type)
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)