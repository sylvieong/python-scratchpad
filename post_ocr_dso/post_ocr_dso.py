# pseudo code post OCR processing

# assume the input is two lists - input_word_list, input_confidence_value_list
# # TODO: figure out what to do with input_confidence_value_list

# example input
#input_word_list=['Eigentum der AUDI AG'],['Teilenummer','8V7 837 249'],['Teilebenennung','Turieststeller']]
#input_confidence_value_list=[ [ [80, 81, 82, 83] ], [ [84], [85, 86, 87] ],[ [88], [89] ]]


label_txt_pair1 = [ ['Teilebenennung: Montagevorrichtung', 'Aufschuss EFR-LZS'],
                    ['D-U-N-S: 312968706'],
                    ['AUDI lnventar-Nr2152601 -002'],
                    ['Fahrzeugprojekt: P0 416'],
                    ['Teilenummer: 8R0 201 021'],
                    ['Eigentum der AUDI AG'],
                    ['Erstelldatum: Nov. 2013'],
                    ["Dimensions: L: 500 W: 500 H:460"] ]
label_conf_pair1 =[ [[79, 83], [89, 80]],
                    [[81, 82]],
                    [[82, 64, 74]],
                    [[79, 89, 78]],
                    [[80, 88, 87, 85]],
                    [[88, 91, 92, 90]],
                    [[84, 88, 85]] ]
tuple1 = ( True, [1,2], label_txt_pair1, label_conf_pair1 )
#result_list = [tuple1, tuple1, tuple1, tuple1, tuple1]


# example structured output
dummy_output_result= {
 "label": {
    "present": True,
    "standard_full": "Pass",
    "standard_restricted": "Pass",
    "standard_full_fail_reason": " ",
    "standard_restricted_fail_reason": " "
 },
 "required_fields":{
    "property_of_unit": {
             "literal": ["Property of","AUDI AG"],
             "standard":[ "Pass", "Pass"],
              "confidence": [90, 90]},
    "inventory_number": {
             "literal": ["Inventory number","2164861-001"],
             "standard": [ "Pass","Pass"],
              "confidence": [90, 90]},
    "part_number" : {
             "literal": ["Part number","4M0 121 146"],
             "standard": [ "Pass", "Pass"],
              "confidence": [90, 90]},
    "part_designation" : {
             "literal": ["Part designation","ABSCHIRMUNG GETRIEBERUECKEN"],
             "standard": [ "Pass", "Pass"],
              "confidence": [90, 90]},
    "project": {
             "literal": ["Project","MLB53A PHEV"],
             "standard": [ "Pass", "Pass"],
              "confidence": [90, 90]},
    "weight_kg" :  {
             "literal": ["Weight","495"],
             "standard": [ "Pass", "Pass"],
              "confidence": [90, 90]},
    "dimension" :{
             "literal": ["Dimensions","L: 500 W: 500 H:460"],
             "standard": [ "Pass", "Pass"],
              "confidence": [90, 90]},
    "issue_date" : {
             "literal": ["Date of manufacture","01/12/2014"],
             "standard": [ "Pass", "Pass"],
              "confidence": [90, 90]},
    "DUNS" : {
             "literal":["D-U-N-S","422349308"],
             "standard": [ "Pass", "Pass"],
             "confidence": [90, 90] }
  },
  "extra_info": []
}



# enumerate set of possible 9 fields 

#-----------------------
# function match_literal_with_field()
# returns one of 9 fields
# match token with literal in dictionary
# dict_eight = { 'part_number' : [part number', ... ], 
#          'inventory_number' : ['inventory number', ...],
#       }

# dict_property_of_unit

# algo
# go through each key in dict_eight and find max match with the literals in its list
# get the max match across the keys, 
# if it is higher than a threshold, consider it a match, return the matched key
# else try to do smart matching wih literals in dict_property_of_unit, 
# if there is a match, return property_of_unit 
# else return None


#------------------------
# what to do with AUDI Inventar-Nr2152601 -002\n\n

#------------------------

#** for each line in input_word_list, find one of the 9 fields that it belongs to, or if not, append to extra_info **

# for each line:
#   if line has >1 box, get leftmost box as matching token, join the rest of the boxes with space <--- still need to split by ":"
#   else split text by ":" and get leftmost token, join the rest of the boxes together with ":"

# get rid of \n\n, leading and trailing spaces

#   try to match the leftmost box with a literal in the dictionary - call match_literal_with_field()
#   if there is a match, 
#       append token to output_result.<returned_field>['literal']
#       append rest of the line to output_result.<returned_field>['literal']
#       append 'Pass' to output_result.<returned_field>['standard']
#       if rest of the line is not empty or exists or there is a list:
#           if returned_field is DUNS or inventory_number, validate the rest of the line, append result to output_result.<returned_field>['standard']
#           else append 'Pass' to output_result.<returned_field>['standard']
#       else append 'Fail' to output_result.<returned_field>['standard']


#   else append whole line to extra_info

item = tuple1
input_word_list = item[2]
input_confidence_value = item[3]

print(item[2])
print(item[3])

for line in input_word_list:
    print(line)

    if len(line)>1:
        pass
        #get leftmost box as matching token, join the rest of the boxes with space 
        #split leftmost box with ":"

    else:
        #split text by ":" and get leftmost token, join the rest of the boxes together with ":"
        line_tokens = line[0].split(":")
        token_to_match =  line_tokens[0]
        token_to_match=token_to_match.strip()
        tokens_rest_of_line = ':'.join(line_tokens[1:])
        tokens_rest_of_line = tokens_rest_of_line.strip()
        #tokens_rest_of_line.strip()
        print(token_to_match)
        print(tokens_rest_of_line)
