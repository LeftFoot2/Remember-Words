from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from remember_words_gui_template_1 import Ui_MainWindow
from add_word_window_1 import Ui_add_word_window
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.alphabet = ["a__________","b__________","c__________","d__________","e__________","f__________","g__________","h__________","i__________","j__________","k__________","l__________","m__________","n__________","o__________","p__________","q__________","r__________","s__________","t__________","u__________","v__________","w__________","x__________","y__________","z__________"]
        self.word_list = []


        # Buttons clicked
        self.ui.add_word_button.clicked.connect(self.add_word)
        self.ui.remove_word_button.clicked.connect(self.remove_word)



        # Load the words in from the word bank to the screen
        self.load_words()






    # Called if the 'add' button was pressed
    def add_word(self):
        self.add_win = QtWidgets.QMainWindow()
        self.add_ui = Ui_add_word_window()
        self.add_ui.setupUi(self.add_win)
        self.add_win.show()

        self.add_ui.add_word_line.returnPressed.connect(self.enter_pressed_add)
    
    # Called if the 'remove' button was pressed
    def remove_word(self):

        current_word = self.ui.word_bank.currentItem()

        # If the user didn't select a word than we don't
        # want to do anything.
        if current_word == None:
            pass

        else:
            self.delete_warning = QMessageBox()
            self.delete_warning.setWindowTitle("Warning: Deleting")
            self.delete_warning.setText(f'Are you sure you want to delete: "{current_word.text()}"')
            self.delete_warning.setIcon(QMessageBox.Warning)
            self.delete_warning.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            self.delete_warning.buttonClicked.connect(self.pop_buttons)

            self.delete_warning.exec_()
        





    def pop_buttons(self, answer):
        
        if answer.text() == '&Yes':
            
            current_row = self.ui.word_bank.currentRow()

            self.ui.word_bank.takeItem(current_row)

        elif answer.text() == '&No':
            pass
        else:
            pass

    


        
    def enter_pressed_add(self):
        self.word_list.append(self.add_ui.add_word_line.text()) # Pointless now. This will have to be a something that can be altered SQL?
        self.ui.word_bank.addItem(self.add_ui.add_word_line.text())
        self.ui.word_bank.sortItems()
        self.add_win.close()


    def load_words(self):
        # self.ui.word_bank.clear()
        self.ui.word_bank.addItems(self.alphabet)
        self.ui.word_bank.addItems(self.word_list)
        self.ui.word_bank.sortItems()



def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()