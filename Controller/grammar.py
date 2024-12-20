from Models.category_model import CategoryModel
from Models.language_model import LanguageModel
from Models.struct_model import StructModel

from Services.category_service import CategoryService
from Services.word_service import WordService
from Services.language_service import LanguageService
from Services.struct_service import StructService

class Grammar:
    def __init__(self, db):
        self.db = db
        self.category_service = CategoryService(db)
        self.word_service = WordService(db)
        self.language_service = LanguageService(db)
        self.struct_service = StructService(db)
        self.categories = self.category_service.get_categories()

    def get_categories(self):
        self.categories = self.category_service.get_categories()
        new_categories = list()
        for i in self.categories:
            new_categories.append(i['category'])

            
        return new_categories
        
    
    def addCategory(self, category_name):
        model  = CategoryModel(category_name)
        self.category_service.add_category(model)
        self.categories.append(model)
        
    def setCategory(self, set_word, f_category):
        current_category = CategoryModel
        for category in self.categories:
            if category['category'] == f_category:
                current_category = category
                break

        # Find word in words
        words = self.word_service.get_words()
        for word in words:
            for translate in word['translates']:
                if (word['translates'][translate] == set_word):
                    word['categories'].append(current_category)
                    self.word_service.update_word(word['_id'], word)
                    return

    def setStruct(self, from_lan, to_lan, from_content, to_content):
        words_from = from_content.split()
        words_to = to_content.split()

        from_language = LanguageModel
        to_language = LanguageModel
        
        exists = 0
        # Buscar los idiomas
        for language in self.language_service.get_languages():
            if from_lan == language['language']:
                from_language = language
                exists+=1
            elif to_lan == language['language']:
                to_language = language
                exists+=1
        
        if exists < 2:
            return

        from_list = list()
        to_list = list()

        # Iterar words from
        for current_word in words_from:
            # Iterar sobre las palabras para encontrarla
            for word in self.word_service.get_words():
                # Iterar sobre los lenguages
                for lan in word['translates']:
                    if lan == str(from_language['_id']):
                        if word['translates'][lan] == current_word:
                            from_list.append(word)
                            break
        
        # Iterar words to
        for current_word in words_to:
            # Iterar sobre las palabras para encontrarla
            for word in self.word_service.get_words():
                # Iterar sobre los lenguages
                for lan in word['translates']:
                    if lan == str(to_language['_id']):
                        if word['translates'][lan] == current_word:
                            to_list.append(word)
                            break
                        
        struct_from = list()
        struct_to = list()
        
        for fr in from_list:
            struct_from.append(fr['categories'][0])
        for to in to_list:
            struct_to.append(to['categories'][0])
        
        struct = StructModel(from_language, to_language, struct_from, struct_to)
        
        self.struct_service.add_struct(struct)
        print(struct)