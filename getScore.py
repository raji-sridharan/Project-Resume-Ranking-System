from pdfminer.high_level import extract_text
from nltk.corpus import stopwords
import pandas as pd
import spacy
import re
import getEntities
import companies

def score(file):
    file_text = extract_text(file)
    name = getEntities.findname(file_text)
    number = getEntities.findnumber(file_text)
    email = getEntities.findemail(file_text)
    skill = skillScore(file_text)
    qualification = qualificationScore(file_text)
    organization = organizationScore(file_text)
    insight = insightScore(file_text)
    totalScore = skill + qualification + organization + insight
    data = {
        "Category": ['Skills','Qualification','Organization','Personality Insights'],
        "Score": [skill,qualification,organization,insight]
    }
    summary = pd.DataFrame(data)
    print(summary)
    details=[name,email,number,totalScore]
    return details

def skillScore(text):
    coreSkill = coreSkillScore(text)
    nlp = spacy.load('en_core_web_sm')
    nlp_text = nlp(text)
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv("skills.csv") 
    skills = list(data.columns.values)
    skillset = []
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    skillset = [x.lower() for x in skillset]
    skillset = [*set(skillset)]
    skillset = [i for i in skillset if i not in coreSkill]
    if(len(coreSkill)==0):
        return 2*len(skillset)
    return len(skillset) + 2*len(coreSkill)

def coreSkillScore(text):
    retext=text.replace("\n"," ")
    retext=retext.upper()
    topic=['Skills','Skill Set','Skill Sets','Key Skills','Hard Skills']
    topic = [x.upper() for x in topic]
    ch = None
    for i in topic:
        if i in retext:
            ch = i
    if ch==None:
        return []

    pattern  = ".*" + ch 
    retext = re.sub(pattern, '', retext)
    ch = None
    nexttopic = ['Area of Interest','Experience','Internship','Certification','Languages','Certificates','Interests','Education','Projects']
    nexttopic = [x.upper() for x in nexttopic]
    for i in nexttopic:
        if i in retext:
            ch = i 
            break
    if ch != None:
        pattern = ch + ".*"
        retext = re.sub(pattern, '', retext)
        retext = retext.lower()
    
    nlp = spacy.load('en_core_web_sm')
    nlp_text = nlp(retext)
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv("skills.csv") 
    skills = list(data.columns.values)
    skillset = []
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    skillset = [*set(skillset)]
    return skillset

def qualificationScore(text):
    STOPWORDS = set(stopwords.words('english'))
    EDUCATION = [
                    ['Bachelor of Science','BSC','B.S.C','B.S.C.','B S C','Bachelor of Commerce','BCOM','B.COM','B.COM.','B COM'],
                    ['Bachelor of Engineering','BE','B.E', 'B.E.', 'B E','Bachelor of Technology','BTECH', 'B.TECH','B.TECH.','B TECH'],
                    ['Masters in Engineering','ME', 'M.E', 'M.E.','M E','Master of Science','MS', 'M.S','M.S.','M S'] 
                ]
    nlp = spacy.load('en_core_web_sm')
    nlp_text = nlp(text)
    nlp_text = [sent.text.strip() for sent in nlp_text.sents]
    for index, tex in enumerate(nlp_text):
        tex = re.sub(r'[?|$|.|!|,]', r'', tex)
        if '-' in tex:
            tex = tex.partition('-')[0]
        for i in EDUCATION[1]:
            i = i.upper()
            tex = tex.upper()
            pattern = r"\s" + re.escape(i) + r"\s"
            pattern1 = re.escape(i) + r"\s"
            pattern2 = r"\s" + re.escape(i)
            if re.search(pattern,tex) or re.search(pattern1,tex) or re.search(pattern2,tex) and tex not in STOPWORDS:
                return 1
        for i in EDUCATION[2]:
            i = i.upper()
            tex = tex.upper()
            pattern = r"\s" + re.escape(i) + r"\s"
            pattern1 = re.escape(i) + r"\s"
            pattern2 = r"\s" + re.escape(i)
            if re.search(pattern,tex) or re.search(pattern1,tex) or re.search(pattern2,tex) and tex not in STOPWORDS:
                return 2
    return 0

def organizationScore(text):
    retext=text.replace("\n"," ")
    retext=retext.upper()
    topic = ["Internship","Internships","Experience","Work Experience","Employment History","Professional Experience"]
    topic = [x.upper() for x in topic]
    ch = None
    for i in topic:
        if i in retext:
            ch = i
    if ch == None:
        return 0
    pattern  = ".*" + ch 
    retext = re.sub(pattern, '', retext )
    retext = retext.lower()
    score=0
    for i in range(len(companies.company)):
      ch = companies.company[i].lower()
      pattern = r"\s" + re.escape(ch) + r"\s"
      if re.search(pattern,retext):
        score += 1
    return score

def insightScore(text):
    score=0
    text=text.replace('.','')
    text=text.replace('\n',' ')
    insight = ['learner','enthusiastic','engage','goals','motivated','passionate','hardworking','interest','solving','art','grow','responsible']
    for i in insight:
        pattern = r"\s" + re.escape(i) + r"\s"
        if re.search(pattern,text):
            score+=0.5
    return round(score)
