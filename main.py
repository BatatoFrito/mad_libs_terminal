"""

This program is a Mad Libs game that is played through the terminal

"""

from pathlib import Path
import re
import os
import sys

def clear():
    os.system('cls')

def pause():
    os.system('pause')

# Sets up the templates.txt file, extracts the text and transforms it into a dict where the key values are the titles
def setup():
    PATH_LOCATION = Path(__file__).absolute().parent
    PATH_TEMPLATES = PATH_LOCATION / 'templates.txt'

    try:
        with open(PATH_TEMPLATES, 'r') as file:
            text_templates = file.read()
    except(FileNotFoundError):
        with open(PATH_TEMPLATES, 'w+') as file:
            file.write('Instructions: To add a new story, write in a new paragraph:\n'
                       '#[Title]Story text... (without the #)\n'
                       '(Attention: A title needs to have more than 1 character and has to be unique)\n'
                       '---------------------------------------------------------------------------------------------\n'
                       'To add word spots in your story, simply add 4 underlines where you want it to be.\n'
                       '#[Title]Story text ____... ____... (without the #)\n'
                       '---------------------------------------------------------------------------------------------\n'
                       'Word spots cannot be inside another word:\n'
                       '#[Title]Story te____xt... (without the #) <- Not Allowed\n'
                       '---------------------------------------------------------------------------------------------\n'
                       'Also, you can make a story become a comment simply by inserting # right before the title\n'
                       '---------------------------------------------------------------------------------------------\n'
                       '\n'
                       '[Example]Hey my ____ ____, this is a story example!\n'
                       'Very ____, no? ____!')
            file.seek(0)
            text_templates = file.read()

    # Regex patterns and a search for the texts
    text_pattern = re.compile(r'(?<!#)\[(.{2,}?)\](.*?)(?=\n\n|\Z)', flags=re.S) # Will search paragraphs that begins with [] and ends at \n\n
    text_search = re.findall(text_pattern, text_templates)

    text_dict = {}

    # Add every text and their titles to the dict
    for title, text in text_search:
        if title and text is not None:
            text_dict.update({title: text})
    
    return text_dict

# The Mad Libs part of the code
def play_story(text_dict: dict, story_choice: str):

    underline_pattern = re.compile(r'(\s+)(_{4})([\[\].,!?{}-]*\s*)') # Will search for underlines preceded by spaces

    # Will try to find a story with the title sent by the user, if not found will go back to the menu
    try:
        text_choice = text_dict[story_choice]
    except(KeyError):
        clear()
        print(f'Story named "{story_choice}" not found! Are you sure you wrote it correctly?\n')
        pause()
        return play_menu(text_dict)
        
    # If story doesn't have any _
    if not re.search(underline_pattern, text_choice):
        clear()
        print('Story does not have any words to add! (Add 4 underlines in any place on the text to add a word spot)\n')
        pause()
        return play_menu(text_dict)
    # Will keep looping until every single _, that is separated by spaces in the front and back, is replaced
    while re.search(underline_pattern, text_choice):
        clear()
        text_shown = re.sub(underline_pattern, r'\1\2 (Current word)\3', text_choice, count=1)
        print(text_shown)
        word = input('\nWhich word will you insert in the underlines? ')
        if word and not word.isspace():
            word = word.split(maxsplit=1)[0]
        word = f'\\1{word}\\3'
        text_choice= re.sub(underline_pattern, word, text_choice, count=1)
    
    # Prints out the complete story
    clear()
    print(f'Complete story:\n\n{text_choice}\n')
    pause()
    return menu(text_dict)

# The menu that shows up after you select the Play option
def play_menu(text_dict: dict):
    clear()
    
    # Goes back if there are no stories
    if not text_dict:
        print('The templates file is empty, try adding some stories\n')
        pause()
        return menu(text_dict)
    # For Loop that makes a list of the possible stories
    for title in text_dict.keys():
        print(f'-> [{title}]')
    story_choice = input('\nWrite the title of the story you want to use (or B to go back): ')
    if story_choice.upper() == 'B':
        return menu(text_dict)
    
    return play_story(text_dict, story_choice)

# The first menu
def menu(text_dict: dict):
    clear()
    print('Welcome to Mad Libs!\nWhat will you do?\n\n[P]lay [E]xit\n')
    menu_choice = input()

    # Play choice
    if menu_choice.upper() == 'P':
        return play_menu(text_dict)

    # Exit choice
    elif menu_choice.upper() == 'E':
        clear()
        print('Thanks for playing!')
        sys.exit()

    else:
        return menu(text_dict)
    
if __name__ == '__main__':    
    # Setup
    text_dict = setup()

    # Game loop
    menu(text_dict)