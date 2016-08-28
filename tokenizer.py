'''
This code borrows liberally (very liberally) from Christopher Potts'
Twitter-aware tokenizer, full code available here:
http://sentiment.christopherpotts.net/code-data/happyfuntokenizing.py
'''

import re
import htmlentitydefs

regex_strings = (
    # HTML tags
    r"""<[^>]+>""",

    # Twitter username:
    r"""(?:@[\w_]+)"""

    # Twitter hashtags:
    r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)""",

    # Other word types:
    r"""

    # Words with apostrophes or dashes
    (?:[a-z][a-z'\-_]+[a-z])
    |
    # Numbers, including fractions and decimals
    (?:[+\-]?\d+[,/.:-]\d+[+\-]?)
    |
    # Words without apostrophes or dashes
    (?:[\w_]+)
    |
    # Ellipsis dots
    (?:\.(?:\s*\.){1,})
    |
    # Everything else that is not whitespace
    (?:\S)
    """
)

neg_regex = (
    r"""
    (?:
    ^(?:never|no|nothing|nowhere|noone|none|not|
        havent|hasnt|hadnt|cant|couldnt|shouldnt|
        wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint
    )$
    )
    |
    n't"""
)

word_regex = re.compile(r"""(%s)""" % "|".join(
    regex_strings), re.VERBOSE | re.I | re.UNICODE)

# For regularizing HTML entities to Unicode:
html_entity_digit_re = re.compile(r"&#\d+;")
html_entity_alpha_re = re.compile(r"&\w+;")
amp = "&amp;"


# Generate a list containing all of the
# stop words included in stopwords.txt


def readStopWords():
    stop_words = []
    fp = open('stopwords.txt', 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stop_words.append(word)
        line = fp.readline()
    fp.close()
    return stop_words


class Tokenizer:

    def __init__(self, preserve_case=False):
        self.preserve_case = preserve_case

    def tokenize(self, s):
        # Attempt to ensure unicode
        try:
            s = unicode(s)
        except UnicodeDecodeError:
            s = str(s).encode('string_escape')
            s = unicode(s)
        # Fix HTML character entities
        s = self.htmlToUnicode(s)
        # Tokenize
        words = word_regex.findall(s)
        # Alter case
        words = [x.lower() for x in words]
        # Remove stop words
        stop_words = readStopWords()
        words = [x for x in words if x not in stop_words]
        return words

    def htmlToUnicode(self, s):
        # Replace all HTML entities with their
        # corresponding unicode characters

        html_ents = set(html_entity_digit_re.findall(s))
        if len(html_ents) > 0:
            for ent in html_ents:
                ent_num = ent[2:-1]
                try:
                    ent_num = int(ent_num)
                    s = s.replace(ent, unichr(ent_num))
                except:
                    pass

        html_ents = set(html_entity_alpha_re.findall(s))
        html_ents = filter((lambda x: x != amp), html_ents)
        for ent in html_ents:
            ent_name = ent[1:-1]
            try:
                s = s.replace(ent, unichr(htmlentitydefs.
                                          name2codepoint[ent_name]))
            except:
                pass
            s = s.replace(amp, " and ")
        return s
