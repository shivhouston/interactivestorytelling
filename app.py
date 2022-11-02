from flask import *
from bs4 import BeautifulSoup

app = Flask(__name__)

character1_emotion = []
character2_emotion = []
character1_type = ""
character2_type = ""
willstoryloop = False


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload-image", methods=['GET', 'POST'])
def fileupload():
    global character1_emotion, character2_emotion, willstoryloop, character1_type, character2_type
    character1_dialogue = []
    character2_dialogue = []
    if request.method == 'POST':
        if request.files:
            xmlFile = request.files["image"]
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
                return render_template("storyediting.html", willstoryloop=willstoryloop,
                                       character1_type=character1_type,
                                       character2_type=character2_type, character1_dialogue=character1_dialogue,
                                       character1_emotion=character1_emotion, character2_dialogue=character2_dialogue,
                                       character2_emotion=character2_emotion)




@app.route('/', methods=['POST'])
def story():
    global character1_emotion, character2_emotion, willstoryloop, character1_type, character2_type
    character1_dialogue = []
    character2_dialogue = []
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


@app.route('/generate', methods=['POST'])
def generateXML():
    global character1_emotion, character2_emotion, willstoryloop, character1_type, character2_type
    data = request.get_json()
    character1_dialogue = data['x']
    character2_dialogue = data['y']
    print(character1_dialogue)
    print(character2_dialogue)

    soup = BeautifulSoup(features='lxml')

    mainStory = soup.new_tag("story")
    mainStory_Char1Type = soup.new_tag("type_of_character_one")
    mainStory_Char1Type.string = character1_type
    mainStory_Char2Type = soup.new_tag("type_of_character_two")
    mainStory_Char2Type.string = character2_type
    mainStory_DoesLoop = soup.new_tag("does_story_loop")
    mainStory_DoesLoop.string = str(willstoryloop)
    mainStory.append(mainStory_Char1Type)
    mainStory.append(mainStory_Char2Type)
    mainStory.append(mainStory_DoesLoop)
    soup.append(mainStory)

    print(len(character1_emotion))
    for i in range(len(character1_emotion)):
        curScene = soup.new_tag("scene")
        curScene_char1 = soup.new_tag("characterone")
        curScene_char2 = soup.new_tag("charactertwo")
        curScene_char1_emotion = soup.new_tag("emotion")
        curScene_char1_emotion.string = character1_emotion[i]
        curScene_char2_emotion = soup.new_tag("emotion")
        curScene_char2_emotion.string = character2_emotion[i]
        curScene_char1_dialogue = soup.new_tag("dialogue")
        curScene_char1_dialogue.string = character1_dialogue[i]
        curScene_char2_dialogue = soup.new_tag("dialogue")
        curScene_char2_dialogue.string = character2_dialogue[i]

        curScene_char1.append(curScene_char1_emotion)
        curScene_char2.append(curScene_char2_emotion)
        curScene_char1.append(curScene_char1_dialogue)
        curScene_char2.append(curScene_char2_dialogue)
        curScene.append(curScene_char1)
        curScene.append(curScene_char2)
        soup.append(curScene)

    with open("story.xml", "w") as file:
        file.write(soup.prettify())

    return send_file("story.xml", mimetype="text/xml", as_attachment=True, download_name="story.xml")


if __name__ == "__main__":
    app.run(debug=True, passthrough_errors=True)
