import re
import os
import copy
import math


class Reader:

    def __init__(self):
        positive = []
        negative = []
        pos_paths = os.listdir("data/alle/train/pos")
        neg_paths = os.listdir("data/alle/train/neg")

        for path in pos_paths:
            positive += self.file_to_list("data/alle/train/pos/"+path)

        for path in neg_paths:
            negative += self.file_to_list("data/alle/train/neg/"+path)

        self.positive_wordCount = self.countOccurances(positive)
        self.negative_wordCount = self.countOccurances(negative)

        total_words = positive + negative
        self.pruning(0.0000001, total_words)

        self.pos_infoValues = self.informative_words(True)
        self.neg_infoValues = self.informative_words(False)


    # Del 1 og 3
    def file_to_list(self,filename):
        text = ""
        file = open(filename, encoding ='utf-8')
        stop_file = open("./data/stop_words.txt", encoding ='utf-8')
        stop_words = set([word.rstrip('\n') for word in stop_file])
        stop_file.close()

        for line in file:
            text += re.sub("[.,#+()-:?!&<´>/;'^*]", "", line.lower().rstrip('\n').replace('"', '').replace("!","").replace("br ",""))
        file.close()

        words = self.n_gram(text.split())
        return list(set([word for word in words if word not in stop_words]))


    # Tar inn liste, returnerer dict med frekvens per ord
    def countOccurances(self,list):
        wordCount = {}

        for word in list:
            if word not in wordCount:
                wordCount[word] = 1
            else:
                wordCount[word] += 1

        return wordCount

    # Del 2
    # Returnerer mest populære ord
    def most_popular(self, dict):
        wordCount = copy.deepcopy(dict)
        popular_words = []

        for i in range(25):
            max_key = max(wordCount, key=wordCount.get)
            wordCount[max_key] = 0
            popular_words.extend([max_key])

        return popular_words

    # type= TRUE --> Positive and False --> Negative
    def wordValue(self,word, type):
        if type:
            if word in self.negative_wordCount:
                return self.positive_wordCount[word]/(self.positive_wordCount[word]+self.negative_wordCount[word])
            return 1

        else:
            if word in self.positive_wordCount:
                return self.negative_wordCount[word]/(self.positive_wordCount[word]+self.negative_wordCount[word])
            return 1

    # Del 4
    # type= TRUE --> Positive and False --> Negative
    def most_informative(self, type):
        values = {}
        if type:
            dict = self.positive_wordCount
        else:
            dict = self.negative_wordCount

        for word in dict:
            values[word] = self.wordValue(word,type)

        res = {}
        for i in range(25):
            max_key = max(values, key=values.get)
            res[max_key] = values[max_key]
            values[max_key] = 0
        return res

    # Del 5: Pruning
    def pruning(self, percentage, total_words):
        totalOccurances = self.countOccurances(total_words)
        for word in totalOccurances:
            try:
                if totalOccurances[word]/len(total_words) <= percentage:
                    self.positive_wordCount.pop(word)
            except KeyError:
                pass

            try:
                if totalOccurances[word]/len(total_words) <= percentage:
                    self.negative_wordCount.pop(word)
            except KeyError:
                pass

    # Del 6: n-gram
    def n_gram(self, list):
        n_list = []
        for i in range(len(list)-2):
            word1 = list[i]+"_"+list[i+1]
            word2 = list[i]+"_"+list[i+1]+"_"+list[i+2]
            n_list.append(word1)
            n_list.append(word2)

        return list+n_list

    # Information value of all words
    def informative_words(self, type):
        values = {}
        if type:
            dict = self.positive_wordCount
        else:
            dict = self.negative_wordCount

        for word in dict:
            values[word] = self.wordValue(word,type)

        return values


# Del 7 - 9
class ClassificationSystem:

    def __init__(self):
        self.reader = Reader()

    # filename = path to a file containing a movie review
    def get_type(self, filename):
        words = self.reader.file_to_list(filename)
        #print(words)
        pos_sum = 0
        neg_sum = 0
        for word in words:
            if word in self.reader.pos_infoValues:
                    pos_sum += math.log(self.reader.pos_infoValues[word])


            if word not in self.reader.pos_infoValues:
                # "Straffer" positive dersom det ikke inneholder ordet
                pos_sum += math.log(0.0005)

            if word in self.reader.neg_infoValues:
                    neg_sum += math.log(self.reader.neg_infoValues[word])

            if word not in self.reader.neg_infoValues:
                # "Straffer" positive dersom det ikke inneholder ordet
                neg_sum += math.log(0.0005)

        # returns True if positive and False if negative
        return pos_sum > neg_sum



def main():
    c = ClassificationSystem()

    pos_paths = os.listdir("data/alle/test/pos")
    neg_paths = os.listdir("data/alle/test/neg")
    pos_correct = 0
    neg_correct = 0

    for path in pos_paths:
        if c.get_type("data/alle/test/pos/"+path) == True:
            pos_correct += 1

    for path in neg_paths:
        if c.get_type("data/alle/test/neg/"+path) == False:
            neg_correct += 1

    print("Correctness:")
    print("Positive correct: "+ str(pos_correct/len(pos_paths))+" %")
    print("Negative correct: "+ str(neg_correct/len(neg_paths))+" %")
    print("Total correct: "+ str((pos_correct+neg_correct)/(len(pos_paths)+len(neg_paths)))+" %")

main()
