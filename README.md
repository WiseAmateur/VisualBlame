# VisualBlame

VisualBlame is a GUI that was created as part of my Bachelor's thesis. This thesis focused on researching how an overview of Git's data could help developers understand a codebase. The program shows 5 different kinds of data related to a line of code from the Git database. Screenshots of VisualBlame are shown below:

![Alt text](http://i.imgur.com/7Jf0ojw.png "After starting VisualBlame")

![Alt text](http://i.imgur.com/b4oeUOD.png "After performing a few actions")

## Installation
### Linux
VisualBlame has 2 main dependencies that have to be installed in order to run it. These are listed below with the websites where their installation instructions can be found:

- [pygit2](www.pygit2.org/install.html) (last tested version: 0.24.1)
- [kivy](https://kivy.org/docs/installation/installation.html) (last tested version: 1.9.1)

### Other operating systems
It has not been tried to run VisualBlame on other operating systems.

## Usage

After installing the dependencies, VisualBlame can be run with the command `python main.py <file_name>` (assuming you are in the project's directory). The `<file_name>` part has to be replaced with the location of the file you want to open the program with.

In VisualBlame there are multiple ways to get information. The main way of getting information is to click on a line in the left codeview. Besides that there are also the buttons, tabs and boxes that can be clicked in order to gain more information about specific files or commits.

## Codebase

VisualBlame's code consists mostly of the GUI code (gui/) on the one side and the Git modules code (modules/) on the other side. They communicate with each other through events, which go through the event manager (events.py). The GUI triggers events through this manager, which cause the scheduler (scheduler.py) to run the correct Git module in a new thread. Once the module is done, a new event is triggered and through this event the GUI will get the results. Lastly a very simple cache is used (cache.py) to make the program quicker when an action is repeated.

## Future plans

At the moment of writing this readme, I have no intentions to continue with this project. I have already invested a lot of time in it and want to move on to new projects. Should there be someone else who is interested in continuing this project, I am willing to help a little with this though.

## Potential improvements

The following potential features were responded well to in the user researches from the thesis:

- Showing more related files base on the contents of the line instead of based on the Git data.
- Opening the currently viewed file in the user's preferred editor.

The following potential improvements are quality of life or performance improvements:

- Making the text selectable.
- Improving the cache by giving it a limit and utilizing a replacement strategy.
- Improving the memory usage.