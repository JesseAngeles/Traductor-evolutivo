class CategoryModel:
    def __init__(self, category):
        self.category = category
        
    
    def to_dict(self):
        return {
            "category": self.category
        }