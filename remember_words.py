from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
from remember_words_gui_template_1 import Ui_MainWindow
from add_word_window_1 import Ui_add_word_window
from remove_word_window import Ui_remove_word_window
from add_large_window import Ui_add_many_window
from settings_remember_words import Ui_Settings
import sys
import sqlite3
import re
import os
from pynput import keyboard, mouse
import threading
import time
import pyttsx3
from PyDictionary import PyDictionary
from configparser import ConfigParser



#TODO#
# 
#
# 
#BUG#the following are a few known bugs
#hovering over words does not give the definitions for newly added words unto the list is reloaded
#
#definitions are not added when offline. if a word is added offline than it will have the None definition even after connecting to the internet
#try and fix that
#






dictionary = PyDictionary()
# print(dictionary.printMeanings())



input_string = ""

#######

# Note about the exe. I will need to clear it with companies to allow it to not be flagged as a virus.
# This is annoying because it isn't but it seems like a common problem at least with using pyinstaller.
######



#Create a database for the words if one doesn't already exist.
conn = sqlite3.connect('word_bank.db')

cur = conn.cursor()

cur.execute("""CREATE TABLE if not exists words_list(word text, definition text)""")

conn.commit()
conn.close()



class MainWindow(QMainWindow):


    def __init__(self):

        super(MainWindow, self).__init__()

        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon('book_icon.ico'))


        self.setWindowFlag(Qt.WindowStaysOnTopHint) #Makes the main window stay on top even after clicking off of it. This is essential because without it we wouldn't be able to see it when spelling.

        self.add_win = QtWidgets.QMainWindow()
        self.del_win = QtWidgets.QMainWindow()
        self.add_lar = QtWidgets.QMainWindow()
        self.set_win = QtWidgets.QMainWindow()

        self.add_win.setWindowIcon(QIcon('book_icon.ico'))
        self.del_win.setWindowIcon(QIcon('book_icon.ico'))
        self.add_lar.setWindowIcon(QIcon('book_icon.ico'))
        self.set_win.setWindowIcon(QIcon('book_icon.ico'))


        self.setAttribute(QtCore.Qt.WA_AlwaysShowToolTips, True)


        #Listens for keyboard interaction from the user.

        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

        mlistener = mouse.Listener(on_click=self.on_click)
        mlistener.start()
 

        self.ui.word_bank.itemDoubleClicked.connect(self.text_to_speech)

        self.alphabet = ["a__________","b__________","c__________","d__________","e__________","f__________","g__________","h__________","i__________","j__________","k__________","l__________","m__________","n__________","o__________","p__________","q__________","r__________","s__________","t__________","u__________","v__________","w__________","x__________","y__________","z__________"]

        # self.alphabet_input_filter = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        self.new_word_indicators = ["~","`","!","@","#","$","%","^","&","*","(",")","+","=","/","Key.tab","Key.space","Key.left","Key.up","Key.down","Key.right","Key.enter","Key.home","Key.end","Key.page_up","Key.page_down","<",">",",",".","?","\\",":",";",'"',"[","]","{","}","|"]

        self.config = ConfigParser()
        self.font_database = QFontDatabase()
        self.new_font = QFont()

        #Creates and ini file that will hold settings information. Only runs for first run of the program.
        try:
            self.config.read("settings.ini")
            self.config.getboolean("Default","default_alphabet")
            
        except:
            self.config["Default"]={}
            self.config["Default"]["default_alphabet"] = "True"
            self.config["Default"]["default_font_type"] = "Cascadia Mono Light"
            self.config["Default"]["default_font_size"] = "9"

            self.config["User_Settings"]={}
            self.config["User_Settings"]["user_alphabet"] = "True"
            self.config["User_Settings"]["user_font_type"] = "Cascadia Mono Light"
            self.config["User_Settings"]["user_font_size"]= "9"

            with open("settings.ini", "w") as file:
                self.config.write(file)

        self.ui.word_bank.setSelectionMode(QAbstractItemView.ExtendedSelection)  

        # Buttons clicked

        self.ui.add_word_button.clicked.connect(self.add_word)
        self.ui.remove_word_button.clicked.connect(self.remove_word)
        self.ui.search_bar.textEdited.connect(self.search)
        self.ui.actionSettings.triggered.connect(self.settings_window)
        self.ui.actionDownload_Database.triggered.connect(self.download_database)
        self.ui.actionUpload_Database.triggered.connect(self.upload_file)

        # self.contextMenuPolicy()


        self.ui.word_bank.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.ui.menuBar.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.ui.frame.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.reduce_action = QAction("Hide buttons and menu", self)
        self.expand_action = QAction("Show buttons and menu", self)
        self.reduce_action.triggered.connect(self.reduce_size)
        self.expand_action.triggered.connect(self.expand_size)
        self.ui.word_bank.addAction(self.expand_action)
        self.ui.word_bank.addAction(self.reduce_action)

        self.hide_menu = QAction("Hide Menu", self)
        self.hide_menu.triggered.connect(self.hide_menu_bar)
        self.ui.menuBar.addAction(self.hide_menu)
        
        self.hide_frame = QAction("Hide buttons", self)
        self.hide_frame.triggered.connect(self.hide_frame_fun)
        self.ui.frame.addAction(self.hide_frame)

        # Load the words in from the word bank to the screen
        self.load_words()




    def hide_menu_bar(self):
        self.ui.menuBar.hide()

    def hide_frame_fun(self):
        self.ui.frame.hide()


    def reduce_size(self):

        self.hide_menu_bar()
        self.hide_frame_fun()


    def expand_size(self):
        self.ui.menuBar.show()
        self.ui.frame.show()



