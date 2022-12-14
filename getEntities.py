from operator import gt
import re
import en_core_web_sm
from spacy.matcher import Matcher

def findname(text):
    nlp = en_core_web_sm.load()
    matcher = Matcher(nlp.vocab)
    nlp_text = nlp(text)
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    matcher.add('NAME', [pattern])
    matches = matcher(nlp_text)
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text.title()

def findnumber(text):
    orphone = re.search(r'\b[6789]\d{11}\b', text, flags=0)
    phone = re.search(r'\b[6789]\d{9}\b', text, flags=0)
    if phone:
      return phone.group(0)
    elif orphone:
      return orphone.group(0)
    return "None"

def findemail(text):
    EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
    if len(re.findall(EMAIL_REG, text)) > 0:
        return re.findall(EMAIL_REG, text)[0]
    return "None"

findname("my name is raji s")
