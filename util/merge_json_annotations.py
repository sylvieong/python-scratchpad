import pickle
import json

input_bad_labels = json.loads(open('./data/Bad_Labels_annos.json').read())
input_bad_labels_filtered = [y for y in input_bad_labels if y['filename']]
input_good_labels = json.loads(open('./data/Labels_annotations-Kyle.json').read())
merged_annotations = input_good_labels + input_bad_labels_filtered

pickle.dump(merged_annotations, open("./data/merged_annotations.p", "wb"))

with open('./data/merged_annotations.json','w') as outfile:
    json.dump(merged_annotations, outfile)
    
print(f'Done! Num annotations in Labels/: {len(input_good_labels)}, Num annotations in Bad_Labels/: {len(input_bad_labels_filtered)}, Total num: {len(merged_annotations)}')
