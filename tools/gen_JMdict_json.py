from lxml import etree
import json
import copy

tree = etree.parse("JMdict_e")

dtd_entities = tree.docinfo.internalDTD.entities()

# {"noun or verb acting prenominally": "adj-f", 
# "adjective (keiyoushi)": "adj-i", ...}
entityValueToName = {}

for entity in dtd_entities:
    entityValueToName[entity.content] = entity.name

root = tree.getroot()

"""
json_dict
{
"keb_word": [[[pos1, pos2], meaning1], [[pos1], meaning2]],
"reb_word": [[[pos1, pos2], meaning1], [[pos1], (keb_str)meaning2]]
reb_word w/o keb_str is listed before reb_word with keb_str
}
"""

json_dict = dict()

# temp dict to store meaning with lower priority
# For reb word, meaning with keb_str has lower priority
# {reb: [[[pos1, pos2], (keb_str)meaning]]}
json_dict_2 = dict()

for entry in root.findall('./entry'):
    print(int(entry.find('./ent_seq').text))

    # json_dict: {"word": sense_list}
    # sense_list = [[[pos1, pos2], meaning1], [[pos1], meaning2]]
    # sense_list[0] = [[pos1, pos2], meaning1]
    # sense_list[0][0] = [pos1, pos2]
    # sense_list[0][1] = meaning1
    sense_list = []
    # sense_list_uk: sense with <misc>&uk;</misc> (Usually Kana)
    # sense_list_no_uk: sense w/o <misc>&uk;</misc>
    # sense_list_uk + sense_list_no_uk = sense_list
    sense_list_uk = []
    sense_list_no_uk = []

    for sense_entry in entry.findall('./sense'):
        pos_list = []
        gloss_str = ""
        withUk = False
        for gloss_entry in sense_entry.findall('./gloss'):
            if len(gloss_str) == 0:
                gloss_str += gloss_entry.text
            else:
                gloss_str += "; " + gloss_entry.text
        for pos_entry in sense_entry.findall('./pos'):
            pos_list.append(entityValueToName[pos_entry.text])
        for misc_entry in sense_entry.findall('./misc'):
            if entityValueToName[misc_entry.text] == "uk":
                withUk = True
                break
        sense_list.append([pos_list, gloss_str])
        if withUk:
            sense_list_uk.append([pos_list, gloss_str])
        else:
            sense_list_no_uk.append([pos_list, gloss_str])
    
    keb_str = ""
    for kele_entry in entry.findall('./k_ele'):
        keb = kele_entry.find('./keb').text
        if len(keb_str) == 0:
            keb_str += keb
        else:
            keb_str += "; " + keb
        
        if keb not in json_dict:
            json_dict[keb] = []
        json_dict[keb].extend(copy.deepcopy(sense_list))
    
    # If reb's meaning: 1) has keb_str; 2) no uk(usually kana); Then lower the priority of this meaning
    # prepend keb_str to the beginning of such meanings
    if len(keb_str) > 0:
        for i in range(len(sense_list_no_uk)):
            sense_list_no_uk[i][1] = "(" + keb_str + ")" + sense_list_no_uk[i][1]

    for rele_entry in entry.findall('./r_ele'):
        reb = rele_entry.find('./reb').text
        if reb not in json_dict:
            json_dict[reb] = []
        if reb not in json_dict_2:
            json_dict_2[reb] = []
        
        if len(keb_str) == 0:
            # If no keb_str, simply extend original sense_list
            json_dict[reb].extend(copy.deepcopy(sense_list))
        else:
            # If keb_str, no_uk meanings have lower priority
            json_dict[reb].extend(copy.deepcopy(sense_list_uk))
            json_dict_2[reb].extend(copy.deepcopy(sense_list_no_uk))
for reb, meaning_list in json_dict_2.items():
    json_dict[reb].extend(meaning_list)

with open('JMdict_e.json', 'w') as fp:
    json.dump(json_dict, fp)