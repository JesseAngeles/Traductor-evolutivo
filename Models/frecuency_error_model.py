class FrecuencyErrorModel:
    def __init__(self, word, corrections):
        self.word = word
        self.corrections = corrections
        
    def to_dict(self):
        return {
            "word": self.word,
            "corrections": self.corrections
        }