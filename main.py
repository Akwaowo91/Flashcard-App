from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
french_word = {}

# READ FILE
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    french_word = original_data.to_dict(orient="records")
else:
    french_word = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer, french_word
    window.after_cancel(flip_timer)
    current_card = random.choice(french_word)
    canvas.itemconfigure(language_text, text='French', fill="black")
    canvas.itemconfigure(word_text, text=current_card['French'], fill="black")
    canvas.itemconfigure(canvas_image, image=front_card_img)
    flip_timer = window.after(3000, func=translation)


def translation():
    canvas.itemconfigure(canvas_image, image=back_card_img)
    canvas.itemconfigure(language_text, text='English', fill="white")
    canvas.itemconfigure(word_text, text=current_card['English'], fill='White')


def right_button_press():
    french_word.remove(current_card)
    print(len(french_word))
    new_data = pandas.DataFrame(french_word)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, translation)

canvas = Canvas(width=800, height=526, highlightthickness=0)
front_card_img = PhotoImage(file="images/card_front.png")
back_card_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_card_img)
canvas.config(bg=BACKGROUND_COLOR)
canvas.grid(column=2, row=1, pady=50, columnspan=2)

# Question
language_text = canvas.create_text(400, 150, font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, font=("Arial", 60, "bold"))

# BUTTONS
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=right_button_press)
right_button.grid(column=3, row=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=2, row=2)

next_card()
# window.after(3000, translation)
# window.after_cancel(translation)
window.mainloop()
