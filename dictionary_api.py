import requests
import sys
from typing import Tuple, Optional, List

class Dictionary:
    def __init__(self, word: str):
        self.word = word
        self.definition: Optional[str]
        self.synonyms: List[str]
        self.antonyms: List[str]
        self.definition, self.synonyms, self.antonyms = self.word_data()

    def word_data(self) -> Tuple[Optional[str], List[str], List[str]]:
        try:
            # Fetch dictionary data
            dict_url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}'
            dictionary_data = requests.get(dict_url).json()

            # Fetch thesaurus data
            thesaurus_url = f'https://api.api-ninjas.com/v1/thesaurus?word={self.word}'
            thesaurus_data = requests.get(thesaurus_url).json()

            # Extract definition from dictionary data
            if 'meanings' in dictionary_data[0] and 'definitions' in dictionary_data[0]['meanings'][0]:
                definition = dictionary_data[0]['meanings'][0]['definitions'][0]['definition']
            else:
                definition = None

            # Extract synonyms and antonyms from thesaurus data
            synonyms = thesaurus_data.get('synonyms', [])
            antonyms = thesaurus_data.get('antonyms', [])

            return (definition, synonyms, antonyms)
        except requests.exceptions.RequestException:
            print('An error occurred while fetching data from the API')
            quit()
        except (KeyError, ValueError):
            print('The word you entered does not exist in the dictionary')
            quit()

    def display(self):
        print(
        f'''
        Definition:
            {None if not self.definition else self.definition}\n
        Synonyms:
            {None if not self.synonyms else ', '.join(self.synonyms)}\n

        Antonyms:
            {None if not self.antonyms else ', '.join(self.antonyms)}
        ''')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        word = Dictionary(sys.argv[1])
        word.display()
    else:
        print('Please provide a word to search for')
        try:
            sys.argv = input('Enter a word: ')
            word = Dictionary(sys.argv)
            word.display()
        except:
            quit()
