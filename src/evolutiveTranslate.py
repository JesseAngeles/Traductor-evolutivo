import pandas as pd

class evolutiveTranslate:
    def __init__(self):
        self.loadCSV()

    def loadCSV(self):
        self.df = pd.read_csv('resources/dictionary.csv')

    def saveCSV(self):
        self.df.to_csv('resources/dictionary.csv', index=False)

    def findTranslate(self, word):
        translation_word = self.df[self.df.iloc[:, 0] == word]

        if not translation_word.empty:
            return translation_word.iloc[0, 1]
        
        return False
    
    def insertWord(self, word, translate):
        self.df.loc[len(self.df)] = [word, translate]
