from hmmlearn import hmm
import numpy as np
from bs4 import BeautifulSoup
import random
from datetime import datetime

random.seed(datetime.now())

character1states = []
character2states = []
images = np.array(["sinceresmile", "sad", "anger", "fear"])
emotions = np.array(["Happiness", "Sadness", "Anger", "Fear"])
characters = np.array(["duck", "frog", "octopus"])

character1_startprob = np.array([0.2, 0.2, 0.2, 0.4])
character2_startprob = np.array([0.4, 0.2, 0.2, 0.2])

character1_transmat = np.array([[0.1, 0.3, 0.3, 0.3],
                                [0.2, 0.1, 0.5, 0.2],
                                [0.2, 0.1, 0.3, 0.4],
                                [0.2, 0.2, 0.2, 0.4]])

character2_transmat = np.array([[0.1, 0.3, 0.3, 0.3],
                                [0.2, 0.1, 0.5, 0.2],
                                [0.2, 0.1, 0.3, 0.4],
                                [0.2, 0.2, 0.2, 0.4]])

def hmmGen(storylength, characterstate, characternum):
    global character1_startprob, character2_startprob
    global character1_transmat, character2_transmat

    characterstartstate = []
    if(characternum == 1):
        if(characterstate == ""):
            characterstartstate = character1_startprob
        else:
            characterstartstate = statetoarray(characterstate)
        trans_matrix = character1_transmat
    else:
        if(characterstate == ""):
            characterstartstate = character2_startprob
        else:
            characterstartstate = statetoarray(characterstate)
        trans_matrix = character2_transmat

    output = hmm_model(characterstartstate, trans_matrix, storylength)
    return output


def hmm_model(start_prob, trans_matrix, length):
    model = hmm.GaussianHMM(n_components=4, covariance_type="full")
    model.startprob_ = start_prob
    model.transmat_ = trans_matrix
    model.means_ = np.array([[0.0,  0.0],
                             [0.0, 11.0],
                             [9.0, 10.0],
                             [11.0, -1.0]])
    model.covars_ = .5 * np.tile(np.identity(2), (4, 1, 1))
    X, Z = model.sample(length)
    return Z

def statetoarray(state):
    if(state == "Happiness"):
        return np.array([1, 0, 0, 0])
    elif(state == "Sadness"):
        return np.array([0, 1, 0, 0])
    elif (state == "Anger"):
        return np.array([0, 0, 1, 0])
    elif (state == "Fear"):
        return np.array([0, 0, 0, 1])

def arr(index):
    if(index == 0):
        return np.array([1, 0, 0, 0])
    elif(index == 1):
        return np.array([0, 1, 0, 0])
    elif (index == 2):
        return np.array([0, 0, 1, 0])
    elif (index == 3):
        return np.array([0, 0, 1, 0])

def numtoemotion(arr):
    global emotions
    output = []
    for x in range(len(arr)):
        output.append(emotions[arr[x]])
    return output


def write_story( typechar1, typechar2, doesloop ):
    global character1states, character2states
    soup = BeautifulSoup(features='lxml')

    mainStory = soup.new_tag("story")
    mainStory_Char1Type = soup.new_tag("type_of_character_one")
    mainStory_Char1Type.string = typechar1
    mainStory_Char2Type = soup.new_tag("type_of_character_two")
    mainStory_Char2Type.string = typechar2
    mainStory_DoesLoop = soup.new_tag("does_story_loop")
    mainStory_DoesLoop.string = doesloop
    mainStory.append(mainStory_Char1Type)
    mainStory.append(mainStory_Char2Type)
    mainStory.append(mainStory_DoesLoop)
    soup.append(mainStory)

    for i in range(len(character1states)):
        curScene = soup.new_tag("scene")
        curScene_char1 = soup.new_tag("characterone")
        curScene_char2 = soup.new_tag("charactertwo")
        curScene_char1_emotion = soup.new_tag("emotion")
        curScene_char1_emotion.string = character1states[i]
        curScene_char2_emotion = soup.new_tag("emotion")
        curScene_char2_emotion.string = character2states[i]
        curScene_char1_dialogue = soup.new_tag("dialogue")
        curScene_char1_dialogue.string = "null"
        curScene_char2_dialogue = soup.new_tag("dialogue")
        curScene_char2_dialogue.string = "null"

        curScene_char1.append( curScene_char1_emotion )
        curScene_char2.append( curScene_char2_emotion )
        curScene_char1.append( curScene_char1_dialogue )
        curScene_char2.append( curScene_char2_dialogue )
        curScene.append( curScene_char1 )
        curScene.append( curScene_char2 )
        soup.append(curScene)

    file = open("story.xml", "w")
    file.write( soup.prettify() )


print("Available Characters: duck, frog, and octopus")
character1 = input("Enter character 1: ")
character2 = input("Enter character 2: ")

if(character1 not in characters or character2 not in characters):
    print("Invalid input")
    exit(0)

print()

orientation = input("Enter 1 for Char 1 left and Char 2 right orientation or 2 for characters to be flipped: ")
if(not (orientation.isdigit())):
    print("Invalid input orientation")
    exit(0)
orientation = int(orientation)
if(not (orientation == 1 or orientation == 2)):
    print("Invalid input")
    exit(0)
if(orientation == 2):
    temp = character1
    character1 = character2
    character2 = temp

print()

storylength = input("Enter length of story: ")
if(not (storylength.isdigit())):
    print("Invalid input")
    exit(0)
storylength = int(storylength)

print()
print("Available Emotions: Happiness, Sadness, Anger, and Fear")
character1state = input("Enter character 1 starting state or leave blank for random generation: ")
character2state = input("Enter character 2 starting state or leave blank for random generation: ")

if(not (character1state in emotions or character1state == "")):
    print("Invalid input")
    exit(0)

if(not (character2state in emotions or character2state == "")):
    print("Invalid input")
    exit(0)

print()

loop = input("Do you want the story to end on a loop, enter True or False: ")
if(not (loop == 'True' or loop == 'False')):
    print("Invalid input")
    exit(0)


character1states = hmmGen(storylength, character1state, 1)
character2states = hmmGen(storylength, character2state, 2)

character1states = numtoemotion(character1states)
character2states = numtoemotion(character2states)

write_story( character1, character2, loop )
"""
XML File will need to include
characters chosen
loop boolean


"""