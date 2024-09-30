import xml.etree.ElementTree as ET
import json

tree = ET.parse("JMdict_e")

root = tree.getroot()

json_dict = dict()
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
    for kele_entry in entry.findall('./k_ele'):
        keb = kele_entry.find('./keb').text
        if keb not in json_dict:
            json_dict[keb] = []
        json_dict[keb].extend(sense_list)
    for rele_entry in entry.findall('./r_ele'):
        reb = rele_entry.find('./reb').text
        if reb not in json_dict:
            json_dict[reb] = []
        json_dict[reb].extend(sense_list)
with open('JMdict_e.json', 'w') as fp:
    json.dump(json_dict, fp)