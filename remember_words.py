from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from remember_words_gui_template_1 import Ui_MainWindow
from add_word_window_1 import Ui_add_word_window
import sys
import sqlite3




conn = sqlite3.connect('word_bank.db')

cur = conn.cursor()

cur.execute("""CREATE TABLE if not exists words_list(word text)""")

conn.commit()

conn.close()


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.alphabet = ["a__________","b__________","c__________","d__________","e__________","f__________","g__________","h__________","i__________","j__________","k__________","l__________","m__________","n__________","o__________","p__________","q__________","r__________","s__________","t__________","u__________","v__________","w__________","x__________","y__________","z__________"]
        # self.word_list = []


        # Buttons clicked
        self.ui.add_word_button.clicked.connect(self.add_word)
        self.ui.remove_word_button.clicked.connect(self.remove_word)



        self.ui.search_bar.textEdited.connect(self.search)
  
      

        # Load the words in from the word bank to the screen
        self.load_words()



    def search(self):
        conn = sqlite3.connect('word_bank.db')

        cur = conn.cursor()

        cur.execute("SELECT * FROM words_list")
        word_record = cur.fetchall()
        
        conn.commit()

        conn.close()
        # self.ui.word_bank.clear()
        search_list =[]

        self.ui.word_bank.addItems(self.alphabet)

        for record in word_record:
            search_list.append(record)

        # print(search_list)
        cat ="asfsa"

        print(cat[1])
        
        print(len(self.ui.search_bar.text()))
        # filtered_results = filter(self.filtering, search_list)
        
        # for x in filtered_results:
        #     print(x)


    # def filtering(self, list_index):
        
    #     word = str(list_index[0])
    #     # if list_index[0][len(self.ui.search_bar.text())] == self.ui.search_bar.text():
    #     if word[1] == "aaaaaaaaaa":
    #         return True
    #     else:
    #         return False


        

        # for words in self.ui.word_bank:
        #     if words[0] == self.ui.search_bar.text():
        #         print('it workds')


    # Called if the 'add' button was pressed
    def add_word(self):
        self.add_win = QtWidgets.QMainWindow()
        self.add_ui = Ui_add_word_window()
        self.add_ui.setupUi(self.add_win)
        self.add_win.show()

        self.add_ui.add_word_line.returnPressed.connect(self.add_window_button)
        self.add_ui.adding_pushButton.clicked.connect(self.add_window_button)
        self.add_ui.cancel_add_pushButton.clicked.connect(self.close_window_button)


    
    def close_window_button(self):
        self.add_win.close()


    def add_window_button(self):
        ##### TODO ####
        # Add a way to varify that it is a valid word
        # aka no numbers or speshel charactors


        conn = sqlite3.connect('word_bank.db')

        cur = conn.cursor()

        cur.execute("INSERT INTO words_list VALUES (:word)",
        {
            'word': self.add_ui.add_word_line.text()
        }
        )
        self.ui.word_bank.addItem(self.add_ui.add_word_line.text())

        
        # self.word_list.append(self.add_ui.add_word_line.text()) # Pointless now. This will have to be a something that can be altered SQL?

        conn.commit()

        conn.close()


        self.ui.word_bank.sortItems()
        self.add_win.close()
    
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
            self.delete_warning.buttonClicked.connect(self.option_buttons)

            self.delete_warning.exec_()
        





    def option_buttons(self, answer):
        
        if answer.text() == '&Yes':

            current_row = self.ui.word_bank.currentRow()
            current_word = self.ui.word_bank.currentItem()

            self.ui.word_bank.takeItem(current_row)

            conn = sqlite3.connect('word_bank.db')

            cur = conn.cursor()

            delete_query = """DELETE FROM words_list WHERE word = ?"""

            cur.execute(delete_query, (current_word.text(),))

            conn.commit()

            conn.close()
            
            # current_row = self.ui.word_bank.currentRow()

            # self.ui.word_bank.takeItem(current_row)

        elif answer.text() == '&No':
            pass
        else:
            pass

    


        
        


    def load_words(self):



        conn = sqlite3.connect('word_bank.db')

        cur = conn.cursor()

        cur.execute("SELECT * FROM words_list")
        word_record = cur.fetchall()
        
        conn.commit()

        conn.close()
        # self.ui.word_bank.clear()

        self.ui.word_bank.addItems(self.alphabet)

        for record in word_record:
            self.ui.word_bank.addItems(record)


        self.ui.word_bank.sortItems()
        



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()