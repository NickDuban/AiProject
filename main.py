# code courtesy of https://nlpforhackers.io/language-models/
#import nltk
#nltk.download('all')

#from nltk.corpus import reuters
from nltk import bigrams, trigrams
from collections import Counter, defaultdict
import random
import sys
# Create a placeholder for model
model = defaultdict(lambda: defaultdict(lambda: 0))
# Count frequency of co-occurance  
#for sentence in reuters.sents():
#    for w1, w2, w3 in trigrams(sentence, pad_right=True, pad_left=True):
#        model[(w1, w2)][w3] += 1

# SOME CUSTOM TOMFOOLORRY THIS WORKS

# DuBot Personallity 
dubot = open("./AIProject/dubotAI.txt", "r",encoding='UTF8')
dubotLines = dubot.readlines()
for sentence in dubotLines:
    text = sentence.split()
    for w1, w2, w3 in trigrams(text, pad_right=True, pad_left=True):
        model[(w1, w2)][w3] += 1

# Facts Module
#facts = open("facts.txt", "r",encoding='UTF8')
#factsLines = facts.readlines()
#for sentence in factsLines:
#    text = sentence.split()
#    for w1, w2, w3 in trigrams(text, pad_right=True, pad_left=True):
#        model[(w1, w2)][w3] += 1

# Insults Module
insults = open("./AIProject/insults.txt", "r",encoding='UTF8')
insultLines = insults.readlines()
for sentence in insultLines:
    text = sentence.split()
    for w1, w2, w3 in trigrams(text, pad_right=True, pad_left=True):
        model[(w1, w2)][w3] += 1

# Compliments Module
complements = open("./AIProject/complements.txt", "r",encoding='UTF8')
complementLines = complements.readlines()
for sentence in complementLines:
    text = sentence.split()
    for w1, w2, w3 in trigrams(text, pad_right=True, pad_left=True):
        model[(w1, w2)][w3] += 1

# Self Train Module
selfTrain = open("./AIProject/dubotSelfTrain.txt", "r", encoding='cp1252')
selfTrainLines = selfTrain.readlines()
for sentence in selfTrainLines:
    text = sentence.split()
    for w1, w2, w3 in trigrams(text, pad_right=True, pad_left=True):
        model[(w1, w2)][w3] += 1
selfTrain.close()

# Let's transform the counts to probabilities
for w1_w2 in model:
    total_count = float(sum(model[w1_w2].values()))
    for w3 in model[w1_w2]:
        model[w1_w2][w3] /= total_count
#print(model.keys())
# This is after the Model is trained

# starting words
#i = 20
file = open("./AIProject/dubotSelfTrain.txt", "a")
phrases = sys.argv[1:]
#while i > 0:
sys.stdout.flush()
texts = []
for t in phrases:
    texts.append(t.split())

# text = ["I", "think", "there", "was"]
dubotSays = []
# THINKING ABOUT REWRITING HOW THE MODEL WORKS, AND HAVING SECTIONS FOR THINGS DUBOT WOULD SAY AND THINGS
# ABOUT OTHERS, well then would need verbs in all spots, maybe i should teach the whole noun verb structure
 
for text in texts:
    sentence_finished = False
    sentence_started = False
    count = 0
    anotherCount = 0
    eCount = [False,False]
    dubotError = ["There", "is" ,"a" ,"problem", "with" ,"my" ,"AI!"]
    while not sentence_finished or not sentence_started:
        # select a random probability threshold  
        r = random.random()
        accumulator = .0
        if not sentence_started:
            done = False
            secCount = -1
            thirdCount = 0
            if count > 0:
                secCount = round((random.random() * 100) % count)
            try:
                for word, t2 in model.keys():
                    if t2 == text[0]:
                        if done:
                            break  
                        x = (word, t2)
                        for sec in model[x].keys():
                            if secCount != -1:
                                if thirdCount == secCount:
                                    text.insert(0, word)
                                    done = True
                                    count = 0
                                    break
                                else:
                                    thirdCount+=1
                            if len(text) > 1:
                                if sec == text[1]:
                                    count+=1
                            else:                      
                                count+=1
            except:
                # Could fix so single word starters could start
                if (count == 0 or secCount != -1) and len(text) != 1:
                    sentence_started = True
                #print("Broke ", count, " ", text)
            if count == 0:
                sentence_started = True
                eCount[1] = True

        if not sentence_finished and len(text) > 1:
            noWord = True
            for word in model[tuple(text[-2:])].keys():
                accumulator += model[tuple(text[-2:])][word]
                noWord = False
                # select words that are above the probability threshold
                if accumulator >= r:
                    text.append(word)
                    break
            if noWord:
                sentence_finished = True
                eCount[0] = True
        else:
            anotherCount = anotherCount + 1
            if anotherCount > 6:
                sentence_finished = True
                eCount[0] = True

        if text[-2:] == [None, None]:
            sentence_finished = True
        
        if text[0] == None:
            sentence_started = True

        if sentence_started == True and sentence_finished == True and eCount != [True, True]:
            dubotSays.append(text)
        
        if eCount == [True, True]:
            dubotSays.append(dubotError)


writing = []
for text in dubotSays:
    writing.append(' '.join([t for t in text if t]) + '\n')
if writing != ['There is a problem with my AI!\n']:
    file.writelines(writing)
# i = i - 1
file.close()
file = open('./AIProject/DubotReply.txt', 'w')
file.writelines(writing)
file.close()
print(writing)
sys.stdout.flush()