import sys # passing args. Not really used atm
import os # used to get the datafile's location 
from random import randint # randomly choose text
from glob import glob # used to find all the phrase files

from board import Ui_MainWindow # UI
from about_gui import Ui_Dialog as bingo_gui

# various gui elements
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QDialog

'''
Ben Smithers (benjamin.smithers@mavs.uta.edu)

~~~ I regret nothing ~~~

07 May 2020 
'''

# pyinstaller was being awful and wouldn't work. So I'm just transcribing the phrases directly into here
breengo = """Someone drops something
Naked ladies face down
Guns with stock vfx
Wife is either killed or commits suicide
Gratuitous stock footage
Pool party
Someone makes an unusual mistake
magic rock
Overly mean person
Death by the power of editing
Repurposed prop or location
Gratuitous blood
Fade effect
HACK THE PLANET
Evil businessman or government
Breen talking to himself
Braless ladies
Desert Driving
Badly edited death scene
Green screen effect
Neil Breen has magic
Fuck Laptops
Multiple Laptops
Neil Breen nutsack shot
Skull and/or skeleton
Weird laughing"""

breengo = breengo.split("\n")

neils = """Neil waits to the last minute to get food.
Andy mutes Neil so he gets food.
Drunk NPC
God-tier character randomly shows up.
Incompetent NPC
NPC acts out theme hyperbolicaly 
Something takes way longer than it should.
Loralie doesn't blink.
The Manta makes an appearance.
Freaking Pinewood. 
Loralie gets edgy.
Dom changes into a new outfit.
Loralie does/says something super evil.
A hero of time dies.
Sidequest to kill another god-tier entity.
Wander into something ridiculous. 
Good plan doesn't work. 
Good deed is punished.
Forced into a blind decision.
Critical Hit.
Critical Failure.
Neil says to roll a nonexistent skill. 
Loralie gets another song.
Loralie plays a song badly.
Alloryn flexes his goo knowledge. 
Alloryn is dumbfounded by stupidity.
"""

neils = neils.split("\n")

zoom = """Person asks "can you hear me?" before speaking.
Person has to ask "can you hear me?" twice before speaking.
Someone joins without realizing their camera is on.
Loud typing next to open mic. 
Someone can't figure out how to share their screen.
Emails and slack shared during presentation. 
Nobody has any questions after a presetation. 
Presenter goes over time. 
Presenter asks "can everyone see my screen?"
Presenter has to ask "can everyone see my screen?" twice
Presenter doesn't realize they're muted. 
Heavy breathing in open microphone.
Someone's open mic echoes another speaker. 
VERY LOUD PERSON.
very quiet person
Animation doesn't work.
Crying baby in the background. 
Someone else talking in the background. 
Someone says "in these trying times"
Person calls in from in bed.
Dog barks during call. 
Cat noises. 
Loud car noises. 
Someone yells Bingo! 
Someone on camera drinks coffee.
Someone on camera drinks alcohol. 
Raised hand goes ignored. 
Message in chat goes ignored. 
Presenter warned they are almost out of time.
Presenter warned they are way over time. 
Question is really more of a comment. 
Roboty voice.
Someone walks away while their camera stays on.
Weird camera angle at person's face.
"""

zoom = zoom.split("\n")

def write(filename, datas):
    obj = open(filename, 'w')
    for line in datas:
        obj.write(str(line))
        obj.write("\n")
    obj.close()

def copy_file(which, to_what):
    if not os.path.exists(which):
        raise IOError("File {} doesn't exist".format(which))

    if not os.path.abspath(to_what):
        raise IOError("Destination folder doesn't exist")

    
    old = open(which, 'r')
    new = open(to_what, 'w')

    for line in old.readlines():
        new.write(line)
    old.close()
    new.close()

def get_disable_function( board,x,y ):
    """
    Returns a function that disables the given button
    """
    if not isinstance(board, main_gui):
        raise TypeError("Arg should be {}, not {}".format(main_gui, type(board)))
    def disable():
        board.ui.buttons[x][y].setEnabled(False)
        board.check_bingo()
    return( disable )

class bingo_class(QDialog):
    def __init__(self,parent):
        super(bingo_class, self).__init__(parent)
        self.ui = bingo_gui()
        self.ui.setupUi(self)

