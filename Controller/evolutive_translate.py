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
        self.frecuency_errros = self.s_frecuency_errors.get_frecuency_errors()  # Actualización inicial
        
        self.levenshtein = Levenshtein
        
    def get_languages(self):
        languages_data = self.db['languages'].find()
        languages_list = [lang['language'] for lang in languages_data]

        return languages_list 
    
    def find_translate(self, from_lan, to_lan, content):
        if from_lan == to_lan: 
            return False

        from_language = self.find_lan_by_name(from_lan)
        to_language = self.find_lan_by_name(to_lan)

        if not from_language or not to_language: 
            return False 
        
        for translates in self.words:
            if str(from_language['_id']) in translates['translates'] and translates['translates'][str(from_language['_id'])] == content:
                # Si encuentra el idioma destino en las traducciones
                if str(to_language['_id']) in translates['translates']:
                    return translates['translates'][str(to_language['_id'])]
                
        return False
    
    def add_translate(self, from_lan, to_lan, content, translate):
        from_language = self.find_lan_by_name(from_lan)
        to_language = self.find_lan_by_name(to_lan)
        
        if from_language and to_language and content and translate:
            translates = {str(from_language['_id']) : content, 
                          str(to_language['_id']) : translate}
            word = WordModel([], translates)
            self.db['words'].insert_one(word.to_dict())
            self.words = list(self.db['words'].find())  # Actualizamos después de cada inserción
            
    def get_similar_words(self, word):
        words = []
        for content in self.words:
            for _, translate in content['translates'].items():
                # Calcula la distancia de Levenshtein entre `word` y cada `translate`
                new_word = (translate, self.levenshtein.distance(self, word, translate))
                words.append(new_word)
        
        sorted_words = sorted(words, key=lambda x: x[1])[:5]  # Obtiene las 5 palabras más cercanas
        
        for error in self.frecuency_errros:
            if error['word'] == word:
                # Si existe en la lista de errores, devolvemos las correcciones
                return sorted(error['corrections'], key=lambda x: x[2], reverse=True)
        
        # Si no existe, lo creamos
        corrections = [(item[0], item[1], 0) for item in sorted_words]
        frecuency_error = FrecuencyErrorModel(word, corrections)
        self.s_frecuency_errors.add_frecuency_error(frecuency_error)
        
        # Refrescamos la lista de errores para incluir el nuevo
        self.frecuency_errros = self.s_frecuency_errors.get_frecuency_errors()
        
        return sorted(frecuency_error.to_dict()['corrections'], key=lambda x: x[2], reverse=True)

    def update_frecuency_errors(self, word, translate):
        # Intentamos encontrar el error en los datos existentes
        for error in self.frecuency_errros:
            if error['word'] == word:
                for correction in error['corrections']:
                    if correction[0] == translate:
                        correction[2] += 1  # Actualizamos la frecuencia
                        self.s_frecuency_errors.update_frecuency_error(error)
                        # Refrescamos los errores para asegurarnos de tener datos consistentes
                        self.frecuency_errros = self.s_frecuency_errors.get_frecuency_errors()
                        return
                    
        # Si no se encontró el error, lo agregamos
        corrections = [(translate, 0, 1)] 
        new_frecuency_error = FrecuencyErrorModel(word, corrections)
        self.s_frecuency_errors.add_frecuency_error(new_frecuency_error)
        self.frecuency_errros = self.s_frecuency_errors.get_frecuency_errors()
    
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
