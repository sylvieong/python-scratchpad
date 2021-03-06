"""
Map field names that appear in tool label to one of 9 required fields (or append
to list of extra_info.
Find and validate field values.
Return results as Pass/Fail for each field name and value, and for the label as a whole
(full and restricted list of fields)
"""

from collections import Sequence
from collections import OrderedDict

import pandas as pd
import sys
import string
from nltk.metrics import distance
import numpy as np

from drw.workflow.hpc.experiment import RunResourceConfig
from mlaas.dso.base import CalculatorDSO
from mlaas.workflow.base import BaseDSOConfig


'''
validate_label that is returned in the result of the DSO is a dict() with this structure:
'''
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

class ValidateFieldsDSO(CalculatorDSO):
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
                                                'eigentum firma']
    fieldname_variations['inventory_number'] = ['inventory number', 'inventarnummer', 'invent-nr.', 'tool no.',
                                                'wekrzeugnummer']
    fieldname_variations['part_number'] = ['part no', 'part number', 'teilenummer',  'audi teilenummer']
    fieldname_variations['part_designation'] = ['part designation', 'part name', 'description', 'teilebenennung',
                                                'bezeichnung']
    fieldname_variations['project'] = ['project', 'vehicle object', 'fahrzeugprojekt']
    fieldname_variations['weight_kg'] = ['geewicht', 'swz gesamtgewicht', 'swzgesamtgewicht', 'tool weight', 'weight',
                                         'serial tool weight kg']
    fieldname_variations['dimension'] = ['dimension', 'dimension l w h', 'dimensions mm', 'abmessung']
    fieldname_variations['issue_date'] = ['issue date', 'erstelldatum', 'werkzeugerstellung','tool construction date',
                                          'baujahr', 'year of manuf', 'date of manufacture', 'year of manufacture']
    fieldname_variations['DUNS'] = ['duns', 'hersteller']

    def match_literal_fieldname_variations(self, literal_to_match):
        fieldname_match_scores = []
        for fieldname, variations in self.fieldname_variations.items():
            g = lambda x: distance.edit_distance(x,self.normalize(literal_to_match))
            variations_match_scores= [g(x) for x in variations]
            fieldname_match_scores.append(min(variations_match_scores))
        fieldname_match_scores_nparr = np.asarray(fieldname_match_scores)
        return np.argmin(fieldname_match_scores_nparr), np.min(fieldname_match_scores_nparr)

    def normalize(self,s):
        for p in string.punctuation:
            s = s.replace(p, '')
        return s.lower().strip()

    def map_literal_to_field(self, tokens_to_match):
        #print(f'In function {sys._getframe().f_code.co_name}')

        

        # match with literals in the dictionary
        # iterate through fieldname_variations and for each key, find max match score with its list of variations
        fieldname_min_index,  fieldname_min_score = self.match_literal_fieldname_variations(token_to_match)
        print(f'best matched field: {self.required_keys_list[fieldname_min_index ]}, score:{fieldname_min_score}')


        return 'dummy_field', ['dummy', 'tokens', 'to', 'add']



    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__()

    def calculate(self, dataset: Sequence, *, res_config: RunResourceConfig = None):

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
                print(f'line: {line}')

                if len(line) > 1:
                    pass
                    # get leftmost box as matching token, join the rest of the boxes with space
                    # split leftmost box with ":"

                else:
                    # split text by ":" and get leftmost token, join the rest of the boxes together with ":"
                    line_tokens = line[0].split(":")
                    tokens_to_match = line_tokens[0]
                    tokens_to_match = tokens_to_match.strip()
                    tokens_rest_of_line = ':'.join(line_tokens[1:])
                    tokens_rest_of_line = tokens_rest_of_line.strip()

                    #TODO get rid of \n at beginning, end and anywhere and replace with space?
                    # tokens_rest_of_line.strip()
                    print(f'tokens_to_match: {tokens_to_match}')
                    print(f'tokens_rest_of_line: {tokens_rest_of_line}')
                    field, tokens_to_add_to_rest_of_line = self.map_literal_to_field(tokens_to_match)

            output_result_list.append(dummy_output_result)

        return output_result_list


class ValidateFieldsDSO_Config(BaseDSOConfig, dso=ValidateFieldsDSO):

    # TODO: pass in the dictionary of synonyms as parameters?

    # TODO: remove this?
    params = str, {'default': '?', 'ui': {'hide': {'table': True, 'form': True}}}
