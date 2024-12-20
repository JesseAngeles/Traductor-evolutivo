class WordService:
    def __init__(self, db):
        self.db = db
    
    def add_word(self, word_model):
        self.db['words'].insert_one(word_model.to_dict())
        
    def get_words(self):
        return list(self.db['words'].find())
    
    def update_word(self, word_id, word_model):
        result = self.db['words'].update_one(
            {'_id': word_id},  # Filtro para encontrar el documento
            {'$set': word_model}  # Actualización
        )
        return result.matched_count > 0