class main_gui(QMainWindow):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.phrases = []

        # set up the save directory
        if sys.platform=='linux':
            basedir = os.path.join(os.path.expandvars('$HOME'),'.local','ZoomBingo')
        elif sys.platform=='darwin': #macOS
            basedir = os.path.join(os.path.expandvars('$HOME'),'ZoomBingo')
        elif sys.platform=='win32' or sys.platform=='cygwin': # Windows and/or cygwin. Not actually sure if this works on cygwin
            basedir = os.path.join(os.path.expandvars('%AppData%'),'ZoomBingo')
        else:
            raise NotImplementedError("{} is not a supported OS".format(sys.platform))
        if not os.path.exists(basedir):
            os.mkdir(basedir)
        self.phrase_dir = basedir

        if glob(os.path.join( self.phrase_dir, "*.dat"))==[]:
            # copy the pre-distributed phrases into the folder
            pre_installed = {"Neils Game.dat":neils, "zoom phrases.dat":zoom, "Breengo.dat":breengo}

            for each in pre_installed.keys():
                #copy_file(os.path.join("default_phrases",each), os.path.join(self.phrase_dir, each))
                write(os.path.join(self.phrase_dir, each), pre_installed[each])

        self.phrase_files = glob(os.path.join( self.phrase_dir, "*.dat"))
        

        phrase_names = [ os.path.basename(filepath).split(".")[0] for filepath in self.phrase_files ]
        for phrase in phrase_names:
            self.ui.comboBox.addItem(phrase)

        # laod file and assign button phrases 
        self.ui.comboBox.setCurrentIndex(0)
        self.load_phrases(True)

        # assure we have enough phrases to make the bingo board
        if len(self.phrases)<(self.ui.x_dim*self.ui.y_dim):
            raise Exception("Insufficient phrases! {}".format(len(self.phrases)))


        # Need to assign a function to each button
        # buttons disable themselves when pressed. 
        for x in range(self.ui.x_dim):
            for y in range(self.ui.y_dim):
                self.ui.buttons[x][y].clicked.connect(get_disable_function(self,x,y))

        # assign function to reset button 
        self.ui.pushButton.clicked.connect(self.assign)
        self.ui.comboBox.currentIndexChanged.connect(self.load_phrases)
        self.ui.comboBox.setCurrentIndex(1)
        self.ui.actionQuit.triggered.connect(self.exit)

        

    def exit(self):
        sys.exit()

    def bingo(self):
        bingo_notification = bingo_class(self)
        bingo_notification.setAttribute( Qt.WA_DeleteOnClose )
        bingo_notification.exec_()

    def check_bingo(self):
        # check rows and columns for bingo!
        for x in range(self.ui.x_dim):
            bingo = True
            for y in range(self.ui.y_dim):
                # if button still enabled, no bingo, so skip
                bingo = bingo and (not self.ui.buttons[x][y].isEnabled())
                if not bingo:
                    break
            if bingo:
                self.bingo()

        for y in range(self.ui.y_dim):
            bingo = True
            for x in range(self.ui.x_dim):
                bingo = bingo and (not self.ui.buttons[x][y].isEnabled())
                if not bingo:
                    break
            if bingo:
                self.bingo()
        
        # check diagonals for bingo
        if self.ui.x_dim == self.ui.y_dim:
            bingo = True
            other_bingo = True
            for xy in range(self.ui.x_dim):
                bingo = bingo and (not self.ui.buttons[xy][xy].isEnabled())
                other_bingo = other_bingo and (not self.ui.buttons[xy][self.ui.y_dim - xy - 1].isEnabled())
                if not (bingo or other_bingo):
                    break
            if bingo or other_bingo:
                self.bingo()

    def load_phrases(self, force=False):

        if not force:
            file_index = self.ui.comboBox.currentIndex()
            file_name = self.phrase_files[file_index]
        else:
            file_name = os.path.join( self.phrase_dir, "zoom phrases.dat")


        file_obj = open(file_name, 'r')
        self.phrases = file_obj.readlines()
        file_obj.close()
        print("Loaded {} phrases".format(len(self.phrases)))
        self.assign()

    def add_line_breaks(self, what):
        """
        Really simplistic method for adding line breaks to the phrases

        Returns passed string with linebreaks inserted 
        """
        if not isinstance(what, str):
            raise TypeError("Arg 'what' should be {}, got {}".format(str, type(what)))

        working = what.split(" ")
        freq = 2 # number of words before a linebreak 
        n_linebreaks = int(len(working)/freq)

        for i in range(n_linebreaks):
            working.insert(freq*(i+1) + i ,'\n' )

        working = " ".join(working)
        return(working)
    

    def assign(self):
        """
        Re-enables all the buttons and assigns new text to them. 
        """

        # make a new list of phrases from which to sample
        phrase_copy = [phrase for phrase in self.phrases]

        # get the coordinates of the Free space
        #    if even, no free space 
        if self.ui.x_dim%2 == 0:
            middle_x = -1
            # setting this to -1 so that no coordinate will match it, and so there is not free space 
        else:
            middle_x = (self.ui.x_dim-1)/2
        if self.ui.y_dim%2 ==0:
            middle_y = -1
        else:
            middle_y = (self.ui.y_dim-1)/2


        for x in range(self.ui.x_dim):
            for y in range(self.ui.y_dim):
                if x==middle_x and y==middle_y:
                    # skip the free space 
                    self.ui.buttons[x][y].setText("Free \n Space!")
                    self.ui.buttons[x][y].setEnabled(False)
                else:
                    if len(phrase_copy)==1:
                        which = 0
                    else:
                        which = randint( 0, len(phrase_copy)-1)
                    self.ui.buttons[x][y].setText( self.add_line_breaks(phrase_copy[which]) ) 

                    # make sure no phrase is assigned twice! 
                    phrase_copy.pop(which)

                    self.ui.buttons[x][y].setEnabled(True)


# instantiate and run the app
app = QApplication(sys.argv)
app_instance = main_gui()
if __name__=="__main__":
    app_instance.show()
    sys.exit(app.exec_())
