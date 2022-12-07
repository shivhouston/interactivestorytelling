import numpy as np
import random
from datetime import datetime

random.seed(datetime.now())

character_transmat = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

# Each column in the transition matrix will signify the states or emotions in the order Happiness, Sadness, Anger, Fear
# In the matrix, [0][0] will signify the probability that the character's emotional state will go from happy to happy
# In the matrix, [0][1] will signify the probability that the character's emotional state will go from happy to sad
# The probabilities for each state must add up to 1

file = open("matrix.csv", "w")

for i in range(4):
    for j in range(4):
        if(i == j):
            character_transmat[i][j] = random.randint(5, 10) / 10

for i in range(4):
    for j in range(4):
        if(i == j):
            continue
        else:
            character_transmat[i][j] = random.randint(0, 4) / 10
            while (sum(character_transmat[i]) > 1):
                character_transmat[i][j] = random.randint(0, 4) / 10
    while (round(sum(character_transmat[i]), 1) != 1):
        character_transmat[i][3] = random.randint(0, 10) / 10
storecharacter_transmat = character_transmat

for x in range(2):
    for i in range(4):
        character_transmat = storecharacter_transmat
        print("Current transition matrix for character " + str(x + 1))
        print("          Happiness Sadness Anger Fear")
        print("Happiness     " + str(character_transmat[0][0]) + "        " + str(character_transmat[0][1]) + "      " + str(character_transmat[0][2]) + "    " + str(character_transmat[0][3]))
        print("Sadness       " + str(character_transmat[1][0]) + "        " + str(character_transmat[1][1]) + "      " + str(character_transmat[1][2]) + "    " + str(character_transmat[1][3]))
        print("Anger         " + str(character_transmat[2][0]) + "        " + str(character_transmat[2][1]) + "      " + str(character_transmat[2][2]) + "    " + str(character_transmat[2][3]))
        print("Fear          " + str(character_transmat[3][0]) + "        " + str(character_transmat[3][1]) + "      " + str(character_transmat[3][2]) + "    " + str(character_transmat[3][3]))
        print("Enter \"keep\" to store this current matrix or anything else to edit matrix: ")
        if(input() == "keep"):
            break
        print("Enter the transition values for character " + str(x + 1) + " row " + str(i + 1) + " values separated by row or continue to skip this row: ")
        string = input()
        if(string == "continue"):
            continue
        character_transmat[i] = [abs(float(n)) for n in string.split(" ")]
        rowsum = sum(character_transmat[i])
        for j in range(4):
            character_transmat[i][j] = round(character_transmat[i][j] / rowsum, 3)
        while(sum(character_transmat[i]) != 1):
            print(character_transmat[i])
            print("Invalid input, values must add up to 1")
            print("Enter the transition values for character" + str(x +1) + " row " + str(i + 1) + " values separated by row: ")
            character_transmat[i] = [float(n) for n in input().split(" ")]

    print("Current transition matrix for character " +  str(x + 1))
    print("          Happiness Sadness Anger Fear")
    print("Happiness     " + str(character_transmat[0][0]) + "        " + str(character_transmat[0][1]) + "      " + str(character_transmat[0][2]) + "    " + str(character_transmat[0][3]))
    print("Sadness       " + str(character_transmat[1][0]) + "        " + str(character_transmat[1][1]) + "      " + str(character_transmat[1][2]) + "    " + str(character_transmat[1][3]))
    print("Anger         " + str(character_transmat[2][0]) + "        " + str(character_transmat[2][1]) + "      " + str(character_transmat[2][2]) + "    " + str(character_transmat[2][3]))
    print("Fear          " + str(character_transmat[3][0]) + "        " + str(character_transmat[3][1]) + "      " + str(character_transmat[3][2]) + "    " + str(character_transmat[3][3]))

    for p in range(4):
        string = str(character_transmat[p][0]) + ", " + str(character_transmat[p][1]) + ", " + str(character_transmat[p][2]) + ", " + str(character_transmat[p][3]) + "\n"
        file.write(string)
    if(x == 0):
        file.write("next\n")

    print()
    print()
    print()

print("matrix.csv has been generated")
