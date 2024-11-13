from sudachipy import dictionary
from sudachipy import SplitMode
from sudachipy import Morpheme
from JMdict_json import JMdict_json
from Kana import kata2hira, is_kana

def analyse_original_text(original_text: str, sudachi_dictionary: dictionary.Dictionary, 
                          jmdict_dictionary: JMdict_json) -> dict:
    """
    Analyse original Japanese text
    Parameters:
    -----
    original_text: Japanese text used for analysis
    sudachi_dictionary: Used for segmentation and phonetic annotation
    jmdict_dictionary: Used for retrieving English meaning
    -----
    
    Return json object (a Python dict):
    {
        "original_text": [
            -----
            phrase_obj:
            -----
            {
                "phrase": [
                    { "word": "国家", "kana": ["...", "..."], "index": 0 },
                    { "word": "公務", "kana": ["...", "..."], "index": 0 }
                    ...
                ],
                "meaning": {
                    "word": "国家公務員",
                    "list": ["...", "..."],
                    "index": 0
                }
            }
        ]
    }
    """
    result_obj = { "original_text": [] }

    original_lines = original_text.splitlines(False)
    for line in original_lines:
        result_obj["original_text"] += __generate_phrase_obj_list(line, sudachi_dictionary, jmdict_dictionary)
        result_obj["original_text"].append({
            "phrase": [ { "word": "\n", "kana": [], "index": -1 } ],
            "meaning": { "word": "\n", "list": [], "index": -1 } 
        })

    return result_obj

def __generate_phrase_obj_list(text: str, sudachi_dictionary: dictionary.Dictionary, 
                        jmdict_dictionary: JMdict_json) -> list:
    """
    Parameters:
    -----
    text: Japanese text used for analysis
    sudachi_dictionary: Used for segmentation and phonetic annotation
    jmdict_dictionary: Used for retrieving English meaning
    -----

    Return a phrase_obj list:
    [
        -----
        phrase_obj:
        -----
        {
            "phrase": [
                { "word": "国家", "kana": ["...", "..."], "index": 0 },
                { "word": "公務", "kana": ["...", "..."], "index": 0 }
                ...
            ],
            "meaning": {
                "word": "国家公務員",
                "list": ["...", "..."],
                "index": 0
            }
        }
    ]
    """
    result = []

    tokenizer_obj = sudachi_dictionary.create(mode=SplitMode.C)
    # Split the text into long phrases
    for phrase_m in tokenizer_obj.tokenize(text):
        # Lookup the phrase in the Japanese to English Dictionary (JMdict)
        if jmdict_dictionary.exists(phrase_m.dictionary_form()):
            phrase_obj = __generate_phrase_obj(phrase_m, sudachi_dictionary)
            if is_kana(phrase_m.dictionary_form()):
                phrase_obj["meaning"] = { "word": phrase_m.dictionary_form(), 
                                         "list": [], 
                                         "index": -1 }
            else:
                phrase_obj["meaning"] = { "word": phrase_m.dictionary_form(), 
                                         "list": jmdict_dictionary.lookup(phrase_m.dictionary_form(), phrase_m.part_of_speech()[0]), 
                                         "index": 0 }
            result.append(phrase_obj)
        else:
            # If phrase not exists in JMdict
            phrase_obj = __generate_phrase_obj(phrase_m, sudachi_dictionary)
            phrase_obj["meaning"] = { "word": phrase_m.dictionary_form(),
                                    "list": [], 
                                    "index": -1 }
            result.append(phrase_obj)
    return result

def __generate_phrase_obj(phrase_m: Morpheme, sudachi_dictionary: dictionary.Dictionary) -> dict:
    """
    1. Split the long phrase into short words
    2. Lookup word pronunciation in sudachi dictionary
    3. Return phrase_obj:
    {
        "phrase": [
            -----
            word_obj:
            -----
            { "word": "国家", "kana": ["...", "..."], "index": 0 },
            { "word": "公務", "kana": ["...", "..."], "index": 0 }
            ...
        ]
    }
    """
    phrase_obj = { "phrase": [] }
    # 1. Split the phrase into short word, get word pronunciation(in kana format)
    for word_m in phrase_m.split(SplitMode.A):
        word_obj = dict()
        # kana: possible pronunciations for the word(a list)
        # index: index of the currently selected pronunciation in the list
        word_obj["word"] = word_m.raw_surface()
        word_obj["kana"] = []
        word_obj["index"] = -1
        if word_obj["word"] not in (' ', '\u3000', '（', '）'):
            kana = kata2hira(word_m.reading_form())
            if kana != "きごう" or word_obj["word"] in ("記号", "揮毫"):
                if len(kana) > 0 and word_obj["word"] != kana:
                    word_obj["kana"].append(kana)
                    word_obj["index"] = 0
                # 3. Look up the dictionary, add all possible pronunciations to the list
                for entry in sudachi_dictionary.lookup(word_obj["word"]):
                    kana = kata2hira(entry.reading_form())
                    if word_obj["word"] != kana and kana not in word_obj["kana"]:
                        word_obj["kana"].append(kana)
        phrase_obj["phrase"].append(word_obj)
    return phrase_obj