import os
import json


def create_folder_structure(lang: str):
    # Define the structure
    folders = [
        os.path.join(lang, 'in'),
        os.path.join(lang, 'resources'),
        os.path.join(lang, 'resources', 'initial_prompts'),
        os.path.join(lang, 'resources', 'target_words'),
        os.path.join(lang, 'utils')
    ]

    # Create the folders
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    # todo: create readme and config files


def get_related_words(lang: str) -> {}:
    if lang == 'en':
        return {}  # ps: add manually for now b.c. api doesn't provide ranking
    if lang == 'ru':
        with open(f"{lang}/resources/related_words.json", 'r', encoding='utf-8') as file:
            related_words = json.loads(file.read())
        # load related words
        return related_words


# create_folder_structure("ru")
