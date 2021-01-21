import nltk
import numpy as np
import random
import string
import json

f=open('disease.txt','r',errors = 'ignore')

raw=f.read()
raw=raw.lower()
sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)


lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


def greeting(sentence):
    
    with open("inputs.json") as greetFile:
        greets = json.load(greetFile)
    for word in sentence.split():
        if word.lower() in greets["greetings"]:
            return(random.choice(greets["greetings"]))

# Checking for Basic_Q
def basic(sentence):
    
    with open("inputs.json") as baseQueryFile:
        baseQueries = json.load(baseQueryFile)
    with open("responses.json") as baseRespFile:
        baseResps = json.load(baseRespFile)
    for word in baseQueries["basic_query"]:
        if sentence.lower() == word:
            return baseResps["basic_query_resp"][0]

# Checking for Basic_QM
def basicM(sentence):
    
    with open("inputs.json") as input_comparisons:
        inpComp_f = json.load(input_comparisons)
    

# Checking for Introduce
def IntroduceMe(sentence):
    
    with open("inputs.json") as introFile:
        intros = json.load(introFile)
    with open("responses.json") as introRespFile:
        introResps = json.load(introRespFile)
    return random.choice(introResps["introduce"])


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response




def chat(user_response):
    user_response=user_response.lower().strip()
    with open("inputs.json") as input_comparisons:
        inpComp_f = json.load(input_comparisons)
    keyword = [" siam weed ", " chaff flower weed", "black pigweed weed  ", " bermuda weed ", " touch me not weed ", " crowsfoot weed ", " weeds ", " details "]

    if user_response != 'bye' :
        if(user_response=='thanks' or user_response=='thank you' ):
            return "You are welcome.."
        elif basicM(user_response)!=None:
            return basicM(user_response)
        else:
            if user_response in keyword:
                
                return response(user_response)
                
                
            elif greeting(user_response)!=None:
                return greeting(user_response)
            elif user_response in inpComp_f["introduce"]:
                return IntroduceMe(user_response)
          
            elif basic(user_response)!=None:
                from googletrans import Translator
                
      
                return response(user_response)
            else:
                
                return response(user_response)
                

    else:
        return "Bye! take care.."
