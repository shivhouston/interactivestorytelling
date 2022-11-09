import numpy as np

character_transmat = [[0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]]

file = open("matrix.csv", "w")

for x in range(2):
    for i in range(4):
        print("Current transition matrix for character " + str(x + 1))
        print("          Happiness Sadness Anger Fear")
        print("Happiness     " + str(character_transmat[0][0]) + "        " + str(character_transmat[0][1]) + "      " + str(character_transmat[0][2]) + "    " + str(character_transmat[0][3]))
        print("Sadness       " + str(character_transmat[1][0]) + "        " + str(character_transmat[1][1]) + "      " + str(character_transmat[1][2]) + "    " + str(character_transmat[1][3]))
        print("Anger         " + str(character_transmat[2][0]) + "        " + str(character_transmat[2][1]) + "      " + str(character_transmat[2][2]) + "    " + str(character_transmat[2][3]))
        print("Fear          " + str(character_transmat[3][0]) + "        " + str(character_transmat[3][1]) + "      " + str(character_transmat[3][2]) + "    " + str(character_transmat[3][3]))
        print("Enter the transition values for character " + str(x + 1) + " row " + str(i + 1) + " values separated by row: ")
        character_transmat[i] = [float(n) for n in input().split(" ")]
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