import webbrowser #This module provides a high-level interface to allow displaying Web-based documents to users
import pyperclip #Provides a cross-platform Python module for copying and pasting text to the clipboard.
import keyboard #This module allows to hook global events, register hotkeys, simulate key presses

def displayTranslate():
    """
    Opens browser window and displays the translate (ENG - > RUS) for the text from the clipboard using Google Translate
    """
    url = "https://translate.google.ru/#view=home&op=translate&sl=en&tl=ru&text="
    text = pyperclip.paste()
    webbrowser.open(url + text)

keyboard.add_hotkey('tab', lambda: displayTranslate())
keyboard.wait('esc')
