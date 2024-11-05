import xml.etree.ElementTree as ET
import json

tree = ET.parse("JMdict_e")

root = tree.getroot()

"""
json_dict
{
"keb_word": [meaning1, meaning2],
"reb_word": [meaning1, (keb_str)meaning2]
reb_word w/o keb_str is listed before reb_word with keb_str
}
"""

json_dict = dict()

# temp dict to store {reb: (keb_str)meaning}
json_dict_2 = dict()

for entry in root.findall('./entry'):
    print(int(entry.find('./ent_seq').text))
    sense_list = []
    for sense_entry in entry.findall('./sense'):
        gloss_str = ""
        for gloss_entry in sense_entry.findall('./gloss'):
            if len(gloss_str) == 0:
                gloss_str += gloss_entry.text
            else:
                gloss_str += "; " + gloss_entry.text
        sense_list.append(gloss_str)
    
    keb_str = ""
    for kele_entry in entry.findall('./k_ele'):
        keb = kele_entry.find('./keb').text
        if len(keb_str) == 0:
            keb_str += keb
        else:
            keb_str += "; " + keb
        
        if keb not in json_dict:
            json_dict[keb] = []
        json_dict[keb].extend(sense_list)
    
    # If keb_str exists, prepend it to the beginning of each meaning
    if len(keb_str) > 0:
        for i in range(len(sense_list)):
            sense_list[i] = "(" + keb_str + ")" + sense_list[i]

    for rele_entry in entry.findall('./r_ele'):
        reb = rele_entry.find('./reb').text
        if reb not in json_dict:
            json_dict[reb] = []
        if reb not in json_dict_2:
            json_dict_2[reb] = []
        
        if len(keb_str) == 0:
            json_dict[reb].extend(sense_list)
        else:
            json_dict_2[reb].extend(sense_list)
for reb, meaning_list in json_dict_2.items():
    json_dict[reb].extend(meaning_list)

with open('JMdict_e.json', 'w') as fp:
    json.dump(json_dict, fp)