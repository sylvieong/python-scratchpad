"""
Map field names that appear in tool label to one of 9 required fields (or append
to list of extra_info.
Find and validate field values.
Return results as Pass/Fail for each field name and value, and for the label as a whole
(full and restricted list of fields)
"""

from collections import Sequence
from collections import OrderedDict

import sys
import string
import numpy as np
from nltk.metrics import distance


'''
validate_label that is returned in the result of the DSO is a dict() with this structure:
'''
default_output_result= {
 "label": {
    "present": True,
    "standard_full": "Fail",
    "standard_restricted": "Fail",
    "standard_full_fail_reason": " ",
    "standard_restricted_fail_reason": " "
 },
 "required_fields":{
    "property_of_unit": {
             "literal": ["",""],
             "standard":[ "Fail", "Fail"],
              "confidence": [-1, -1]},
    "inventory_number": {
            "literal": ["", ""],
            "standard": ["Fail", "Fail"],
            "confidence": [-1, -1]},
    "part_number" : {
            "literal": ["", ""],
            "standard": ["Fail", "Fail"],
            "confidence": [-1, -1]},
    "part_designation" : {
            "literal": ["", ""],
            "standard": ["Fail", "Fail"],
            "confidence": [-1, -1]},

    "project": {
            "literal": ["", ""],
            "standard": ["Fail", "Fail"],
            "confidence": [-1, -1]},

    "weight_kg" :  {
            "literal": ["", ""],
            "standard": ["Fail", "Fail"],
            "confidence": [-1, -1]},

    "dimension" :{
            "literal": ["", ""],
            "standard": ["Fail", "Fail"],
            "confidence": [-1, -1]},

    "issue_date" : {
            "literal": ["", ""],
            "standard": ["Fail", "Fail"],
            "confidence": [-1, -1]},

    "DUNS" : {
            "literal": ["", ""],
            "standard": ["Fail", "Fail"],
            "confidence": [-1, -1]}

  },
  "extra_info": []
}

