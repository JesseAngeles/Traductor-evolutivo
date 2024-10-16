class WordService:
    def __init__(self, db):
        self.db = db
    
    def add_word(self, word_model):
        self.db['words'].insert_one(word_model.to_dict())
        
    def get_words(self):
        return list(self.db['words'].find())