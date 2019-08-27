from tkinter import *

def add_text():
   label1 = Label(root, text="You have entered the information to the Deadstock sneaker bot")
   label1.pack()

root = Tk()
root.title("Deadstock Sneaker Bot")
root.geometry("450x165")
veh_reg_label = Label(root, text="SIZE")
veh_reg_label.pack()
veh_reg_text_box = Entry(root, bd=1)
veh_reg_text_box.pack()
distance_label = Label(root, text="URL")
distance_label.pack()
distance_text_box = Entry(root, bd=1)
distance_text_box.pack()
time_label = Label(root, text="KEY WORDS")
time_label.pack()
time_text_box = Entry(root, bd=1)
time_text_box.pack()
enter_button = Button(root, text="Enter", command=add_text)
enter_button.pack()
root.mainloop()