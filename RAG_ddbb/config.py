from pydantic import BaseModel
import json

class Config(BaseModel):
    type_db: str
    user: str
    password: str
    host: str
    port: str
    database_name: str
    def serialize(self):
        """Método para serializar la clase en un JSON."""
        return json.dumps(self.dict())

    @classmethod
    def deserialize(cls, json_str: str):
        """Método para deserializar un JSON en una instancia de la clase Config."""
        config_dict = json.loads(json_str)
        return cls(**config_dict)