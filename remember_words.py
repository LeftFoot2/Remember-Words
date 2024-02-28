from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
from remember_words_gui_template_1 import Ui_MainWindow
from add_word_window_1 import Ui_add_word_window
import sys
import sqlite3
import re
from pynput import keyboard
import threading
import time



input_string = ""

#######

# Note about the exe. I will need to clear it with companies to allow it to not be flagged as a virus.

# This is annoying because it isn't but it seems like a common problem at least with using pyinstaller.
######


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




        self.setWindowFlag(Qt.WindowStaysOnTopHint) #Makes the main window stay on top even after clicking off of it. This is essential because without it we wouldn't be able to see it when spelling.

           
        #Listens for keyboard interaction from the user.
        listener = keyboard.Listener(

            on_press=self.on_press)
        listener.start()
 


        self.alphabet = ["a__________","b__________","c__________","d__________","e__________","f__________","g__________","h__________","i__________","j__________","k__________","l__________","m__________","n__________","o__________","p__________","q__________","r__________","s__________","t__________","u__________","v__________","w__________","x__________","y__________","z__________"]

        self.alphabet_input_filter = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        self.new_word_indicators = ["~","`","!","@","#","$","%","^","&","*","(",")","+","=","/","Key.tab","Key.space","Key.left","Key.up","Key.down","Key.right","Key.enter","Key.home","Key.end","Key.page_up","Key.page_down","<",">",",",".","?","\\",":",";",'"',"[","]","{","}","|"]

        # Buttons clicked

        self.ui.add_word_button.clicked.connect(self.add_word)

        self.ui.remove_word_button.clicked.connect(self.remove_word)

        self.ui.search_bar.textEdited.connect(self.search)


        # Load the words in from the word bank to the screen
        self.load_words()


#*********************************************************************
#Next three functions have to deal with managing outside input.
#TODO#
#If user clicks away from the word than it needs to reset.
#TODO#
#If it would be great if it could tell if there are letters before
#the selection and be able to filter for that.


    def on_press(self,key):
        if not self.isActiveWindow():

            new_key = str(key).strip("'")

            # print(new_key)

            if new_key.lower() in self.alphabet_input_filter:
                self.filter_outside_letters(new_key)
            elif new_key in self.new_word_indicators:
                self.filter_outside_letters("")
            elif new_key == "Key.backspace":
                self.filter_outside_letters("Key.backspace")


    def filter_outside_letters(self, key):

        global input_string

        conn = sqlite3.connect('word_bank.db')

        cur = conn.cursor()

        cur.execute("SELECT * FROM words_list")

        word_record = cur.fetchall()
         
        conn.close()

        self.ui.word_bank.clear()

        print(input_string)

        search_list = []

        if key.isalpha():
            input_string += key
        elif key == "":
            input_string = ""
        elif key == "Key.backspace":
            input_string = input_string[:-1]

        for record in word_record:
            search_list.append(record[0]) 

        if input_string == "":
            self.ui.word_bank.clear()
            self.load_words()


        self.filter_inputs(search_list,input_string)
      

    def filter_inputs(self, search_list, input_string):
        
        for word in search_list:
           
            if re.match(input_string, word, re.IGNORECASE): 
                self.ui.word_bank.addItem(word) 

        if len(self.ui.word_bank) == 0:
            self.ui.word_bank.addItem("No results found.")

#**********************************************************************


#*********************************************************************
#Next two functions have to deal with managing the search bar.

    # This function is in charge of making the search bar work.
    def search(self):
        
        # We first need to get the words that the user has put into the database. 
        conn = sqlite3.connect('word_bank.db')

        cur = conn.cursor()

        cur.execute("SELECT * FROM words_list")
        word_record = cur.fetchall()
        
        conn.close()
        self.ui.word_bank.clear()
        search_list =[]

        #This is what we get from the word_record. It is here to help me understand the
        #how to work with it.
        # word_record = ('aaaaaaaaaaaaaaaaaaaaa',), ('bat',), ('cat',), ('rat',), ('sat',), ('mat',), ('darn',)

        for record in word_record:

            search_list.append(record[0]) # Gets the word out of the tuple and makes a list of strings 

        search_reset = ["!","?",".",",",'"'," "]
        for letter in self.ui.search_bar.text():
            if letter in search_reset:
                self.ui.search_bar.clear()
                break
    

        #If we have nothing in the search bar than I want the whole list to be presented to the user.
        #We have to clear what the search has done so we don't repeat the words in the main list.

        if len(self.ui.search_bar.text()) == 0:

            self.ui.word_bank.clear()

            self.load_words()
        else:
            self.filtering(search_list)


    #This is the brains of the search bar 

    def filtering(self, search_list):
        

        for word in search_list:


            #TODO#

            #re.fullmatch(pattern, string, flags=0) potintaly use to determian if the whole word was spelled.

            if re.match(self.ui.search_bar.text(), word, re.IGNORECASE): #The re library's match starts from the beginning of the word and matches it, in this case, to what is in the search bar.

                self.ui.word_bank.addItem(word) 


        if len(self.ui.word_bank) == 0: #Let's the user know that what they have typed is not anywhere in there word bank.

            self.ui.word_bank.addItem("No results found.")

#**********************************************************************


#*********************************************************************
#Next three functions have to deal with the add button.

    # Called if the 'add' button was pressed

    def add_word(self):

        ##TODO##

        #Make it so that this closes if the main window closes.


        #Shows the add window.

        self.add_win = QtWidgets.QMainWindow()

        self.add_ui = Ui_add_word_window()

        self.add_ui.setupUi(self.add_win)

        self.add_win.setWindowFlag(Qt.WindowStaysOnTopHint) #Allows for the add window to show on top of main window.

        self.add_win.show()




        #Logic for the add window.

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


        conn.commit()

        conn.close()



        self.ui.word_bank.sortItems()
        self.add_win.close()
    
#*********************************************************************




#*********************************************************************
#Next two functions have to deal the remove button.


    # Called if the 'remove' button was pressed

    def remove_word(self):


        current_word = self.ui.word_bank.currentItem()


        # If the user didn't select a word than we don't

        # want to do anything.

        if current_word == None:

            pass


        else:

            self.delete_warning = QMessageBox()

            self.delete_warning.setWindowFlag(Qt.WindowStaysOnTopHint)#Allows for the remove window to show on top of main window.

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
            


        elif answer.text() == '&No':

            pass

        else:

            pass

#*********************************************************************
       



#*********************************************************************
#Loads words from the database. Used to set and reset the list that is
#shown.
    def load_words(self):


        conn = sqlite3.connect('word_bank.db')


        cur = conn.cursor()


        cur.execute("SELECT * FROM words_list")

        word_record = cur.fetchall()
        

        conn.commit()

        conn.close()


        #May take out in final.

        # self.ui.word_bank.clear()


        self.ui.word_bank.addItems(self.alphabet)


        for record in word_record:

            self.ui.word_bank.addItems(record)



        self.ui.word_bank.sortItems()
        
#*********************************************************************




def main():

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()



if __name__ == "__main__":

    main()