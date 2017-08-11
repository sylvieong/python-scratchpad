import pickle
import json
import string
from collections import OrderedDict


def normalize(s):
    for p in string.punctuation:
        s = s.replace(p, '')
    return s.lower().strip()



required_keys_list = ['property_of_unit', 'inventory_number', 'part_number', 'part_designation', 'project', 'weight_kg', 'dimension', 'issue_date', 'DUNS']


#for key in required_keys_list:                  # do this just so that keys will be in the right order
#    fieldname_variations_merged[key] = []

annotations = json.loads(open('./data/merged_annotations.json').read())

fieldname_variations_from_annotations= dict()
for key in required_keys_list:
    fieldname_variations_from_annotations[key] = []

for annotation in annotations:
    for key in required_keys_list:
        if annotation[key]["field_pass_fail"] == "Pass":
                fieldname_variations_from_annotations[key].append(normalize(annotation[key]["field_text_literal"]))
                
print(fieldname_variations_from_annotations)

fieldname_variations_from_code = json.loads(open('./data/fieldname_variations_code.json').read())
                
# fieldname_variations_from_annotations is dict with list of variations for each field_pass_fail
# fieldname_variations_from_code is dict with list of variations for each field_pass_fail

# merge the two and write to fieldname_variations_merged
fieldname_variations_merged = OrderedDict()
for key in required_keys_list:
    fieldname_variations_merged[key] = list(set(fieldname_variations_from_code[key]) | set(fieldname_variations_from_annotations[key]))

# write fieldname_variations_merged to json file
with open('./data/fieldname_variations_merged.json','w') as outfile:
    json.dump(fieldname_variations_merged, outfile)

