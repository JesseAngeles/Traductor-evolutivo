import pandas as pd

from Levenshtein import Levenshtein

class evolutiveTranslate:
    def __init__(self):
        self.loadCSV()
        self.levenshtein = Levenshtein()

    def loadCSV(self):
        self.dictionary = pd.read_csv('resources/dictionary.csv')
        self.recommendation = pd.read_csv('resources/recommendation.csv')

    def saveCSV(self):
        self.dictionary.to_csv('resources/dictionary.csv', index=False)
        self.recommendation.to_csv('resources/recommendation.csv', index=False)

    def getHeaders(self):
        return list(self.dictionary.columns.values)

    def findLanguage(self, word, fromLanguage, toLanguage):
        word_from = self.dictionary[self.dictionary[fromLanguage] == word]
        word_to = self.dictionary[self.dictionary[toLanguage] == word]

        if not word_from.empty:
            return fromLanguage
        elif not word_to.empty:
            return toLanguage
        else:
            return False

    def findTranslate(self, word, fromLanguage, toLanguage):
        translation_df = self.dictionary[self.dictionary[fromLanguage] == word]

        if not translation_df.empty:
            return translation_df.iloc[0][toLanguage]

        return False
    
    def insertWord(self, word, translate):
        self.dictionary.loc[len(self.dictionary)] = [word, translate]

    def getDistances(self, word, fromLanguage):
        new_df = self.dictionary.copy()

        new_df['distance'] = new_df[fromLanguage].apply(lambda x: self.levenshtein.distance(word, x))

        new_df = new_df.sort_values(by='distance', ascending=True).head()
        for index, row in new_df.iterrows():
            match = self.recommendation[(self.recommendation['word'] == word) & (self.recommendation['translate'] == row[fromLanguage])]
            if match.empty:
                new_row = {"word": word, "translate": row[fromLanguage], "counter":0}  
                self.recommendation = pd.concat([self.recommendation, pd.DataFrame([new_row])], ignore_index=True)

        return self.recommendation.sort_values(by='counter', ascending=False)

    def increaseCounter(self, word, translate):
        # Encuentra la coincidencia en el DataFrame 'recommendation'
        match = self.recommendation[
            (self.recommendation['word'] == word) & 
            (self.recommendation['translate'] == translate)]
        
        if not match.empty:  
            self.recommendation.at[match.index[0], 'counter'] += 1

    def getRegister(self, index):
        return self.dictionary.iloc[index]