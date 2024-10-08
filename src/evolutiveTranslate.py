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

    def findLanguage(self, word, fromLanguage, toLanguage):
        word_from = self.df[self.df[fromLanguage] == word]
        word_to = self.df[self.df[toLanguage] == word]

        if not word_from.empty:
            return fromLanguage
        elif not word_to.empty:
            return toLanguage
        else:
            return False

    def findTranslate(self, word, fromLanguage, toLanguage):
        translation_df = self.df[self.df[fromLanguage] == word]

        if not translation_df.empty:
            return translation_df.iloc[0][toLanguage]

        return False
    
    def insertWord(self, word, translate):
        self.df.loc[len(self.df)] = [word, translate]

    def getDistances(self, word, fromLanguage):
        new_df = self.df.copy()

        new_df['distance'] = new_df[fromLanguage].apply(lambda x: self.levenshtein.distance(word, x))

        return new_df.sort_values(by='distance', ascending=True)

    def getRegister(self, index):
        return self.df.iloc[index]