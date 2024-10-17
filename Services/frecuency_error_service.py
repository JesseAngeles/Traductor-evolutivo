class FrecuencyErrorService:
    def __init__(self, db):
        self.db = db
    
    def add_frecuency_error(self, frecuency_error):
        self.db['frecuency_errors'].insert_one(frecuency_error.to_dict())
        
    def get_frecuency_errors(self):
        return list(self.db['frecuency_errors'].find())
    
    def update_frecuency_error(self, frecuency_error):
        # Utilizar replace_one para reemplazar el documento completo basado en el _id
        self.db['frecuency_errors'].replace_one(
            {"_id": frecuency_error['_id']},  # Busca por el _id
            frecuency_error  # Reemplaza con el nuevo documento
        )