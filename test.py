import json
import requests
import argparse

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

#    inputAcronym = input("Input an acronym: ")
#    inputGeneralKeywords = input("Input an general keywords: ")

    for i, c in enumerate(inputAcronym):
#        inputKeywords = input("Input some keywords for " + c + ": ")
        firstLetter = c.lower()

        wordList = []
        for keyword in inputGeneralKeywords:
            thesaurusList_url = "http://words.bighugelabs.com/api/2/ff854eb1f0151b1a2d15940fdb5cb1b5/" + keyword + "/json"

            response = requests.get(thesaurusList_url)
            if response.status_code == 200:
                json_words = json.loads(response.text)

                for wordType in json_words.keys():
                    for meaningType in json_words[wordType].keys():
                        for word in json_words[wordType][meaningType]:
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
            response = requests.get(randomWords_url)
            if response.status_code == 200:
                json_words = json.loads(response.text)

                for entry in json_words["searchResults"]:
                    word = entry["word"]
                    if word[0].islower() and word != firstLetter:
                       # for w in wordList:
                       #     if w.word == word:
                       #         break
                       #     else:
                       wordList.append(Word(word,0))

        acronym.append(AcronymLetter(firstLetter,wordList))

    results = ''

    for x in range (0,numOutputs):
        winner = ''
        for letter in acronym:
            winner = winner + ' ' + letter.words[x].word
        #print(winner)
        results += winner + '\n'
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='De-Generate Acronym')
    parser.add_argument('acronym', metavar='ACR',help='the acronym')
    parser.add_argument('--numOutputs', metavar='NOU',type=int, help='number of outputs', default=1)
    parser.add_argument('keywords', metavar='KEY', nargs='+',help='some keywords')

    args = parser.parse_args()

    #print(args)
    acronym_finder(args.acronym,args.numOutputs,args.keywords)