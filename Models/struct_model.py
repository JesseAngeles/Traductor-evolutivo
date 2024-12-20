class StructModel:
    def __init__(self, lan_from, lan_to, struct_from, struct_to):
        self.lan_from = lan_from
        self.lan_to = lan_to
        self.struct_from = struct_from
        self.struct_to = struct_to
        
    def to_dict(self):
        return {
            "language_from": self.lan_from,
            "language_to": self.lan_to,
            "struct_from": [
                item.to_dict() if hasattr(item, "to_dict") else item for item in self.struct_from
            ],
            "struct_to": [
                item.to_dict() if hasattr(item, "to_dict") else item for item in self.struct_to
            ]
        }