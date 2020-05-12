import sys # passing args. Not really used atm
import os # used to get the datafile's location 
from random import randint # randomly choose text
from glob import glob # used to find all the phrase files

from board import Ui_MainWindow # UI
from about_gui import Ui_Dialog as bingo_gui

# various gui elements
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QDialog

'''
Ben Smithers (benjamin.smithers@mavs.uta.edu)

~~~ I regret nothing ~~~

07 May 2020 
'''

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
        self.phrase_files = glob(os.path.join(os.path.dirname(__file__) ,"*.dat"))
        print(os.path.dirname(__file__))
        print(self.phrase_files)
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
        bingo_notification.setAttribute( QtCore.Qt.WA_DeleteOnClose )
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
            file_name = os.path.join(os.path.dirname(__file__), "zoom phrases.dat")


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
