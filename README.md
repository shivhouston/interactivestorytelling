# Hyperlink Markov Chain Models

The objectives of the project are as follows: view previous efforts to create hyperlinks via various mathematical methods, evaluate these methods into forming a specific approach such as Markov chains, create a procedure for classifying the websites and links as different components in the Markov model, and implement a coherent framework with nodes and edges to satisfy the goal of a hyperlinked Markov chain design.

### matrixGenerator.py

Generates a matrix using randomly generated values and/or user inputted values that can be imported into the storyGenerator.py in order to create various emotions and scenes.

### storyGenerator.py

Creates an XML file using the provided matrix that contains all the emotions and character settings. Runs entirely in the command line.
Begins by reading in the matrices provided by the MatrixGenerator. Asks the user to enter the two characters they would like to have in the story and their orientations. Then the user can enter a starting emotion for each character. Lastly, the user is asked if the story should loop. Afterwards, the code will take the user inputs and generate the emotions for each scene and character. Finally, the code will write out an XML file containing all the data provided by the user and generated by the Markov Model.

### Story Editor Website

https://interactivestorytelling.azurewebsites.net/

### app.py

Flask backend for the story editor website.

### templates

Contains the various .html files for the website

### static/characters

Contains all the images for the characters

## Sources

[Page Rank Model](https://web.mst.edu/~gosavia/page_rank_model.pdf)  
This page gives us more of an idea behind the mathematics of Markov models. The whole network is regarded as a finite state machine, where every state is perceived as a state.
- Every state has a 1 - d probability of returning to the restart state 0, which is essentially the landing page for a storyline.
- d is a chosen constant relating to how likely the surfer is to return to the restart state 0. (d is the probability of going to an actual page and 1-d is the probability of restarting)
- There is also a probability for moving from state to the non-restart state which is calculated by d / N, where N is the total number of webpages

[Link Prediction and Path Analysis Using Markov Chains](http://www9.thewebconf.org/w9cdrom/68/68.html)  
In this paper, the notion of probabilistic link prediction and path analysis using Markov chains is proposed and evaluated. This paper presents using Hidden Markov Models as a sort of page rank that will allow a user that accesses one webpage to move onto another webpage that is relevant and connected are predicted by the model.

[hmmlearn](https://hmmlearn.readthedocs.io/en/latest/)  
hmmlearn is a library for Python. The library is a set of algorithms for unsupervised learning and inference of Hidden Markov Models. 

[Hidden Markov Model HMM Implementation using Python](https://www.youtube.com/watch?v=mnGN9BUs0HI)  
This is a video walk-through implementing and using one of the python packages for Hidden Markov Models. This is a good starting point to understand how the code works and how it could be implemented in our situation.
