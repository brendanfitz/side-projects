import pyautogui
import time
import keyboard

#pyautogui.moveTo(X, Y, Seconds)
while True:
    pyautogui.moveTo(100, 100, 2) 
    pyautogui.moveTo(100, 200, 2) 

    if keyboard.is_pressed('Esc'):
        break