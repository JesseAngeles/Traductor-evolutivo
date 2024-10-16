class CategoryService:
    def __init__(self, db):
        self.db = db
        
    def add_category(self, category_model):
        self.db['categories'].insert_one(category_model.to_dict())
        
    def get_categories(self):
        return list(self.db['categories'].find())