from tkinter import *
import sys
import os


def add_text():
   label1 = Label(
       root, text="You have entered the information to the Deadstock sneaker bot")
   label1.pack()


def run():
   os.system('/Users/arajkumar/Desktop/deadstock-bot/deadstock_bot.py')


root = Tk()
root.title("Deadstock Sneaker Bot")
root.geometry("500x500")
size_label = Label(root, text="SIZE")
size_label.pack()
size_text_box = Entry(root, bd=1)
size_text_box.pack()
url_label = Label(root, text="URL")
url_label.pack()
url_text_box = Entry(root, bd=1)
url_text_box.pack()
key_words_label = Label(root, text="KEY WORDS")
key_words_label.pack()
key_words_text_box = Entry(root, bd=1)
key_words_text_box.pack()
enter_button = Button(root, text="Run", command=run)
enter_button.pack()
root.mainloop()
