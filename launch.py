import sys # passing args. Not really used atm
import os # used to get the datafile's location 
from random import randint # randomly choose text

from board import Ui_MainWindow # UI

# various gui elements
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton

'''
Ben Smithers (benjamin.smithers@mavs.uta.edu)

~~~ I regret nothing ~~~

07 May 2020 
'''


# which phrases file to use
word_file = os.path.join(os.path.dirname(__file__), "phrases.dat")

def get_disable_function( button ):
    """
    Returns a function that disables the given button
    """
    if not isinstance(button, QPushButton):
        raise TypeError("Arg should be {}, not {}".format(QPushButton, type(button)))
    def disable():
        button.setEnabled(False)
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
        
        # assure we have enough phrases to make the bingo board
        if len(self.phrases)<(self.ui.x_dim*self.ui.y_dim):
            raise Exception("Insufficient phrases! {}".format(len(self.phrases)))

        # need to assign starting values to the buttons
        self.assign()

        # Need to assign a function to each button
        # buttons disable themselves when pressed. 
        for x in range(self.ui.x_dim):
            for y in range(self.ui.y_dim):
                self.ui.buttons[x][y].clicked.connect(get_disable_function(self.ui.buttons[x][y]))

        # assign function to reset button 
        self.ui.pushButton.clicked.connect(self.assign)

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
