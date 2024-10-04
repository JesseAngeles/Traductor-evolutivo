import pandas as pd

from Levenshtein import Levenshtein

class evolutiveTranslate:
    def __init__(self):
        self.loadCSV()
        self.levenshtein = Levenshtein()

    def loadCSV(self):
        self.df = pd.read_csv('resources/dictionary.csv')

    def saveCSV(self):
        self.df.to_csv('resources/dictionary.csv', index=False)

    def getHeaders(self):
        return list(self.df.columns.values)

    def findTranslate(self, word):
        translation_word = self.df[self.df.iloc[:, 0] == word]

        if not translation_word.empty:
            return translation_word.iloc[0, 1]
        
        return False
    
    def insertWord(self, word, translate):
        self.df.loc[len(self.df)] = [word, translate]

    def getDistances(self, word):
        new_df = self.df.copy()

        new_df['distance'] = new_df['español'].apply(lambda x: self.levenshtein.distance(word, x))

        return new_df.sort_values(by='distance', ascending=True)

    def getRegister(self, index):
        return self.df.iloc[index]