#*********************************************************************
#Next four functions have to deal with managing outside input.
#TODO#
#When minimized nothing should happen.
#TODO#
#If it would be great if it could tell if there are letters before
#the selection and be able to filter for that.

    def on_press(self,key):

        if not self.isActiveWindow() and not self.add_win.isActiveWindow() and not self.del_win.isActiveWindow() and not self.add_lar.isActiveWindow() and not self.set_win.isActiveWindow():


            new_key = str(key).strip("'")


            # print(new_key)


            if new_key.isalpha():#lower() in self.alphabet_input_filter:
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

        search_list = []

        if key.isalpha():
            input_string += key
        elif key == "":
            input_string = ""
        elif key == "Key.backspace":
            input_string = input_string[:-1]

        for record in word_record:
            search_list.append((record[0],record[1])) 

        if input_string == "":
            self.ui.word_bank.clear()
            self.load_words()
        else:
            self.filter_inputs(search_list,input_string)
      
    def filter_inputs(self, search_list, input_string):
        

        for word, definition in search_list:
           
            if re.match(input_string, word, re.IGNORECASE): 
                self.ui.word_bank.addItem(word)
                for i in range(self.ui.word_bank.count()):
                    if self.ui.word_bank.item(i).text() == word:
                        word_tip = self.ui.word_bank.item(i)
                        word_tip.setToolTip(definition)


        if len(self.ui.word_bank) == 0:
            self.ui.word_bank.addItem("No results found.")

    def on_click(self,x, y, button, pressed):
        if not self.isActiveWindow() and not self.add_win.isActiveWindow() and not self.del_win.isActiveWindow() and not self.add_lar.isActiveWindow() and not self.set_win.isActiveWindow():
            
            if str(button) == "Button.left":   
                self.filter_outside_letters("")

            elif str(button) == "Button.right":
                pass 

            else:
                pass
    
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
        search_list = []
        def_list = []

        #This is what we get from the word_record. It is here to help me understand the
        #how to work with it.
        # word_record = ('aaaaaaaaaaaaaaaaaaaaa',), ('bat',), ('cat',), ('rat',), ('sat',), ('mat',), ('darn',)
        # print(word_record)
        for record in word_record:
            
            search_list.append((record[0],record[1])) # Gets the word out of the tuple and makes a list of strings 
            # def_list.append()


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
            self.filtering(search_list,def_list)

    #This is the brains of the search bar 

    def filtering(self, search_list, def_list):
        

        for word, definition in search_list:
            # print(f'in filter {type(word)}')

            print(word)
            print(definition)


            #TODO#

            #re.fullmatch(pattern, string, flags=0) potintaly use to determian if the whole word was spelled.

            if re.match(self.ui.search_bar.text(), word, re.IGNORECASE): #The re library's match starts from the beginning of the word and matches it, in this case, to what is in the search bar.


                self.ui.word_bank.addItem(word)
                for i in range(self.ui.word_bank.count()):
                    if self.ui.word_bank.item(i).text() == word:
                        word_tip = self.ui.word_bank.item(i)
                        word_tip.setToolTip(definition)
                # self.ui.word_bank.setToolTip(definition)



        if len(self.ui.word_bank) == 0: #Let's the user know that what they have typed is not anywhere in there word bank.

            self.ui.word_bank.addItem("No results found.")

