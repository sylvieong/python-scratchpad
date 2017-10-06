import json

input_json = json.loads(open('./data/merged_annotations.json').read())

for annotation in input_json:
    print(annotation['filename'])

