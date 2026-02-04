from flask import Flask, render_template, Response, jsonify
import gunicorn
from camera import *

app = Flask(__name__)

headings = ("Name","Album","Artist")
df1 = music_rec()
df1 = df1.head(15)
@app.route('/')

def index():
    # Assuming df1 contains columns: Name, Album, Artist
    df1['SpotifySearchLink'] = df1.apply(lambda row: f"https://open.spotify.com/search/?query={row['Name']}", axis=1)
    return render_template('index.html', headings=headings, data=df1.to_dict(orient='records'))
def gen(camera):
    while True:
        global df1
        frame, df1 = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/t')
def gen_table():
    return df1.to_json(orient='records')

if __name__ == '__main__':
    app.debug = True
    app.run()