class StructService:
    def __init__(self, db):
        self.db = db
        
    def add_struct(self, struct_model):
        self.db['structs'].insert_one(struct_model.to_dict())
        
    def get_struct(self):
        return list(self.db['structs'].find())