#**********************************************************************



#*********************************************************************
#Next two functions have to deal with the add button.

    


#TODO#

# Add a way to verify that it is a valid words aka no numbers or special characters



# Called if the 'add' button was pressed

    def add_word(self):

        ##TODO#Not necessary but nice# 

        #Make it so that this closes if the main window closes.


        #Shows the add window.

        self.add_ui = Ui_add_word_window()
        self.add_ui.setupUi(self.add_win)

        self.add_win.setWindowFlag(Qt.WindowStaysOnTopHint) #Allows for the add window to show on top of main window.
        self.add_win.show()

        #Logic for the add window.
        self.add_ui.add_word_line.returnPressed.connect(self.add_single_or_many)
        self.add_ui.adding_pushButton.clicked.connect(self.add_single_or_many)
        self.add_ui.add_multiple.clicked.connect(self.add_many)
        self.add_ui.cancel_add_pushButton.clicked.connect(self.close_window_button)  
    

    def close_window_button(self):

        self.add_win.close()

#*********************************************************************




#*********************************************************************

#TODO#

#Make it possible to add more than one thing at a time.


    def add_many(self):

        self.add_many_ui = Ui_add_many_window()

        self.add_many_ui.setupUi(self.add_lar)

        self.add_lar.setWindowFlag(Qt.WindowStaysOnTopHint) #Allows for the add many window to show on top of main window.
        self.add_lar.show()

        self.add_many_ui.add_large_words.clicked.connect(self.add_single_or_many)
        self.add_many_ui.cancel_large_words.clicked.connect(self.cancel_large_button)

        self.add_win.close()



    def add_single_or_many(self):

        user_text = [] 
        user_words = []
        def_word_thread_list = []
        word = ""
        count = 0


        #This determines whether it is adding a single word from that window or many.
        #It does this by seeing if the add_win is active or not.
        if self.add_win.isActiveWindow():
            #To add many words I separated the the words into individual letters.
            #Since I combined both the many and the single addition functions
            #I need to treat the single as the same.

            for letter in self.add_ui.add_word_line.text():
                user_text.append(letter)
                if letter == " ":
                    break

        else:

            for letter in self.add_many_ui.large_add_box.toPlainText():
                user_text.append(letter)
        # else:


        for letters in user_text:
            count += 1

            #isalpha determines if the input was a letter.
            if letters.isalpha():
                word += letters
                #the count will equal the user_text aka the word when all the letters are added to the word string.
                if count == len(user_text):
                    user_words.append(word)
            else:
                if word == "":
                    pass
                else:
                    user_words.append(word)
                    word = ""



        conn = sqlite3.connect('word_bank.db')

        cur = conn.cursor()
        

        for add_words in user_words:
            dup = False
            dup_list = []


            cur.execute("SELECT word FROM words_list")
            word_record = cur.fetchall()

            #we don't want the user to be able to add duplicate words
            for record in word_record:
                dup_list.append(record[0])

            for word in dup_list:
                if word.lower() == add_words.lower():
                    dup = True

            if not dup:
                #inserting the word and a blank definition into the database
                cur.execute("INSERT INTO words_list VALUES (:word, :definition)",
                {
                    'word': add_words,
                    #the definition needs to be updated. This is done in separate threads because
                    #the manner of getting the definitions is slow and would cause the user to experience
                    #a great deal of lag.
                    'definition': "No definition"
                }
                )
                self.ui.word_bank.addItem(add_words)
                #threads for adding the definitions
                thread = threading.Thread(target=self.word_addition_definition, args=(add_words,))
                def_word_thread_list.append(thread)

                conn.commit()

        conn.close()

        
        for threads in def_word_thread_list:
            threads.start()

        self.ui.word_bank.sortItems()

        #since this can be either addition window we need to make sure we try and close the right one.
        if self.add_win.isActiveWindow():
            self.add_ui.add_word_line.clear()
            self.add_win.close()
        else:
            self.add_lar.close()


    def cancel_large_button(self):
        self.add_lar.close()


