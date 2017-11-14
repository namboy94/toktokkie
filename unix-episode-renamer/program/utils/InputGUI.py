"""
GUI
Class that implements a simple GUI for entering data relevant to the files to be renamed

Created on June 9, 2015

@author Hermann Krumrey
@version 0.1
"""

#imports
from Tkinter import Tk, Entry, Button, Checkbutton, Label, StringVar

"""
The Main GUI Class
"""
class InputGUI(object):

    """
    Constructor fo the GUI
    """
    def __init__(self, configFile):
        self.configFile = configFile
        
    """
    starts the GUI
    """
    def guiStart(self):
        
        #Initialize GUI
        self.gui = Tk()
        self.gui.geometry("450x500+300+300")
        self.gui.title("Episode Renamer")
        self.gui.wm_resizable(False, False)
        
        #textbox variables
        showName = StringVar()
        firstEpisode = StringVar()
        lastEpisode = StringVar()
        directory = StringVar()
        directory.set(open(self.configFile, "r").readline())
        
        #Add objects to gui
        self.addLabel("Showname", 5, 5, 200, 40)
        self.addLabel("First Episode", 5, 50, 200, 40)
        self.addLabel("Last Episode", 5, 100, 200, 40)
        self.addLabel("Directory", 5, 150, 200, 40)
        self.addTextBox(showName, 250, 5, 200, 40)
        self.addTextBox(firstEpisode, 250, 50, 200, 40)
        self.addTextBox(lastEpisode, 250, 100, 200, 40)
        self.addTextBox(directory, 250, 150, 200, 40)
        
        self.addButton("Start Rename", 170, 300, 300, 50, self.start)
        
        
        #Start GUI
        self.gui.mainloop()
        
    """
    adds a button to the GUI
    @param text - the text to be displayed
    @param xPos - the x position in the window
    @param yPos - the y position in the window
    @param xSize - the width of the button
    @param ySize - the height of the button
    @param command - the function to be invoked when this button is pressed
    """
    def addButton(self, text, xPos, yPos, xSize, ySize, command):
        button = Button(self.gui, command=command, text=text)
        button.pack()
        button.place(x=xPos, y=yPos, width=xSize, height=ySize)
        
    """
    adds a textBox to the gui, which saves its content to a predefined variable
    @param variable - the variable to be used and displayed
    @param xPos - the x position in the window
    @param yPos - the y position in the window
    @param xSize - the width of the textBox
    @param ySize - the height of the textBox
    @param command - the function to be invoked when Enter is pressed
    """
    def addTextBox(self, variable, xPos, yPos, xSize, ySize):
        textBox = Entry(self.gui, textvariable=variable)
        textBox.pack()
        textBox.place(x=xPos, y=yPos, width=xSize, height=ySize)
        
    """
    adds a checkbox to the gui with the given parameters
    @param variable - the variable to be used
    @param text - the text to be displayed next to the checkbox
    @param xPos - the x position in the window
    @param yPos - the y position in the window
    @param xSize - the width of the checkBox
    @param ySize - the height of the checkBox
    @param command - the function to be invoked when the checkBox is pressed
    """
    def addCheckBox(self, variable, text, xPos, yPos, xSize, ySize, command):
        checkBox = Checkbutton(self.gui, command=command, text=text, variable=variable)
        checkBox.pack()
        checkBox.place(x=xPos, y=yPos, width=xSize, height=ySize)
        
    """
    adds a label to the GUI
    @param text - the text to be displayed by the label
    @param xPos - the x position in the window
    @param yPos - the y position in the window
    @param xSize - the width of the label
    @param ySize - the height of the label
    """
    def addLabel(self, text, xPos, yPos, xSize, ySize):
        label = Label(self.gui, text=text)
        label.pack()
        label.place(x=xPos, y=yPos, width=xSize, height=ySize)
        
    """
    adds a picture to the GUI
    @param image - the PhotoImage object containing the picture to be added
    @param xPos - the picture's x-position on the GUI
    @param yPos - the picture's y-position on the GUI
    @param xSize - the width of the picture
    @param ySize - the height of the picture
    """
    def addPictureLabel(self, image, xPos, yPos, xSize, ySize):
        label = Label(self.gui, image=image)
        label.pack()
        label.place(x=xPos, y=yPos, width=xSize, height=ySize)
        
    def start(self):
        print ""