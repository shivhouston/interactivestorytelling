from hmmlearn import hmm
import numpy as np
from bs4 import BeautifulSoup
import random
from datetime import datetime
import csv

random.seed(datetime.now())

character1states = []
character2states = []

# Parallel arrays of the various character emotions and their corresponding image file names
images = np.array(["sinceresmile", "sad", "anger", "fear"])
emotions = np.array(["Happiness", "Sadness", "Anger", "Fear"])

# This array contains all the character image file names
characters = np.array(["duck", "frog", "octopus"])

# Default transition matrices for the two characters
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

# This function will take in the provided parameters for storylength, characterstate, characternum and define the character start state. This info is sent to hmm_model to create an array of emotions and that is returned to the user.
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

# This function will generate the array of emotions that is sent back to hmmGen.
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

# Converts a string state into an array. Each position in the transition matrices correspond to an emotion.
def statetoarray(state):
    if(state == "Happiness"):
        return np.array([1, 0, 0, 0])
    elif(state == "Sadness"):
        return np.array([0, 1, 0, 0])
    elif (state == "Anger"):
        return np.array([0, 0, 1, 0])
    elif (state == "Fear"):
        return np.array([0, 0, 0, 1])

# Same as statetoarray except using an index
def arr(index):
    if(index == 0):
        return np.array([1, 0, 0, 0])
    elif(index == 1):
        return np.array([0, 1, 0, 0])
    elif (index == 2):
        return np.array([0, 0, 1, 0])
    elif (index == 3):
        return np.array([0, 0, 1, 0])

# Converts index of an emotion to the string value of the specified emotion.
def numtoemotion(arr):
    global emotions
    output = []
    for x in range(len(arr)):
        output.append(emotions[arr[x]])
    return output

# Writes the XML file for the story generated.
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

        curScene_char1_proportion = soup.new_tag("proportion")
        curScene_char1_proportion.string = "50"
        curScene_char2_proportion = soup.new_tag("proportion")
        curScene_char2_proportion.string = "50"

        curScene_char1.append( curScene_char1_emotion )
        curScene_char2.append( curScene_char2_emotion )
        curScene_char1.append( curScene_char1_dialogue )
        curScene_char2.append( curScene_char2_dialogue )
        curScene_char1.append(curScene_char1_proportion)
        curScene_char2.append(curScene_char2_proportion)
        curScene.append( curScene_char1 )
        curScene.append( curScene_char2 )
        soup.append(curScene)

    file = open("story.xml", "w")
    file.write( soup.prettify() )


# CSV File Format
# <Row 1>
# <Row 2>
#
# Example
# 0.1, 0.3, 0.3, 0.3
# 0.1, 0.3, 0.3, 0.3
# 0.1, 0.3, 0.3, 0.3
# 0.1, 0.3, 0.3, 0.3

# Reads in the matrix.csv that is created from matrixGenerator.py
print("Reading in transition matrices from file...")
with open('matrix.csv') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    temp_array = []
    for row in csv_reader:
        print(row)
        if row[0] == "next":
            character1_transmat = np.array(temp_array)
            temp_array.clear()
            continue
        temp_array.append([float(n) for n in row])

    character2_transmat = np.array(temp_array)

# User can pick from the provided characters.
print("Available Characters: duck, frog, and octopus")
character1 = input("Enter character 1: ")
character2 = input("Enter character 2: ")

if(character1 not in characters or character2 not in characters):
    print("Invalid input")
    exit(0)

print()

# User can pick the orientation of which character faces what direction for the entirety of the story.
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

# User enters how many frames they want the story to be.
storylength = input("Enter length of story: ")
if(not (storylength.isdigit())):
    print("Invalid input")
    exit(0)
storylength = int(storylength)

print()

# User enters the starting emotions for the characters or can choose to let the transition matrices decide.
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

# User enters if they would like the story to loop or end after the last frame.
loop = input("Do you want the story to end on a loop, enter True or False: ")
if(not (loop == 'True' or loop == 'False')):
    print("Invalid input")
    exit(0)

# Use the provided information to generate the various emotions for both characters and convert them to string values.
character1states = hmmGen(storylength, character1state, 1)
character2states = hmmGen(storylength, character2state, 2)

character1states = numtoemotion(character1states)
character2states = numtoemotion(character2states)

# Write the xml file using the data created. This can then be put into the web application so that the dialogue and other information can be modified there.
write_story( character1, character2, loop )
"""
XML File will need to include
characters chosen
loop boolean
"""
