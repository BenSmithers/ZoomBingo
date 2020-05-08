import sys
import os
from random import randint

from board import Ui_MainWindow

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication

word_file = os.path.join(os.path.dirname(__file__), "phrases.dat")

# this returns a function that disables the button at (x,y) 
# needs to be outside the main class for proper scoping of the "disable" function 
def get_disable_function( what, x, y):
    def disable():
        what.ui.buttons[x][y].setEnabled(False)
    return( disable )

class main_gui(QMainWindow):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        file_obj = open(word_file, 'r')
        self.phrases = file_obj.readlines()
        file_obj.close()
        print("Loaded {} phrases".format(len(self.phrases)))
        if len(self.phrases)<24:
            raise Exception("Insufficient phrases! {}".format(len(self.phrases)))

        self.assign()

        # Buttons simply disable themselves when pressed         
        for x in range(self.ui.x_dim):
            for y in range(self.ui.y_dim):
                self.ui.buttons[x][y].clicked.connect(get_disable_function(self,x,y) )

        self.ui.pushButton.clicked.connect(self.assign)

    def add_line_breaks(self, what):
        working = what.split(" ")
        freq = 2
        n_linebreaks = int(len(working)/freq)

        for i in range(n_linebreaks):
            working.insert(freq*(i+1) + i ,'\n' )

        working = " ".join(working)
        return(working)
    

    def assign(self):
        # make a new list of phrases from which to sample
        phrase_copy = [phrase for phrase in self.phrases]

        for x in range(self.ui.x_dim):
            for y in range(self.ui.y_dim):
                if x==2 and y==2:
                    self.ui.buttons[x][y].setText("Free \n Space!")
                else:
                    if len(phrase_copy)==1:
                        which = 0
                    else:
                        which = randint( 0, len(phrase_copy)-1)
                    self.ui.buttons[x][y].setText( self.add_line_breaks(phrase_copy[which]) ) 
                    phrase_copy.pop(which)

                    self.ui.buttons[x][y].setEnabled(True)


app = QApplication(sys.argv)
app_instance = main_gui()

if __name__=="__main__":
    app_instance.show()
    sys.exit(app.exec_())
