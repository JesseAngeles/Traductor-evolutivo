from Models.word_model import WordModel

class EvolutiveTranslate():
    def __init__(self, db):
        self.db = db
        self.languages = list(self.db['languages'].find())
        self.categories = list(self.db['categories'].find())
        self.words = list(self.db['words'].find())

        
    def get_languages(self):
        languages_data = self.db['languages'].find()
        languages_list = [lang['language'] for lang in languages_data]

        return languages_list 
    
    #todo 
    def find_translate(self, from_lan, to_lan, content):
        if from_lan == to_lan: return False

        from_language = self.find_lan_by_name(from_lan)
        to_language = self.find_lan_by_name(to_lan)

        if not from_language or not to_language: return False 

        finded = False
        for translates in self.words:
            for translate in translates['translates']:
                if str(from_language['_id']) == str(translate[0]) and str(translate[1]) == str(content):
                    finded = True
                    break
            if finded:
                for translate in translates['translates']:
                    if str(to_language['_id']) == str(translate[0]): 
                        return translate[1]
                        
        return False
    
    def add_translate(self, from_lan, to_lan, content, translate):
        from_language = self.find_lan_by_name(from_lan)
        to_language = self.find_lan_by_name(to_lan)
        
        if from_language and to_language and content and translate:
            translates = {str(from_language['_id']) : content, 
                          str(to_language['_id']) : translate}
            word = WordModel([], translates)
            self.db['words'].insert_one(word.to_dict())
            return True
        else:
            return False
        
        
    def find_lan_by_name(self, name):
        for lan in self.languages:
            if lan['language'] == name:
                return lan
            
        return False
        