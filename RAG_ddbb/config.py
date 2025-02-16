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
        return self.dict()

    @classmethod
    def deserialize(cls, data: dict):
        return cls(**data)