#*********************************************************************




#*********************************************************************

#Next three functions have to deal the remove button.


    # Called if the 'remove' button was pressed

    def remove_word(self):


        current_words = self.ui.word_bank.selectedItems()

        # print(current_words)


        # If the user didn't select a word than we don't
        # want to do anything.
        if current_words == []:
            pass

        else:

            word_list = ""
            self.del_ui = Ui_remove_word_window()
            self.del_ui.setupUi(self.del_win)

            self.del_win.setWindowFlag(Qt.WindowStaysOnTopHint) #Allows for the delete window to show on top of main window.
            self.del_win.show()

            for word in current_words:

                if word.text() in self.alphabet:
                    pass      

                    
                elif word_list == "":
                    word_list+=word.text()

                else:

                    word_list+=(f", {word.text()}")


            self.del_ui.delete_label.setText(f"Warning: You are about to delete - {word_list}")


            self.del_ui.yes_del_button.clicked.connect(self.del_window_button)
            self.del_ui.cancel_del_button.clicked.connect(self.close_del_window_button)



    def close_del_window_button(self):

        self.del_win.close()


    def del_window_button(self):


        current_words = self.ui.word_bank.selectedItems()

        word_list = []

        for word in current_words:
            word_list.append(word.text())

        # self.ui.word_bank.takeItem(current_row)

        conn = sqlite3.connect('word_bank.db')
        cur = conn.cursor()

        #delete all selected words
        for words in word_list:
            delete_query = """DELETE FROM words_list WHERE word = ?"""

            cur.execute(delete_query, (words,))

        conn.commit()
        conn.close()

        self.del_win.close()

        self.load_words()


#*********************************************************************




#*********************************************************************

#TODO#

#Text to speech and definition.

    def text_to_speech(self):
        #This is from a simple library that allows words to be read out load by the computer.
        engine = pyttsx3.init()

        engine.say(self.ui.word_bank.currentItem().text())

        engine.runAndWait()


    def word_addition_definition(self, word):

        #Retrieves the definition for the word
        
        word_def = dictionary.meaning(word)
        word_def_string = str(word_def)

        
        conn = sqlite3.connect('word_bank.db')
        cur = conn.cursor()

        #The definition will be set for the correct words do to the WHERE clause.
        cur.execute("UPDATE words_list SET definition=:definition WHERE word=:word", 
        {
            'definition': word_def_string,
            'word': word

        })

        conn.commit()

        conn.close()


#*********************************************************************



#*********************************************************************
#TODO#
#Ability to change settings.

    def settings_window(self):

        self.set_ui = Ui_Settings()
        self.set_ui.setupUi(self.set_win)

        #Retrieves fonts to choose from and adds them to the drop down object in the settings
        for fonts in self.font_database.families():
            self.set_ui.font_change.addItem(fonts)

        self.config.read("settings.ini")
        
        #Following few lines allow for the settings to be the same way they set it up
        #the next time the user goes back to look at them.
        if self.set_ui.alphabet_toggle.isChecked() != self.config.getboolean("User_Settings","user_alphabet"):
            self.set_ui.alphabet_toggle.setChecked(self.config.getboolean("User_Settings","user_alphabet"))

        if self.set_ui.font_size.value() != int(self.config["User_Settings"]["user_font_size"]):
            self.set_ui.font_size.setValue(int(self.config["User_Settings"]["user_font_size"]))
        
        self.set_ui.font_change.setCurrentIndex(self.set_ui.font_change.findText(self.config["User_Settings"]["user_font_type"]))



        self.set_win.setWindowFlag(Qt.WindowStaysOnTopHint) #Allows for the window to show on top of other windows.
        self.set_win.show()

        #activation listeners
        self.set_ui.save_changes.clicked.connect(self.save_settings)
        self.set_ui.default_changes.clicked.connect(self.default_settings)
        self.set_ui.cancel_changes.clicked.connect(self.close_settings)



    def save_settings(self):
        self.config.read("settings.ini")

        #if any of the settings where changed and the user saved them than this will set those
        #settings
        self.config["User_Settings"]["user_alphabet"]=str(self.set_ui.alphabet_toggle.isChecked())
        self.config["User_Settings"]["user_font_type"]=self.set_ui.font_change.currentText()
        self.config["User_Settings"]["user_font_size"]=str(self.set_ui.font_size.value())

        with open("settings.ini", "w") as file:
            self.config.write(file)

        #reloading the list lets the changes made to the settings be shown immediately 
        self.load_words()

        self.set_win.close()


    def default_settings(self):
        self.config.read("settings.ini")

        #the settings that are used are always the user ones, but we have default settings that
        #the users revert back to by setting the user settings to the default settings.
        self.config["User_Settings"]["user_alphabet"]=str(self.config.getboolean("Default","default_alphabet"))
        self.config["User_Settings"]["user_font_type"]=self.config["Default"]["default_font_type"]
        self.config["User_Settings"]["user_font_size"]=self.config["Default"]["default_font_size"]

        with open("settings.ini", "w") as file:
            self.config.write(file)

        self.load_words()
        self.set_win.close()

    def close_settings(self):
        self.set_win.close()

