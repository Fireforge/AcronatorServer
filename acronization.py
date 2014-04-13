import json
import requests
import argparse
import random
from operator import itemgetter

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


def acronym_finder(inputAcronym,numOutputs,inputGeneralKeywords):
    acronym = []

    for keyword in inputGeneralKeywords:
        thesaurusList_url = "http://words.bighugelabs.com/api/2/ff854eb1f0151b1a2d15940fdb5cb1b5/" + keyword + "/json"
        thesaurusResponse = requests.get(thesaurusList_url)
        if thesaurusResponse.status_code == 200:
            thesaurusJson = json.loads(thesaurusResponse.text)

    for i, c in enumerate(inputAcronym):
        firstLetter = c.lower()
        wordList = []

        if thesaurusResponse.status_code == 200:
            for wordType in thesaurusJson.keys():
                for meaningType in thesaurusJson[wordType].keys():
                    for word in thesaurusJson[wordType][meaningType]:
                        if word[0] == firstLetter and word.count(' ') == 0:
                            for w in wordList:
                                if w.word == word:
                                    priority = w.priority + 1
                                    wordList.remove(w)
                                    wordList.insert(0,Word(word,priority))
                                    break
                            else:
                                wordList.append(Word(word,0))

        randomWords_url = "http://api.wordnik.com:80/v4/words.json/search/" + firstLetter + "?caseSensitive=false&includePartOfSpeech=noun&minCorpusCount=5&maxCorpusCount=-1&minDictionaryCount=1&maxDictionaryCount=-1&minLength=1&maxLength=-1&skip=0&limit=10&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5"
        randomWordsResponse = requests.get(randomWords_url)
        if randomWordsResponse.status_code == 200:
            randomWordsJson = json.loads(randomWordsResponse.text)

            for entry in randomWordsJson["searchResults"]:
                word = entry["word"]
                if word[0] == firstLetter and len(word) > 1 and word.count(' ') == 0:
                    wordList.append(Word(word,0))

        sorted(wordList, key=lambda word: word.priority)
        acronym.append(AcronymLetter(firstLetter,wordList))

    winners = []
    for x in range (0,numOutputs):
        winner = ''
        for letter in acronym:
            if len(winner) == 0:
                winner = letter.words[x].word
            else:
                winner = winner + ' ' + letter.words[x].word
        winners.append(winner)

    return winners



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='De-Generate Acronym')
    parser.add_argument('acronym', metavar='ACR',help='the acronym')
    parser.add_argument('--numOutputs', metavar='NOU',type=int, help='number of outputs', default=1)
    parser.add_argument('keywords', metavar='KEY', nargs='+',help='some keywords')

    args = parser.parse_args()

    winner_list = acronym_finder(args.acronym,args.numOutputs,args.keywords)
    print('\n'.join(winner_list))