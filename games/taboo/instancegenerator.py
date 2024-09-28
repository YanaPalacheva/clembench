"""
This script generates game instances for the taboo game.

Creates a JSON file (instances.json) in ./in/{language code}

Tip: prettify the resulting JSON with
    Windows/Linux: Press Ctrl + Alt + L.
    macOS: Press Cmd + Option + L.
"""
import os
import random

from tqdm import tqdm

import clemgame
from clemgame.clemgame import GameInstanceGenerator
from utils import get_related_words

# set game parameters (todo: create configs for different languages)
GAME_NAME = "taboo"
N_INSTANCES = 20  # how many different target words; zero means "all"
N_GUESSES = 3  # how many tries the guesser will have
N_RELATED_WORDS = 3

LANGUAGE = "en"
VERSION = 'v1.5'

logger = clemgame.get_logger(__name__)


class TabooGameInstanceGenerator(GameInstanceGenerator):

    def __init__(self):
        super().__init__(GAME_NAME)

    def load_instances(self):
        return self.load_json(f"{LANGUAGE}/in/instances")

    def on_generate(self):
        # define file location prefix for target words
        file_prefix = f"{LANGUAGE}/resources/target_words"
        if VERSION:
            file_prefix = f"{file_prefix}/{VERSION}"

        assert os.path.exists(file_prefix), \
            f'The {file_prefix} path does not exist, run utils.py -> create_folder_structure(your_language).'


        # load related words
        related_words = get_related_words(LANGUAGE)

        # load target words based on the difficultly
        for frequency in ["high", "medium", "low"]:
            print("Sampling from freq:", frequency)
            fp = f"{file_prefix}/{frequency}_freq_100"
            target_words = self.load_file(file_name=fp, file_ending=".txt").split('\n')

            # randomly sample N_INSTANCES words
            if N_INSTANCES > 0:
                assert len(target_words) >= N_INSTANCES, \
                    f'Fewer words available ({len(target_words)}) than requested ({N_INSTANCES}).'
                target_words_sample = random.sample(target_words, k=N_INSTANCES)

            # use the same target_words for the different player assignments
            experiment = self.add_experiment(f"{frequency}_{LANGUAGE}")
            experiment["max_turns"] = N_GUESSES

            # load game prompts
            describer_prompt = self.load_template(f"{LANGUAGE}/resources/initial_prompts/initial_describer")
            guesser_prompt = self.load_template(f"{LANGUAGE}/resources/initial_prompts/initial_guesser")
            experiment["describer_initial_prompt"] = describer_prompt
            experiment["guesser_initial_prompt"] = guesser_prompt

            # create game instances based on target words
            for game_id in tqdm(range(len(target_words_sample))):
                target = target_words_sample[game_id]

                game_instance = self.add_game_instance(experiment, game_id)
                game_instance["target_word"] = target

                related = related_words.get(target, [])
                if len(related) < N_RELATED_WORDS:
                    print(f"Found {len(related)} related words instead of {N_RELATED_WORDS} for: {target}")

                game_instance["related_word"] = related[:N_RELATED_WORDS]


if __name__ == '__main__':
    # todo add lang arg and read config file
    TabooGameInstanceGenerator().generate(sub_dir=f"{LANGUAGE}/in")
