import json
import argparse
import random
import sys

import requests

BIGHUGELABS_API_KEY = 'f79909b74265ba8593daf87741f3c874'

buzzWords = ['alignment','bot', 'collusion', 'derivative', 'engagement', 'focus', 'gathering' ,'housing','liability','management','nomenclature','operation','procedure','reduction','strategic','technology','undertaking','vision','widget','yardbird']
forbiddenWords = ['who','what','when','where','why','were','am','and','there','their']

class AcronymLetter:
    def __init__(self, letter, word_list):
        self.letter = letter.upper()
        self.words = word_list
    def __str__(self):
        outString = ''

        for word in self.words:
            if len(outString) == 0:
                outString = self.letter + " - " + str(word)
            else:
                outString = outString + ", " + str(word) 
        return outString


class Word:
    def __init__(self, word, priority):
        self.word = word
        self.priority = priority
    def __str__(self):
        return self.word + " : " + str(self.priority)


def acronym_finder(inputAcronym, inputGeneralKeywords, numOutputs=5, minWordLength=2):
    # holds letter objects 
    acronym = []

    inputError = False 
    if minWordLength < 2:
        print('You dun goofed. Minimum word length must be greater than 1')
        inputError = True
    if numOutputs < 1:
        print('WTF! How does it make sense to print any less than 1 output?')
        inputError = True

    if inputError:
        sys.exit()
    
    # Generate possible word names from the synonym API
    for keyword in inputGeneralKeywords:
        thesaurusList_url = "http://words.bighugelabs.com/api/2/" + BIGHUGELABS_API_KEY + "/" + keyword + "/json"
        thesaurusResponse = requests.get(thesaurusList_url)
        if thesaurusResponse.status_code == 200:
            thesaurusJson = json.loads(thesaurusResponse.text)
        # this is normal for some words. 
        elif thesaurusResponse.status_code == 404:
            continue
        else:
            print("Shit: " + str(thesaurusResponse.status_code))

    letters = []

    for i, c in enumerate(inputAcronym):
        letters.append(c)
            
    distinctLetters = list(set(letters))

    # Rank possible synonym words for each letter in the acronym
	for letter in distinctLetters:
        firstLetter = letter.lower()
        wordList = []

        if thesaurusResponse.status_code == 200:
            for wordType in thesaurusJson.keys():
                for meaningType in thesaurusJson[wordType].keys(): 
                    for word in thesaurusJson[wordType][meaningType]:
                        if word[0] == firstLetter and word.count(' ') == 0 and len(word) >= minWordLength:
                            for w in wordList:
                                if w.word == word:
                                    priority = w.priority + 1
                                    wordList.remove(w)
                                    wordList.insert(0,Word(word,priority))
                                    break
                            else:
                                wordList.append(Word(word,1))
        
        randomWords_url = "http://api.wordnik.com:80/v4/words.json/search/" + firstLetter + "?caseSensitive=false&includePartOfSpeech=noun&minCorpusCount=5&maxCorpusCount=-1&minDictionaryCount=1&maxDictionaryCount=-1&minLength=" + str(minWordLength) + "&maxLength=-1&skip=0&limit=" + str(4 * minWordLength * minWordLength * minWordLength) + "&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5" 
        randomWordsResponse = requests.get(randomWords_url)
        if randomWordsResponse.status_code == 200:
            randomWordsJson = json.loads(randomWordsResponse.text)
        
            for entry in randomWordsJson["searchResults"]:
                word = entry["word"]
                if word[0] == firstLetter and len(word) >= minWordLength and word.count(' ') == 0:
                    wordList.append(Word(word,0))
    
        sorted(wordList, key=lambda word: word.priority)
        acronym.append(AcronymLetter(firstLetter,wordList))

    # Generate possible acronym results
    winners = []

    for x in range (0,numOutputs):
        winner = ''
        for i, c in enumerate(inputAcronym):
            for letter in acronym: 
                if letter.letter == c:
            try:
                        word = letter.words[0]
                if len(winner) == 0:
                            winner = word.word
                            letter.words.remove(word)
                else:
                            winner = winner + ' ' + word.word
                            letter.words.remove(word)
            except IndexError:
                print("Can't get all {} words".format(len(acronym)))
        
        # Sanity Check if the winner is a valid acronym
        #if len(winner.split(' ')) == len(acronym):
            winners.append(winner)
    
    return winners


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='De-Generate Acronym')
    parser.add_argument('acronym', metavar='ACR',help='the acronym')
    parser.add_argument('--numOutputs', metavar='NOU',type=int, help='number of outputs', default=1)
    parser.add_argument('--minLength', metavar='MIN',type=int, help='minimum length of words used', default=2)
    parser.add_argument('keywords', metavar='KEY', nargs='+',help='some keywords') 
     
    args = parser.parse_args()
    
    winner_list = acronym_finder(
        inputAcronym=args.acronym,
        numOutputs=args.numOutputs,
        inputGeneralKeywords=args.keywords,
        minWordLength=args.minLength)
    print('\n'.join(winner_list))
    
    # Test call
#     print(acronym_finder('hello', 5, 'world'))
