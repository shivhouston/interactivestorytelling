from flask import Flask, request, render_template, make_response, abort
import os
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.xml']
app.config['UPLOAD_PATH'] = 'uploads'

@app.route("/")
def index():
    if request.method == 'POST':
        xmlFile = request.form.get('xmlFile')
        return redirect(url_for('story', xmlFile=xmlFile))
    return render_template("index.html")


@app.route('/', methods=['POST'])
def story():
    character1_emotion = []
    character2_emotion = []
    character1_dialogue = []
    character2_dialogue = []
    xmlFile = request.form.get('xmlFile', None)
    soup = BeautifulSoup(xmlFile,'lxml')
    scenes = soup.find_all('scene')
    for scene in scenes:
        emotions = scene.find_all('emotion')
        character1_emotion.append(emotions[0].get_text()[4:-3])
        character2_emotion.append(emotions[1].get_text()[4:-3])
        dialogues = scene.find_all('dialogue')
        character1_dialogue.append(dialogues[0].get_text()[4:-3])
        character2_dialogue.append(dialogues[1].get_text()[4:-3])
    print(character1_emotion)
    print(character1_dialogue)
    print(character2_emotion)
    print(character2_dialogue)
    return render_template("story.html", character1_dialogue = character1_dialogue, character1_emotion = character1_emotion, character2_dialogue = character2_dialogue, character2_emotion=character2_emotion)


if __name__ == "__main__":
    app.run(debug=True, passthrough_errors=True)

