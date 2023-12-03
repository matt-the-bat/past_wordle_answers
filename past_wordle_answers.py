#!/usr/bin/env python
""" Guess against the previous answers (and dictionary)
    provided by rockpapershotgun.com
"""
import requests
from bs4 import BeautifulSoup, Tag
from rich import print, console


class WordRetrievalError(LookupError, ConnectionError):
    def __str__(self):
        return "Unable to retrieve words from webpage.\n"\
                "Check the website for changes."


def pastAnswers() -> list:
    url = 'https://www.rockpapershotgun.com/wordle-past-answers'
    try:
        print('Querying website...\n')
        response = requests.get(url)
    except ConnectionError:
        raise
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find the <h2> tag with contents "All Wordle answers"
    h2_tag = soup.find('h2', string='All Wordle answers')

    if h2_tag:
        # Find the <ul class="inline"> following the <h2> tag
        ul_tag = h2_tag.find_next_sibling('ul', class_='inline')
        if ul_tag:
            # Find all <li> tags within the <ul> tag
            li_tags = [li_tag for li_tag in ul_tag
                       if isinstance(li_tag, Tag)]
            # Extract the contents of each <li> tag
            li_contents = [li_tag.text for li_tag in li_tags]
            # Print the contents of all <li> tags
            return li_contents
        else:
            raise WordRetrievalError()
    else:
        raise WordRetrievalError()


with open('5_letter_words.txt', 'r') as f:
    dictionary = [x.strip().upper() for x in f.readlines()]

pastAnswersList = pastAnswers()

# Prompts
print('[yellow3]Do not guess -s (plurals or verbs)[/yellow3]')
while True:  # loop works great for keyboardinterrupt
    try:
        guessT = '[u]Guess[/u]: '
        guess = console.Console().input(guessT).upper()
        if guess in pastAnswersList:
            print(f'❌ [red]{guess}[/red] was previously used.\n')
        elif guess.isalpha() is False:
            print('[red]Invalid input[/red]\n')
        elif len(guess) != 5:
            print('Guess is not 5 letters long\n')
        elif guess not in dictionary:
            print('[red]Not in dictionary[/red]\n')
        else:
            print('✅ [green]Try it![/green]\n')

    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except EOFError:
        break