#*********************************************************************


#*********************************************************************
#TODO#
#Download and upload lists might be easiest to just make a txt file that can be written to and read by the program.
    def download_database(self):
        conn = sqlite3.connect('word_bank.db')
        cur = conn.cursor()
        cur.execute("SELECT word FROM words_list")
        word_record = cur.fetchall()
        conn.close()

        save_name = QFileDialog.getSaveFileName(self, "Save File", "","Text (*.txt)")#learned you had to have the * from AI
        try:#This is needed because unless I click save it crashes. I'm not sure why.
            file_name = open(save_name[0],"w")
            for words in word_record:
                file_name.write(f"{words[0]},")
        except:
            pass
        

    def upload_file(self):
        open_name = QFileDialog.getOpenFileName(self, "Open File", "","Text (*.txt)")

        self.add_many_ui = Ui_add_many_window()

        self.add_many_ui.setupUi(self.add_lar)

        try:
            with open(open_name[0], "r") as f:
                file_lines = f.read()
                for words in file_lines:
                    self.add_many_ui.large_add_box.insertPlainText(words)

                self.add_single_or_many()
        except:
            pass

        

#*********************************************************************


#*********************************************************************
#TODO#
#Change color and style. #NOTE# This may be done solely in the designer.

#*********************************************************************


#*********************************************************************
#Loads words from the database. Used to set and reset the list that is
#shown.
    def load_words(self):
        
        conn = sqlite3.connect('word_bank.db')

        cur = conn.cursor()
        cur.execute("SELECT word, definition FROM words_list")

        word_record = cur.fetchall()

        #May take out in final.
        # conn.commit()

        conn.close()

        #May take out in final.
        self.ui.word_bank.clear()

        def_word_thread_list = []


        #add words to the visible list
        for record in word_record:
            self.ui.word_bank.addItem(record[0])

            #applies the definition to the words tooltip
            for i in range(self.ui.word_bank.count()):
                if self.ui.word_bank.item(i).text() == record[0]:
                    word_tip = self.ui.word_bank.item(i)
                    word_tip.setToolTip(f"{record[1]}")

                    if record[1] == "Reload with internet":

                        thread = threading.Thread(target=self.word_addition_definition, args=(record[0],))
                        def_word_thread_list.append(thread)

        for threads in def_word_thread_list:
            threads.start()

        #this is where the settings are applied to the application
        self.config.read("settings.ini")
        
        if self.config.getboolean("User_Settings","user_alphabet"):
            self.ui.word_bank.addItems(self.alphabet)

        self.new_font.setFamily(self.config["User_Settings"]["user_font_type"])
        self.new_font.setPointSize(int(self.config["User_Settings"]["user_font_size"]))
        self.ui.word_bank.setFont(self.new_font)

        self.ui.word_bank.sortItems()
        

#*********************************************************************





def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

if __name__ == "__main__":
    main()