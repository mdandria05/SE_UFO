from dataclasses import dataclass

@dataclass
class State:
    id: str
    lat: float
    lng: float
    weight: int

    def __eq__(self,other):
        return self.id == other.id
    def __hash__(self):
        return hash(self.id)