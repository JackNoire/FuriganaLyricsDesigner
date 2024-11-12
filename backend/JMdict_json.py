import json
from typing import Optional

# From: https://github.com/alexxander/analyzer
jmdictToUnidic = {
  'symbol': ['補助記号'],
  'adj-f': ['形容詞'],
  'adj-i': ['形容詞'],
  'adj-ix': ['形容詞'],
  'adj-ku': [],
  'adj-na': ['形状詞'],
  'adj-nari': ['形状詞'],
  'adj-no': ['名詞'],
  'adj-pn': ['連体詞'],
  'adj-shiku': [],
  'adj-t': [],
  'adv': ['副詞'],
  'adv-to': ['副詞'],
  'aux': ['助詞'],
  'aux-adj': ['形容詞'],
  'aux-v': ['助動詞'],
  'conj': ['接続詞'],
  'cop': ['助動詞'],
  'ctr': ['名詞'],
  'exp': ['助動詞'],
  'int': ['感動詞'],
  'n': ['名詞'],
  'n-adv': ['名詞'],
  'n-pref': ['名詞'],
  'n-suf': ['名詞'],
  'n-t': ['名詞'],
  'num': ['名詞'],
  'pn': ['代名詞'],
  'pref': ['接頭辞'],
  'prt': ['助詞', '助動詞'],
  'suf': ['接尾辞'],
  'unc': [''],
  'v1': ['動詞'],
  'v1-s': ['動詞'],
  'v2a-s': ['動詞'],
  'v2b-k': ['動詞'],
  'v2d-s': ['動詞'],
  'v2g-k': ['動詞'],
  'v2g-s': ['動詞'],
  'v2h-k': ['動詞'],
  'v2h-s': ['動詞'],
  'v2k-k': ['動詞'],
  'v2k-s': ['動詞'],
  'v2m-s': ['動詞'],
  'v2n-s': ['動詞'],
  'v2r-k': ['動詞'],
  'v2r-s': ['動詞'],
  'v2s-s': ['動詞'],
  'v2t-k': ['動詞'],
  'v2t-s': ['動詞'],
  'v2w-s': ['動詞'],
  'v2y-k': ['動詞'],
  'v2y-s': ['動詞'],
  'v2z-s': ['動詞'],
  'v4b': ['動詞'],
  'v4g': ['動詞'],
  'v4h': ['動詞'],
  'v4k': ['動詞'],
  'v4m': ['動詞'],
  'v4r': ['動詞'],
  'v4s': ['動詞'],
  'v4t': ['動詞'],
  'v5aru': ['動詞'],
  'v5b': ['動詞'],
  'v5g': ['動詞'],
  'v5k': ['動詞'],
  'v5k-s': ['動詞'],
  'v5m': ['動詞'],
  'v5n': ['動詞'],
  'v5r': ['動詞'],
  'v5r-i': ['動詞'],
  'v5s': ['動詞'],
  'v5t': ['動詞'],
  'v5u': ['動詞'],
  'v5u-s': ['動詞'],
  'vi': ['動詞'],
  'vk': ['動詞'],
  'vn': ['動詞'],
  'vr': ['動詞'],
  'vs': ['動詞'],
  'vs-c': ['動詞'],
  'vs-i': ['動詞'],
  'vs-s': ['動詞'],
  'vt': ['動詞'],
  'v-unspec': ['動詞'],
  'vz': ['動詞'],
}

class JMdict_json:
    def __init__(self, json_path='./JMdict_e.json') -> None:
        """
        JMdict_e.json:
        {"word": [
        [[pos1, pos2], meaning1],
        [[pos1, pos2], meaning2]
        ]}
        """
        with open(json_path, 'r') as f:
            self.JMdict = json.load(f)
    
    def exists(self, word: str) -> bool:
        return word in self.JMdict

    def lookup(self, word: str, pos: str) -> Optional[list]:
        """
        Lookup word, return meaning list
        pos: part of speech (in Unidic form, 名詞/動詞/形容詞...)
        Return: ["meaning1", "meaning2"]
        """
        if word in self.JMdict:
            sense_list = self.JMdict[word]
            # Place meaning with correct POS before meaning with wrong POS
            pos_correct_list = []
            pos_wrong_list = []
            for pos_list, meaning in sense_list:
                isPosCorrect = False
                for curr_pos in pos_list:
                    if curr_pos in jmdictToUnidic:
                        isPosCorrect = isPosCorrect or (pos in jmdictToUnidic[curr_pos])
                    if isPosCorrect:
                        break
                if isPosCorrect:
                    pos_correct_list.append(meaning)
                else:
                    pos_wrong_list.append(meaning)
            return pos_correct_list + pos_wrong_list
        else:
            return None