class LanguageService:
    def __init__(self, db):
        self.db = db
        
    def add_language(self, language_model):
        self.db['languages'].insert_one(language_model.to_dict())
        
    def get_languages(self):
        return list(self.db['languages'].find())