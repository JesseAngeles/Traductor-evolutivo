class LanguageModel:
    def __init__(self, language):
        self.language = language
        
    
    def to_dict(self):
        return {
            "language": self.language
        }