#encoding=utf-8

import re
from nltk.tokenize import word_tokenize

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += " "+ele
    return str1


def clean_tex(example_sent):

    if len(example_sent)>0:
        text_nopunct= re.sub(r'[^\w\s]',' ',example_sent)
        output = word_tokenize(text_nopunct)
        cleaned_stc = listToString(output)
        return cleaned_stc
    else:
        return example_sent