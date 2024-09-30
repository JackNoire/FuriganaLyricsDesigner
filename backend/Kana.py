HIRAGANA = list('ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすず'
                'せぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴ'
                'ふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろわ'
                'をんーゎゐゑゕゖゔゝゞ')
KATAKANA = list('ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズ'
                'セゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピ'
                'フブプヘベペホボポマミムメモャヤュユョヨラリルレロワ'
                'ヲンーヮヰヱヵヶヴヽヾ')

def kata2hira(text: str) -> str:
    translate_dict = dict(zip(KATAKANA, HIRAGANA))
    result_list = []
    for character in text:
        if character in translate_dict:
            result_list.append(translate_dict[character])
    result_str = ''.join(result_list)
    return result_str

def is_kana(text: str) -> bool:
    return len(text) == 1 and (text in HIRAGANA or text in KATAKANA)