class WordModel:
    def __init__(self, categories, translates):
        self.categories = categories
        self.translates = translates
        
    def to_dict(self):
        return {
            "categories" : self.categories,
            "translates" : self.translates
        }
        