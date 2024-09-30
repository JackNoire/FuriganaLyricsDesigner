import json
from typing import Optional

class JMdict_json:
    def __init__(self, json_path='./JMdict_e.json') -> None:
        with open(json_path, 'r') as f:
            self.JMdict = json.load(f)
    
    def exists(self, word: str) -> bool:
        return word in self.JMdict

    def lookup(self, word: str) -> Optional[list]:
        if word in self.JMdict:
            return self.JMdict[word]
        return None