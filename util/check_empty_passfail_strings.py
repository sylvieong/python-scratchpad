import json

input_all = json.loads(open('./annotations-scratchpad/subparts01/annotations_all.json').read())


required_keys_list = ['property_of_unit', 'inventory_number', 'part_number', 'part_designation', 'project', 'weight_kg', 'dimension', 'issue_date', 'DUNS']

filename_key = 'filename'

for image in input_all:
    
    for subkey in ["standard_full", "standard_restricted"]:
        if not image['label'][subkey].lower().strip() in ['pass', 'fail']:
            print(f'file {image[filename_key]} incorrect label subkey values')
            
            
    for key in required_keys_list:
        for subkey in ['field_pass_fail', 'value_pass_fail']:
            if not image[key][subkey].lower().strip() in ['pass', 'fail']:
                print(f'file {image[filename_key]} incorrect {key} subkey values')
