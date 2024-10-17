from Models.word_model import WordModel
from Models.frecuency_error_model import FrecuencyErrorModel

from Services.frecuency_error_service import FrecuencyErrorService
from Controller.levenshtein import Levenshtein 

class EvolutiveTranslate():
    def __init__(self, db):
        self.db = db
        
        self.s_frecuency_errors = FrecuencyErrorService(db)
        
        self.languages = list(self.db['languages'].find())
        self.categories = list(self.db['categories'].find())
        self.words = list(self.db['words'].find())
        self.frecuency_errros = self.s_frecuency_errors.get_frecuency_errors()
        
        self.levenshtein = Levenshtein
        
    def get_languages(self):
        languages_data = self.db['languages'].find()
        languages_list = [lang['language'] for lang in languages_data]

        return languages_list 
    
    def find_translate(self, from_lan, to_lan, content):
        if from_lan == to_lan: return False

        from_language = self.find_lan_by_name(from_lan)
        to_language = self.find_lan_by_name(to_lan)

        if not from_language or not to_language: return False 
        finded = False
        for translates in self.words:
            for object_id, translation in translates['translates'].items():
                if str(from_language['_id']) == str(object_id) and str(translation) == str(content):
                    finded = True
                    break
            if finded:
                for object_id, translation in translates['translates'].items():
                    if str(to_language['_id']) == str(object_id): 
                        return translation
                        
        return False
    
    def add_translate(self, from_lan, to_lan, content, translate):
        from_language = self.find_lan_by_name(from_lan)
        to_language = self.find_lan_by_name(to_lan)
        
        if from_language and to_language and content and translate:
            translates = {str(from_language['_id']) : content, 
                          str(to_language['_id']) : translate}
            word = WordModel([], translates)
            self.db['words'].insert_one(word.to_dict())
            self.words = list(self.db['words'].find())
            

    def get_similar_words(self, word):
        words = []
        for content in self.words:
            for _, translate in content['translates'].items():
                new_word = (translate, self.levenshtein.distance(self, word, translate))
                words.append(new_word)
        
        sorted_words = sorted(words, key=lambda x: x[1])[0:5]
        
        for error in self.frecuency_errros:
            if error['word'] == word:
                return sorted(error['corrections'], key=lambda x: x[2], reverse=True)
        
        corrections = []
        for item in sorted_words:
            correction = (item[0], item[1], 0)
            corrections.append(correction)
        frecuency_error = FrecuencyErrorModel(word, corrections)
        self.s_frecuency_errors.add_frecuency_error(frecuency_error)
        
        return sorted(frecuency_error.to_dict()['corrections'], key=lambda x: x[2], reverse=True)

    def update_frecuency_errors(self, word, translate):
        for error in self.frecuency_errros:
            
            if error['word'] == word:
                for correction in error['corrections']:
                    if correction[0] == translate:
                        correction[2] += 1
                        self.s_frecuency_errors.update_frecuency_error(error)
                        return
    
    
    def find_lan_by_word(self, word):
        for translate in self.words:
            for object_id, content in translate['translates'].items():
                if word == content:
                    for lan in self.languages:
                        if str(lan['_id']) == object_id:
                            return lan['language']

    def find_lan_by_name(self, name):
        for lan in self.languages:
            if lan['language'] == name:
                return lan
            
        return False
        