import re
from .badwords import BAD_WORDS  

def censor_word(word):
    if len(word) <= 1:
        return word
    return word[0] + '*' * (len(word) - 1)

def censor_text(text):
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, BAD_WORDS)) + r')\b', re.IGNORECASE)

    def replacer(match):
        word = match.group()
        censored = censor_word(word)
        if word[0].isupper():
            censored = censored[0].upper() + censored[1:]
        else:
            censored = censored.lower()
        return censored

    return pattern.sub(replacer, text)