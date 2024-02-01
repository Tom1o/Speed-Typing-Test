import tkinter as tk
import random

font = 'Courier 20 bold'


def countdown_three():
    global countdown
    canvas.delete('all')
    canvas.create_text(200, 75, anchor='center', text='Test Starting In:\n        3', font=font)
    start_button.config(text='Stop', command=stop_test)
    start_button.place(x=240, y=250)
    window.focus()

    countdown = window.after(1000, countdown_two)


def countdown_two():
    global countdown
    canvas.delete('all')
    canvas.create_text(200, 75, anchor='center', text='Test Starting In:\n        2', font=font)
    countdown = window.after(1000, countdown_one)


def countdown_one():
    global countdown
    canvas.delete('all')
    canvas.create_text(200, 75, anchor='center', text='Test Starting In:\n        1', font=font)
    countdown = window.after(1000, start_test)


def start_test():
    global random_word_order, countdown, typed_words, typed_chars
    typed_words = []
    typed_chars = ''
    random_word_order = random.sample(WORDS, len(WORDS))
    canvas.delete('all')
    canvas.create_text(200, 75, anchor='center', text=random_word_order[0], font=font)

    window.bind('<KeyPress>', key_press)

    countdown = window.after(60000, check_score)


def stop_test():
    window.after_cancel(countdown)
    canvas.delete('all')
    canvas.create_text(200, 75, anchor='center', text='Speed Typing Test\nHow Fast can you type?', font=font)
    start_button.config(text='Start', command=countdown_three)
    window.bind('<KeyPress>', '')


def check_score():
    window.bind('<KeyPress>', '')
    canvas.delete('all')
    correct_words = 0
    correct_letters = 0
    incorrect_words = 0
    for n in range(len(typed_words)):
        if random_word_order[n] == typed_words[n]:
            correct_words += 1
            correct_letters += len(typed_words[n])
        else:
            incorrect_words += 1

    canvas.create_text(200, 75, anchor='center',
                       text=f'The test is over.\n\nYou typed at a rate of\n{correct_words} Words per min'
                            f'\nAt a rate of\n{correct_letters} Letters per min', font=font)


def print_typed_chars():
    global typed_words
    letter_position = 0
    current_word = random_word_order[len(typed_words)]
    starting_position = 200 - (5 * len(current_word))
    for letter in typed_chars:
        if letter_position > (len(current_word) - 1):
            canvas.create_text(starting_position + (letter_position * 12), 125, text=letter, font=font, fill='red')
        elif letter == current_word[letter_position]:
            canvas.create_text(starting_position + (letter_position * 12), 125, text=letter, font=font, fill='green')
        else:
            canvas.create_text(starting_position + (letter_position * 12), 125, text=letter, font=font, fill='red')
        letter_position += 1


def add_letter(key):
    global typed_chars, typed_words
    typed_chars += key.char
    print_typed_chars()


def space():
    global typed_chars, text
    typed_words.append(typed_chars)
    typed_chars = ''
    canvas.delete('all')
    text = canvas.create_text(200, 75, anchor='center', text=random_word_order[len(typed_words)], font=font)


def backspace():
    global typed_chars, typed_words, text
    if typed_chars == '':
        if len(typed_words) == 0:
            pass
        else:
            typed_chars = typed_words[-1]
            typed_words.pop(-1)
            canvas.delete('all')
            text = canvas.create_text(200, 75, anchor='center', text=random_word_order[len(typed_words)], font=font)
            print_typed_chars()
    else:
        canvas.delete('all')
        text = canvas.create_text(200, 75, anchor='center', text=random_word_order[len(typed_words)], font=font)
        typed_chars = typed_chars[0:(len(typed_chars) - 1)]
        print_typed_chars()


def key_press(key):
    if key.keysym == 'BackSpace':
        backspace()
    elif key.keysym == 'space':
        space()
    else:
        add_letter(key)


WORDS = []
with open('words.csv') as file:
    data = file.readlines()

for word in data:
    word = word.split('\n')[0].lower()
    WORDS.append(word)

typed_chars = ''
typed_words = []
random_word_order = []
countdown = None

window = tk.Tk()
window.minsize(500, 300)
window.title('Speed Typing Test')


canvas = tk.Canvas(window, width=400, height=150)
canvas.place(x=50, y=25)
text = canvas.create_text(200, 75, anchor='center', text='  Speed Typing Test\nHow Fast can you type?', font=font)

start_button = tk.Button(window, text='Start', command=countdown_three)
start_button.place(x=240, y=250)


window.mainloop()
