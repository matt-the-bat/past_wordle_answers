#!/usr/bin/env python
"""
    Check your Wordle guess against previous answers
    provided by rockpapershotgun.com
"""
from typing import List
import requests
from bs4 import BeautifulSoup, Tag
from rich import print, console
from rich.columns import Columns
from pathlib import Path
import argparse
import clipman  # type: ignore


parser = argparse.ArgumentParser()
parser.add_argument(
    "-p",
    "--paste",
    action="store_true",
    help="Paste Anagram Solver output",
)

args = parser.parse_args()


class WordRetrievalError(LookupError, ConnectionError):
    def __str__(self):
        return (
            "Unable to retrieve words from webpage.\n"
            "Check the website for changes."
        )


def pastAnswers() -> list:
    url = "https://www.rockpapershotgun.com/wordle-past-answers"
    try:
        print("Querying website...\n")
        response = requests.get(url, timeout=14)
    except ConnectionError:
        raise
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    # Find the <h2> tag with contents "All Wordle answers"
    h2_tag = soup.find("h2", string="All Wordle answers")

    if h2_tag:
        # Find the <ul class="inline"> following the <h2> tag
        ul_tag = h2_tag.find_next_sibling("ul", class_="inline")
        if ul_tag:
            # Find all <li> tags within the <ul> tag
            li_tags = [
                li_tag
                for li_tag in ul_tag
                if isinstance(li_tag, Tag)
            ]
            # Extract the contents of each <li> tag
            li_contents = [li_tag.text for li_tag in li_tags]
            # Print the contents of all <li> tags
            return li_contents
        else:
            raise WordRetrievalError()
    else:
        raise WordRetrievalError()


""" Build list of 5-letter words """
script_dir = Path(__file__).resolve().parent
fives = "5_letter_words.txt"
with open(script_dir / fives, "r") as f:
    dictionary = [x.strip().upper() for x in f.readlines()]

pastAnswersList = pastAnswers()


def resolve_guess(guess) -> str:
    """Ayyyy lmao"""
    guess = guess.upper()
    if guess in pastAnswersList:
        return f"❌ [red]{guess} was previously used.[/red]"
    elif guess.isalpha() is False:
        return "🚫 [red]Invalid input. Use Ctrl+D to exit.[/red]"
    elif len(guess) != 5:
        return "5️⃣  [red]Guess is not 5 letters long.[/red]"
    elif guess not in dictionary:
        return "📖 [red]Not in dictionary[/red]"
    else:
        return "✅ [green]Try it![/green]"


def prompt():
    """Interactive Mode"""
    print(
        "[yellow3]Hint: [/yellow3]Do not guess -s (plurals or verbs)"
    )
    guessT = "[u]Guess[/u]: "
    while True:  # loop works great for keyboardinterrupt
        try:
            guess = console.Console().input(guessT)
            print(resolve_guess(guess) + "\n")
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except EOFError:
            break
    return ""


def with_paste() -> None:
    """Paste from clipboard, processing Anagram Solver output"""
    possibleWords: List[str] = []
    clipman.init()
    paste = list(clipman.paste().split("\n"))
    for line in paste:
        """Omit all non-answers, add guess if good"""
        if line.islower() and resolve_guess(line.strip())[0] == "✅":
            possibleWords.append(line)

    """ Display """
    columns = Columns(possibleWords, equal=True, expand=True)
    print(columns)


if __name__ == "__main__":
    if args.paste:
        with_paste()
    else:
        prompt()
