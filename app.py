from flask import *
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def story():
    character1_emotion = []
    character2_emotion = []
    character1_dialogue = []
    character2_dialogue = []
    character1_type = ""
    character2_type = ""
    willstoryloop = False
    xmlFile = request.form.get('xmlFile')
    soup = BeautifulSoup(xmlFile, 'lxml')
    character1_type = soup.find('type_of_character_one').text.strip()
    character2_type = soup.find('type_of_character_two').text.strip()
    willstoryloop = eval(soup.find('does_story_loop').text.strip())
    scenes = soup.find_all('scene')
    print(len(scenes))
    for scene in scenes:
        emotions = scene.find_all('emotion')
        character1_emotion.append(emotions[0].get_text()[5:-4])
        character2_emotion.append(emotions[1].get_text()[5:-4])
        dialogues = scene.find_all('dialogue')
        character1_dialogue.append(dialogues[0].get_text()[5:-4])
        character2_dialogue.append(dialogues[1].get_text()[5:-4])
    print(willstoryloop)
    print(character1_type)
    print(character2_type)
    print(character1_emotion)
    print(character1_dialogue)
    print(character2_emotion)
    print(character2_dialogue)
    if request.form['action'] == 'View Story':
        return render_template("story.html", willstoryloop=willstoryloop, character1_type=character1_type,
                               character2_type=character2_type, character1_dialogue=character1_dialogue,
                               character1_emotion=character1_emotion, character2_dialogue=character2_dialogue,
                               character2_emotion=character2_emotion)
    elif request.form['action'] == 'Edit Story':
        return render_template("storyediting.html", willstoryloop=willstoryloop, character1_type=character1_type,
                               character2_type=character2_type, character1_dialogue=character1_dialogue,
                               character1_emotion=character1_emotion, character2_dialogue=character2_dialogue,
                               character2_emotion=character2_emotion)


if __name__ == "__main__":
    app.run(debug=True, passthrough_errors=True)