class ValidateFieldsDSO():
    # TODO: enumerate set of 9 required fields

    # -----------------------
    # function match_literal_with_field()
    # returns one of 9 fields
    # what it does:
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

    # algo - more robust: to deal with 'AUDI Inventar-Nr2152601 -002\n\n', 'Teilenummen im 201 021',
    # 'Eigentum der Audi AG'
    # split token_to_match by space, keep appending the split results and
    # trying to match with literals in the dictionary till the match score starts decreasing
    # consider a match as found if the final match score is above a threshold
    # if there is a match,
    # return the matched field and the rest of the split results
    # else return None

    # how to match
    # - convert everything to lower case
    # - find some matching algo - levenstein distance?

    required_keys_list = ['property_of_unit', 'inventory_number', 'part_number', 'part_designation', 'project',
                          'weight_kg', 'dimension', 'issue_date', 'DUNS']

    fieldname_variations = OrderedDict()
    fieldname_variations['property_of_unit'] = ['property of unit', 'eigentum', 'eigentum der', 'kundeneigentum',
                                                'eigentum firma', 'eigentumproperty']
    fieldname_variations['inventory_number'] = ['inventory number', 'inventarnummer', 'invent-nr.', 'tool no.',
                                                'wekrzeugnummer', 'audi inventar-nr', 'audi inventarnummerinventorynumber', 'inventarnummer audi']
    fieldname_variations['part_number'] = ['part no', 'part number', 'teilenummer',  'audi teilenummer', 'audi teilenummerpartnumber']
    fieldname_variations['part_designation'] = ['part designation', 'part name', 'description', 'teilebenennung',
                                                'bezeichnung']
    fieldname_variations['project'] = ['project', 'vehicle object', 'fahrzeugprojekt']
    fieldname_variations['weight_kg'] = ['geewicht', 'swz gesamtgewicht', 'swzgesamtgewicht', 'tool weight', 'weight',
                                         'serial tool weight kg']
    fieldname_variations['dimension'] = ['dimension', 'dimension l w h', 'dimensions mm', 'abmessung']
    fieldname_variations['issue_date'] = ['issue date', 'erstelldatum', 'werkzeugerstellung','tool construction date',
                                          'baujahr', 'year of manuf', 'date of manufacture', 'year of manufacture']
    fieldname_variations['DUNS'] = ['duns', 'hersteller']

    def normalize(self,s):
        for p in string.punctuation:
            s = s.replace(p, '')
        return s.lower()  #.strip() 

    def match_literal_to_fieldname_variations(self, literal_to_match):
        fieldname_match_scores = []
        for fieldname, variations in self.fieldname_variations.items():
            g = lambda x: distance.edit_distance(x,self.normalize(literal_to_match))
            variations_match_scores= [g(x) for x in variations]
            fieldname_match_scores.append(min(variations_match_scores)/len(self.normalize(literal_to_match)))
        fieldname_match_scores_nparr = np.asarray(fieldname_match_scores)
        return np.argmin(fieldname_match_scores_nparr), np.min(fieldname_match_scores_nparr)


    def map_literal_to_field_char_level(self, input_tokens_to_match_string): 
        #print(f'In function {sys._getframe().f_code.co_name}')\
        ##DEBUG  print('In function {}'.format(sys._getframe().f_code.co_name))

        tokens_to_match_string = input_tokens_to_match_string.replace("?", " ")

        tokens_to_match_substring_match_scores = []
        tokens_to_match_substring_match_fieldname_indices = []

        for end_index in range(len(tokens_to_match_string),0,-1): # range(1,len(tokens_to_match_string)+1):
            literal_to_match = tokens_to_match_string[0:end_index]
            #DEBUG print('literal_to_match {}'.format(literal_to_match))

            match_fieldname_index,  match_score = self.match_literal_to_fieldname_variations(literal_to_match)
            tokens_to_match_substring_match_scores.append(match_score)
            tokens_to_match_substring_match_fieldname_indices.append(match_fieldname_index)
           
        tokens_to_match_substring_match_scores_nparr = np.asarray(tokens_to_match_substring_match_scores)
        min_index = np.argmin(tokens_to_match_substring_match_scores_nparr)

        return self.required_keys_list[tokens_to_match_substring_match_fieldname_indices[min_index]], \
        input_tokens_to_match_string[0: len(input_tokens_to_match_string)- min_index].strip(), \
        input_tokens_to_match_string[len(input_tokens_to_match_string)- min_index:].strip(), \
        np.min(tokens_to_match_substring_match_scores_nparr)

        #note: return the original input_tokens_to_match_string)
        #return field, field_name_str, tokens_to_add_to_rest_of_line_str, match_score
        #input_tokens_to_match_string[0: min_index+1].strip(), 
       # input_tokens_to_match_string[min_index+1:].strip(), 
 

    def map_literal_to_field(self, tokens_to_match):
        #print(f'In function {sys._getframe().f_code.co_name}')\
        print('In function {}'.format(sys._getframe().f_code.co_name))

        # replace "?" with space
        # strip leading and trailing space

        # split tokens_to_match
        tokens_to_match_list = tokens_to_match.split(" ")

        # TODO - change from exiting loop at local min to finding global min
        current_fieldname_min_score = 100
        current_fieldname_min_index = -1

        # TODO - take care of empty string in rest_of_tokens
        for end_index in range(1,len(tokens_to_match_list)+1):
            literal_to_match = " ".join(tokens_to_match_list[0:end_index])
            rest_of_tokens = " ".join(tokens_to_match_list[end_index:])

            #TEMP print('literal_to_match:{}'.format(literal_to_match))
            #TEMP print('rest_of_tokens:{}'.format(rest_of_tokens))

            fieldname_min_index,  fieldname_min_score = self.match_literal_to_fieldname_variations(literal_to_match)

            if (fieldname_min_score <= current_fieldname_min_score):
                current_fieldname_min_score = fieldname_min_score
                current_fieldname_min_index = fieldname_min_index
            else:
                break

        print('end_index: {}'.format(end_index))

        # match with literals in the dictionary
        # iterate through fieldname_variations and for each key, find max match score with its list of variations
        #fieldname_min_index,  fieldname_min_score = self.match_literal_fieldname_variations(tokens_to_match)
        #print(f'best matched field: {self.required_keys_list[fieldname_min_index ]}, score:{fieldname_min_score}')
        print('best matched field: {}, score:{}'.format(self.required_keys_list[current_fieldname_min_index],current_fieldname_min_score))

        # TODO - strip both strings that are returned

        return self.required_keys_list[current_fieldname_min_index], " ".join(tokens_to_match_list[0:end_index-1]), " ".join(tokens_to_match_list[end_index-1:])

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__()

    def calculate(self, dataset: Sequence):

        print('In function {}'.format(sys._getframe().f_code.co_name))

        output_result_list = []

        for item in dataset:
            print('OCR output for label:')
            print(item[2])
            print(item[3])
            input_word_list = item[2]
            input_confidence_value = item[3]

            output_result = default_output_result

            # ------------------------

            # ** for each line in input_word_list, find one of the 9 fields that it belongs to, or if not,
            # append to extra_info **

            # for each line:
            #   if line has >1 box, get leftmost box as matching token, join the rest of the boxes with space
            #  <--- still need to split leftmost by ":"
            #   else split text by ":" and get leftmost token, join the rest of the boxes together with ":"

            # get rid of \n\n, leading and trailing spaces

            #   try to match the leftmost box with a literal in the dictionary - call match_literal_with_field()
            #   if there is a match,
            #       append token to output_result.<returned_field>['literal']
            #       append rest of the line to output_result.<returned_field>['literal']
            #       append 'Pass' to output_result.<returned_field>['standard']
            #       if rest of the line is not empty or exists or there is a list:
            #           if returned_field is DUNS or inventory_number, validate the rest of the line, append result to
            #           output_result.<returned_field>['standard']
            #           else append 'Pass' to output_result.<returned_field>['standard']
            #       else append 'Fail' to output_result.<returned_field>['standard']
            #   else append whole line to extra_info

            # important - treat empty string returned from OCR, which is not the first string, as a value that was detected
            #

            for line in input_word_list:
                #print(f'line: {line}')
                print('line raw: {}'.format(line))

                # 1. remove \n   
                # 2. replace empty string with special symbol so that we know that a text box
                # was detected but OCR did not decipher any text
                for index, text_box in enumerate(line):
                    #DEBUG print('text_box: {}'.format(text_box ))
                    text_box = text_box.replace("\n", "")
                    #DEBUG print('text_box, after replacing slash n: {}'.format(text_box ))
                    if not text_box:
                        line[index] = '?'
                    else:
                        line[index] = text_box

                ##DEBUG print('line after processing empty strings: {}'.format(line))

                # get leftmost box as candidate for tokens to match with field, join the rest of the boxes with space
                # split leftmost box with ":" 
                # add any boxes except the leftmost box after the split, to the rest of the boxes
                leftmost_textbox_tokens_list = line[0].split(":")
                tokens_to_match_str = leftmost_textbox_tokens_list[0]
                tokens_to_match_str = tokens_to_match_str.strip()

                tokens_rest_of_leftmost_textbox_str = ':'.join(leftmost_textbox_tokens_list[1:])
                tokens_rest_of_leftmost_textbox_str = tokens_rest_of_leftmost_textbox_str.strip()

                ##DEBUG print('tokens_to_match_str: {}'.format(tokens_to_match_str))
                #DEBUG print('tokens_rest_of_leftmost_textbox_str: {}'.format(tokens_rest_of_leftmost_textbox_str))
                #DEBUG print(tokens_rest_of_leftmost_textbox_str)
                #DEBUG print('line[1:]: {}'.format(line[1:]))

                tokens_rest_of_line_str = ' '.join([tokens_rest_of_leftmost_textbox_str]+line[1:])
                tokens_rest_of_line_str = tokens_rest_of_line_str.strip()
                ##DEBUG print('tokens_rest_of_line_str: {}'.format(tokens_rest_of_line_str))

                # at this point, we are looking for the field name in tokens_to_match_str
                # and we assume that the field variable is tokens_rest_of_line_str, possibly pre-fixed with part of tokens_to_match_str

                if tokens_to_match_str == "?":
                    if tokens_rest_of_line_str:
                        output_result["extra_info"].append(["_",tokens_rest_of_line_str])
                else:
                    field, field_name_str, tokens_to_add_to_rest_of_line_str, match_score = self.map_literal_to_field_char_level(tokens_to_match_str)
                    print('field: {}'.format(field))
                    print('field_name_str: {}'.format(field_name_str))
                    ##DEBUG  print('tokens_to_add_to_rest_of_line_str: {}'.format(tokens_to_add_to_rest_of_line_str))
                    field_var_str = tokens_to_add_to_rest_of_line_str.strip() + ' ' + tokens_rest_of_line_str
                    print('field_var_str: {}'.format(field_var_str))
                    print('match_score: {}'.format(match_score))

            output_result_list.append(output_result)

        return output_result_list


                    #DEBUG print('tokens_to_match:')
                    #DEBUG print(tokens_to_match)
                    #DEBUG print('tokens_rest_of_leftmost_textbox:')
                    #DEBUG print(tokens_rest_of_leftmost_textbox)
                    #DEBUG print('line[1:]:')
                    #DEBUG print(line[1:])
