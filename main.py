import re
import PySimpleGUI as sg
import requests


hman = [r"hman_photos\hman0.png",r"hman_photos\hman1.png",r"hman_photos\hman2.png",
    r"hman_photos\hman3.png",r"hman_photos\hman4.png",r"hman_photos\hman5.png",
    r"hman_photos\hman6.png",r"hman_photos\hman7.png",r"hman_photos\hman8.png",
    r"hman_photos\hman9.png",r"hman_photos\hman10.png"]

def randomWord():
    #return "samurai"
    try:   
        word_url = 'https://random-word-api.herokuapp.com/word'
        response = requests.get(word_url)
        word = response.json()[0]
        return word
    except requests.exceptions.RequestException:
        return "000"

def putWord(said_word):
    length = len(said_word) - 1
    out = "_ "*length
    out += "_"
    return out

def updateWord(said_word, letter, cur_state):
    indexes = [m.start() for m in re.finditer(letter,said_word)]
    for i in indexes:   
        list_cur_state = list(cur_state)
        list_cur_state[i*2] = letter
        cur_state = "".join(list_cur_state)
    return cur_state

def playAgain(x):
    if x == "Yes":
        window["-CHECK-"].update(disabled=True)
        window['-IN-'].update('',disabled=True)
        window["-WORD-"].update("")
        window["-USED-"].update("HERE LETTERS USED ALREADY:\n")
        return 1
    if x == "No":
        return 0


left_col = [[sg.Text("Tries left: "), sg.Text("10", key="-TRY-")],
    [sg.Button("START GAME", key="-START-")],
    [sg.In(font="Helvetica 20", size=(6,6), justification="center",
     disabled=True, enable_events=True, key='-IN-'),
    sg.Button("CHECK", key="-CHECK-", disabled=True)],
    [sg.Text("HERE LETTERS USED ALREADY:\n", pad=(5,100), key="-USED-")]]

right_col = [[sg.Text(" ", font='Helvetica 25', key="-WORD-")],
        [sg.Image(hman[10], key="-IMG-")]]

layout = [[sg.Text("HANGMAN", font="Helvetica 30", justification='center', size=(100,2))],
         [sg.HorizontalSeparator()],
         [sg.Column(left_col, element_justification="center", expand_x=True),
          sg.VerticalSeparator(),
          sg.Column(right_col, element_justification="center", expand_x=True)]]

window = sg.Window("the game", layout, size=(800,600))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if len(values['-IN-']) > 1:
        window.Element('-IN-').Update(values['-IN-'][:-1])

    if event == "-START-":
        window["-USED-"].update("HERE LETTERS USED ALREADY:\n")
        window["-CHECK-"].update(disabled=False)
        window.Element('-IN-').Update('')
        guess_word = randomWord()

        if guess_word == 'samurai':
            url = "https://bit.ly/3pJ4LAo"
            res = requests.get(url, stream=True)
            res.raw.decode_content = True
            sg.popup_timed(title="HINT ;)))))",image=res.raw.read(), auto_close_duration=0.2, button_type=5)

        tries = 10
        print(guess_word)

        if guess_word == '000':
            window["-WORD-"].update("SORRY TRY AGAIN")
            continue
        else:
            window["-IN-"].update(disabled=False)
            window["-WORD-"].update(putWord(guess_word))

    if event == "-CHECK-" and values["-IN-"] != "":
        window['-IN-'].update('')
        lettr = values["-IN-"].lower()
        used = window['-USED-'].get()

        if 96 > ord(lettr) or ord(lettr) > 123:
            sg.popup("THIS IS AN INVALID CHARACTER")
            continue

        if lettr not in used:
            used += f" {lettr}"
            window["-USED-"].update(used)
        else:
            sg.popup("LETTER ALREADY USED!!!")

        if lettr in guess_word:
            curr = window["-WORD-"].get()
            window["-WORD-"].update(updateWord(guess_word, lettr, curr))
        else:
            tries-=1
            window["-TRY-"].update(str(tries))
            window["-IMG-"].update(hman[tries])

    if "_" not in window["-WORD-"].get() and window["-WORD-"].get() != "":
        won = sg.popup_yes_no('YOU WON\nPLAY AGAIN??')
        if playAgain(won) == 0:
            break

    if tries == 0:
        window["-IMG-"].update(hman[tries])
        lost = sg.popup_yes_no("YOU LOST!\nPLAY AGAIN??")
        if playAgain(lost) == 0:
            break

window.close()
