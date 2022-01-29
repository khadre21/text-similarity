from pretraitement import PreTraitement
from math import *

class Similarite:

    def __init__(self, text1, text2):
       
        self.matriceTF = []

        self.d1 = PreTraitement(text1)
        self.d1.ordonnerLesMots()
        self.d2 = PreTraitement(text2)
        self.d2.ordonnerLesMots()

        corpus = PreTraitement(text1+ ' ' + text2)
        corpus.ordonnerLesMots()

    # Détermination de la fréquence des termes au niveau des deux textes
        for i in range(0, len(corpus.doc)):
            self.matriceTF.append([corpus.doc[i], 0, 0])

        for line in self.matriceTF:
            for word in self.d1.doc:
                if line[0] == word:
                    line[1] = line[1] + 1
            for word in self.d2.doc:
                if line[0] == word:
                    line[2] = line[2] + 1


    def sim_cosinus(self):
        num = 0
        den = [0,0]
        for line in self.matriceTF:
            num += line[1] * line[2]
            den[0] += pow(line[1], 2)
            den[1] += pow(line[2], 2)
        den = sqrt(den[0]) * sqrt(den[1])
        return num/den


    def sim_livenshtein(self):
        d = [[]]

        for i in range(1, len(self.d1.doc)+1):
            d.append([i])
            for j in range(0, len(self.d2.doc)):
                d[i].append(0)
        for j in range(0, len(self.d2.doc)+1):
            d[0].append(j)
        
        for i in range(1,len(self.d1.doc)+1):
            for j in range(1,len(self.d2.doc)+1):
                if(self.d1.doc[i-1] == self.d2.doc[j-1]):
                    d[i][j] = d[i-1][j-1]
                else:
                    d[i][j] = min( d[i-1][j],
                                d[i][j-1],
                                d[i-1][j-1]  
                                ) + 1
        distance_livenshtein = d[len(self.d1.doc)][len(self.d2.doc)]
        return distance_livenshtein