import spacy
from nltk.corpus import wordnet as wn
from transformers import *


nlp = spacy.load('en_core_web_sm')
doc = nlp("Just as we must identify all the outputs necessary to reach the purpose .")   

# 步驟 1
def check_sentence_vn(doc):
    annotations = []
    vn=[]
    i=0
    for token in doc:
        if(token.dep_=='dobj'):
            annotations.append([token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.head,i])
        i = i + 1

    for word in annotations:
        i = 0
        worddata=(word[1],word[6])
        tmp=[]
        for token in doc:
            if (str(token.lemma_) == str(word[5]) ):
                tmp.append((token.lemma_,i))
            i = i + 1
        tmp.append(worddata)
        vn.append(tmp)
    return vn


#check_sentence_vn(doc)
''' check_sentence_vn() Output
[[('identify', 4), ('output', 7)], [('reach', 10), ('purpose', 12)]]  
'''


model = "bert-large-uncased"
p = pipeline("fill-mask", model=model, topk=100)


# 步驟 2
def mask_cand(sentence, i):
    new_str = sentence.split(' ')
    new_str[i] = '[MASK]'
    cand_list=[]
    canstr=''
    for i in new_str:
        canstr = canstr + i
        canstr = canstr + ' '
    print(canstr)
    candidates = p(canstr)
    for cand in candidates:
        cand_list.append((cand['token_str'], cand['score']))
    return cand_list

#mask_cand('Just as we must identify all the outputs necessary to reach the purpose .', 4)
''' mask_cand() Output
[('produce', 0.319),
 ('achieve', 0.101),
 ('make', 0.0869),
 ('have', 0.0644),
 ('obtain', 0.0523),
 ('get', 0.0424),
 ('generate', 0.0295),
 ('provide', 0.0219),
 ('create', 0.0134),
'''

from itertools import product
print([i for i in product([1,2],[3,4,5])])

import nltk
nltk.download('wordnet')
# 步驟 3
def similarity(sentence):
    global tester_str
    originWord_list = []
    ans=[]
    for i in sentence:
        print(i)
        masklist = mask_cand(tester_str, i[0][1])
        for synset in wn.synsets(i[0][0], 'v'):
            originWord_list.append(synset)
        for mask_item in masklist:
            max_sim=0
            for maskWord in wn.synsets(mask_item[0], 'v'):
                for originWord in originWord_list:
                    if(originWord.path_similarity(maskWord)>max_sim):
                        max_sim=originWord.path_similarity(maskWord)
            if (max_sim >= 0.4):
                if(mask_item[0]!=i[0][0]):
                    ans.append((mask_item[0], i[1][0], max_sim, mask_item[1]))
                    
        ans.sort(key=lambda score: score[2] + score[3], reverse=True)
        for i in ans:
            print(i)
    print('\n')

tester_str="They all have the mistake ."
doc_3 = nlp(tester_str)   
miscollocations = check_sentence_vn(doc_3)
similarity(miscollocations)
tester_str="I reach the dream as a teacher now ."
doc_3 = nlp(tester_str)   
miscollocations = check_sentence_vn(doc_3)
similarity(miscollocations)
tester_str="This does not entail that we never learn knowledge ."
doc_3 = nlp(tester_str)   
miscollocations = check_sentence_vn(doc_3)
similarity(miscollocations)

tester_str="Just as we must identify all the outputs necessary to reach the purpose ."
doc_3 = nlp(tester_str)   
miscollocations = check_sentence_vn(doc_3)
similarity(miscollocations)


''' similarity() Output
Just as we must [MASK] all the outputs necessary to reach the purpose .
('consider', 'output', 0.5, 0.00335, 3)
('see', 'output', 0.5, 0.0016, 3)
('determine', 'output', 0.5, 0.000828, 3)

Just as we must identify all the outputs necessary to [MASK] the purpose .
('achieve', 'purpose', 1.0, 0.548, 3)
('accomplish', 'purpose', 1.0, 0.262, 3)
('attain', 'purpose', 1.0, 0.0117, 3)
'''

