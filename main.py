import pandas
import random
from tkinter import *
from tkinter import messagebox
BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")
change_to_eng  = 0

try:
    data = pandas.read_csv("data/words_to_learn.csv")

except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
finally:
    data_dict = data.to_dict(orient="records")
    next_word = 0


def random_word():
    global next_word
    global change_to_eng
    next_word = random.randint(1, len(data_dict))
    back_card.grid_forget()
    front_card.grid(row=0, column=1, columnspan=3)
    front_card.itemconfig(language, text="French")
    try:
        front_card.itemconfig(word, text=data_dict[next_word]["French"])
    except IndexError:
        if len(data_dict) == 1:
            check_mark.config(state="disable")
            messagebox.showinfo(title="Congrats!", message="You've learn all of the words!")
        else:
            random_word()
    else:
        back_card.itemconfig(back_language, text="English")
        back_card.itemconfig(back_word, text=data_dict[next_word]["English"])
        change_to_eng = window.after(5000, change_english)

def know_word():
    global next_word
    global change_to_eng
    window.after_cancel(change_to_eng)
    if len(data_dict) == 1:
        check_mark.config(state="disable")
        messagebox.showinfo(title="Congrats!", message="You've learn all of the words!")
    try:
        if data_dict[next_word] in data_dict:
            data_dict.remove(data_dict[next_word])
            random_word()
            window.after_cancel(change_to_eng)
        else:
            random_word()
            window.after_cancel(change_to_eng)
    except IndexError:
        print("It failed")
    finally:
        random_word()
        window.after_cancel(change_to_eng)


def doesnt_word():
    to_learn = pandas.DataFrame(data_dict)
    to_learn.to_csv("data/words_to_learn.csv", index_label=False, index=False)
    random_word()


def change_english():
    front_card.grid_forget()
    back_card.grid(row=0, column=1, columnspan=3)


window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

# front flash card.

front_img = PhotoImage(file="images/card_front.png")
front_card = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_card.create_image(400, 265, image=front_img)
language = front_card.create_text((400, 150), text="", fill="black", font=LANGUAGE_FONT)
word = front_card.create_text((400,263), text=f"", fill="black", font=WORD_FONT)
front_card.grid(row=0, column=1, columnspan=3)

# X button
x_button_img = PhotoImage(file="images/wrong.png")
x_button = Button(image=x_button_img, highlightthickness=0, command=doesnt_word)
x_button.grid(row=1, column=1, pady=50)

# Check mark

check_mark_img = PhotoImage(file="images/right.png")
check_mark = Button(image=check_mark_img, highlightthickness=0, command=know_word)
check_mark.grid(row=1, column=3, pady=50)

# back card

back_img = PhotoImage(file="images/card_back.png")
back_card = Canvas(width=800, height=526, highlightthickness=0, background=BACKGROUND_COLOR)
back_card.create_image(400,265, image=back_img)
back_language = back_card.create_text((400, 150), text="", fill="white", font=LANGUAGE_FONT)
back_word = back_card.create_text((400, 263), text="", fill="white", font=WORD_FONT)


random_word()
window.mainloop()
