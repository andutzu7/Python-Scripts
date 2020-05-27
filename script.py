import cv2
import keyboard  # using module# keyboard
import win32api, win32con
import time
from random import randrange
import pyautogui

messageArray = [':)', ':D', 'O_O', ':P']


def generate_message():
    text_length = randrange(3) + 1
    response = ""
    for i in range(0, text_length):
        entry = messageArray[randrange(len(messageArray))]
        if len(entry) > 1:
            if response != "":
                response += " "
            response += entry
            response += " "
        else:
            response += entry

    return response


def click_enter_comment_menu():
    try:
        buttonx, buttony = pyautogui.locateCenterOnScreen('comment.png', confidence=0.7)
        pyautogui.click(buttonx, buttony)
        return 1
    except TypeError:
        return -1


def post_comment():
    var = generate_message()
    pyautogui.write(var, interval=0.5)
    pyautogui.press('enter')
    time.sleep(2)


def back_to_dash():
    try:
        buttonx, buttony = pyautogui.locateCenterOnScreen('back.png', confidence=0.7)
        pyautogui.click(buttonx, buttony)
        return 1
    except TypeError:
        return -1


def skip_current_post():
    safety = 0
    while pyautogui.locateCenterOnScreen('comment.png', confidence=0.6):
        safety += 1
        if safety == 25:
            break
        pyautogui.press('down')


def find_next_comment():
    badcode = True
    while badcode:
        pyautogui.press('down')
        if pyautogui.locateCenterOnScreen('comment.png', confidence=0.6):
            badcode = False


if __name__ == '__main__':
    while True:
        time.sleep(randrange(5))
        click_enter_comment_menu()
        # gucci am gasit butonu de comment
        post_comment()
        back_to_dash()
        skip_current_post()
        find_next_comment()

        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            print('You Pressed A Key!')
            break  # finishing the loop
