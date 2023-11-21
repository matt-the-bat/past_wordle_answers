# Introduction
past_wordle_answers is a Python script that checks rockpapershotgun.com's [list of past answers](https://www.rockpapershotgun.com/wordle-past-answers) for Wordle.

I couldn't find reliable word lists, nor chronological time-stamped ones to reference. So the solution was to query a website, oh well.

# Requirements
`requests` and `beautifulsoup4` for the querying.

`rich` to throw in some color text.

The included `5_letter_words` to check spelling.

# Usage
Run past_wordle_answers.py and a prompt for your guess appears.
It will tell you if the word's valid, been guessed, or available to try!
