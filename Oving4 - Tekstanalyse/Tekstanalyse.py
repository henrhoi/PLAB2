import re
import os
import copy
import math

__author__ = "Henrik Høiness"

class Reader:

    def __init__(self, trainpath, prune, stopword_path, n_grams):
        positive = []
        negative = []
        self.n_grams = n_grams
        pos_paths = os.listdir(trainpath+"/pos")
        neg_paths = os.listdir(trainpath+"/neg")
        self.stopword_path = stopword_path


        for path in pos_paths:
            positive += self.file_to_list(trainpath+"/pos/"+path)

        for path in neg_paths:
            negative += self.file_to_list(trainpath+"/neg/"+path)

        self.positive_wordCount = self.countOccurances(positive)
        self.negative_wordCount = self.countOccurances(negative)

        total_words = positive + negative
        self.pruning(prune, total_words)

        self.pos_infoValues = self.informative_words(True)
        self.neg_infoValues = self.informative_words(False)



    # Del 1 og 3
    def file_to_list(self,filename):
        text = ""
        file = open(filename, encoding ='utf-8')
        stop_file = open(self.stopword_path, encoding ='utf-8')
        stop_words = set([word.rstrip('\n') for word in stop_file])
        stop_file.close()

        for line in file:
            text += re.sub("[.,#+()-:?!&<´>/;'^*]", "", line.lower().rstrip('\n').replace('"', '').replace("!","").replace("br ",""))
        file.close()

        words = self.n_gram(text.split(),self.n_grams)
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
    def most_popular(self, dict, number):
        wordCount = copy.deepcopy(dict)
        popular_words = []

        for i in range(number):
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
    def n_gram(self, in_list, n):
        n_list = []
        for k in range(len(n)):
            for i in range(len(in_list)-n[k]):
                word = ""
                j = 0
                while j < n[k]:
                    word += in_list[i+j]
                    word += "_"
                    j += 1
                n_list.append(word[:-1])

        return in_list+n_list

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

    def __init__(self, trainpath, prune, stopword_path, n_grams):
        self.reader = Reader(trainpath, prune, stopword_path, n_grams)

    # filename = path to a file containing a movie review
    def get_type(self, filename, e):
        words = self.reader.file_to_list(filename)
        pos_sum = 0
        neg_sum = 0
        for word in words:
            if word in self.reader.pos_infoValues:
                    pos_sum += math.log(self.reader.pos_infoValues[word])


            if word not in self.reader.pos_infoValues:
                # "Straffer" positive dersom det ikke inneholder ordet
                pos_sum += math.log(e)

            if word in self.reader.neg_infoValues:
                    neg_sum += math.log(self.reader.neg_infoValues[word])

            if word not in self.reader.neg_infoValues:
                # "Straffer" positive dersom det ikke inneholder ordet
                neg_sum += math.log(e)

        # returns True if positive and False if negative
        return pos_sum > neg_sum



def main():
    # Her kan jeg endre hvordan klassifikasjonssystemet skal fungere. Kan velge treningsfiler, stoppord og n-gram i
    # klassifiseringen av ord. Prune-verdien går på prosentandelen til ordet i summen av alle dokumenter.

    trainpath = "data/alle/train";      prune= 0.0000001;    stopword_path = "./data/stop_words.txt";  n_grams = [2,3,4,5,6,7,8,9]
    c = ClassificationSystem(trainpath, prune, stopword_path, n_grams)

    pos_paths = os.listdir("data/alle/test/pos")
    neg_paths = os.listdir("data/alle/test/neg")
    pos_correct = 0
    neg_correct = 0
    e = 0.0005

    for path in pos_paths:
        if c.get_type("data/alle/test/pos/"+path, e) == True:
            pos_correct += 1

    for path in neg_paths:
        if c.get_type("data/alle/test/neg/"+path, e) == False:
            neg_correct += 1

    print("Correctness:")
    print("Positive correct: "+ str(pos_correct/len(pos_paths))+" %")
    print("Negative correct: "+ str(neg_correct/len(neg_paths))+" %")
    print("Total correct: "+ str((pos_correct+neg_correct)/(len(pos_paths)+len(neg_paths)))+" %")

main()
