import unittest

from drw.workflow.blob_list import BlobList
from drw.workflow.content_type import ContentType
from drw.workflow.data import BlobDatum
from drw.workflow.storage.block import Block
from mlaas.solutions.audi.ocr_dev.validate_fields_dso import ValidateFieldsDSO_Config


class TestValidateFieldsDSO(unittest.TestCase):

    def setUp(self):
        """
        create dataset from tuples of output from ocr_dso
        writes generator created from the dataset to self.data
        :return:
        """

        # data output from ocr_dso looks like:
        # label_detected, boxes, ocr.label_txt_pair, ocr.label_conf_pair
        # result_list # list of tuples, where each tuple looks like: label_detected, boxes, ocr.label_txt_pair, ocr.label_conf_pair

        # THE FILE NAME IS:  Labels/4_2_Blow_mold_MA_3202560_2.jpg
        label_txt_pair0 = [ ['Teilebenennung: Montagevorrichtung', 'Aufschuss EFR-LZS'],
                            ['D-U-N-S: 312968706'],
                            ['AUDI lnventar-Nr2152601 -002'],
                            ['Fahrzeugprojekt: P0 416'],
                            ['Teilenummer: 8R0 201 021'],
                            ['Eigentum der AUDI AG'],
                            ['Erstelldatum: Nov. 2013'] ]
        label_conf_pair0 =[ [[79, 83], [89, 80]],
                            [[81, 82]],
                            [[82, 64, 74]],
                            [[79, 89, 78]],
                            [[80, 88, 87, 85]],
                            [[88, 91, 92, 90]],
                            [[84, 88, 85]] ]

        #THE FILE NAME IS: Labels / 4_2_Blow_mold_MA_3202560_8.jpg
        label_txt_pair1 = [ ['Invenhmummer Audi: 2152601405'],
        ['Teilebenennung: Ladungslrägor EFR'],
        ['Werkzeugelshellung: Nov. 2013'],
        ['Fahneugpcojekl: ro 416'],
        ['Teilenummen im 201 021'],
        ['Eigentum der Audi AG'] ]

        label_conf_pair1 = [ [['67', '72', '56']],
        [['74', '69', '78']],
        [['69', '85', '71']],
        [['71', '71', '74']],
        [['74', '63', '88', '90']],
        [['78', '75', '77', '76']] ]

        # THE FILE NAME IS:  Labels/4_2_Extrusion_tool_MA_3284664_2.jpg
        label_txt_pair2 = [ ['Abmessung:', '', 'HERST. DAT. 08/201677'],
        ['', ''],
        ['Eigentum der\n\n3 nt:', ''],
        ['lnventamr.', ''],
        ['D-U-N-S', ''],
        ['', '', 'JEILE-NR. USM 103 210 CH'],
        ['ErsIeHdufum:', ''],
        ['bläbmonnung:', '', 'WK. NR.', '1012657'],
        ['Gewicht:', '', 'EEZ. Druckprüileisle'] ]

        label_conf_pair2 = [ [['69'], ['-1'], ['87', '91', '22']],
[['-1'], ['-1']],
[['73', '84', '56', '49'], ['-1']],
[['64'], ['-1']],
[['85'], ['-1']],
[['-1'], ['-1'], ['68', '71', '78', '79', '84']],
[['69'], ['-1']],
[['47'], ['-1'], ['93', '86'], ['95', '78']],
[['59'], ['-1'], ['49', '75']] ]

        # THE FILE NAME IS:  Labels/4_2_Foaming_tool_MA_3173300.jpg
        label_txt_pair3 = [ ['Audi Teilenummer/Partnumber', '8V5 012 109 C/D'],
['Eigentum/Property', 'AUDI AG'],
['Audi lnventarnummer/lnventorynumber', '2145323'],
[''] ]

        label_conf_pair3 = [[['94', '88'], ['93', '89', '89', '93']],
[['86'], ['95', '91']],
[['93', '89'], ['87']],
[['-1']]]

        # THE FILE NAME IS:  Labels/4_2_Foaming_tool_MA_3193397_3.jpg
        label_txt_pair4 = [['Xvazuuqngmmer', '1616 60011958', 'SCHAUMWERKZEUG 5- NUTZEN'],
['Ten f Nummer', '', ''],
['Teil Bezeichnung', '- .v.\n\nU G SQHALTUNG HAND'],
['KWV', '', 'Agusm\n\nls.-'],
['Eigentum', 'AUDI AG'],
['', '', 'Gewicht Ikgl', 'SchwindmaB D/o', '1.39', '225'],
['', ''],
['k 7 wimmenal', '6116 60011958', '1SCHAUK/TWERKZEUG 5- NUTZEN-'],
['KWV', 'Y1L79l-Sm'],
['WNkz-eugart', '64149ng\ntSCHAUMWERKZEUG 5- NUTZEN\n\nn de Anne nnnnnnen -'],
['', 'Mmic dä x T x m hmm', '770x418x314', 'Gewicht Ikgl', '225'],
['', ''],
['Teilenummer: .BSO 863 878'],
['WERKZEUGDATEN'],
['lnventarnummer: 0702983001']]

        label_conf_pair4 = [[['47', '95'], ['95', '88', '80'], ['95', '87', '92', '88']],
[['70', '34', '80'], ['-1'], ['-1']],
[['17', '73'], ['78', '59', '93', '93', '63', '82', '95', '95', '95']],
[['54'], ['-1'], ['95', '44', '76']],
[['82'], ['92', '89']],
[['-1'], ['-1'], ['79', '72'], ['68', '73'], ['87'], ['90']],
[['-1'], ['-1']],
[['95', '72', '52', '48'], ['95', '88', '80'], ['47', '89', '49']],
[['54'], ['47']],
[['48'], ['18', '56', '93', '88', '79', '63', '61', '63', '65']],
[['-1'], ['56', '51', '68', '75', '62', '66', '64'], ['80'], ['79', '72'], ['90']],
[['-1'], ['-1']],
[['84', '25', '82', '83']],
[['84']],
[['82', '78']]]

        tuple0 = ( True, [1,2], label_txt_pair0, label_conf_pair0 )
        tuple1 = ( True, [1,2], label_txt_pair1, label_conf_pair1 )
        tuple2 = ( True, [1,2], label_txt_pair2, label_conf_pair2 )
        tuple3 = ( True, [1,2], label_txt_pair3, label_conf_pair3 )
        tuple4 = ( True, [1,2], label_txt_pair4, label_conf_pair4 )

        result_list = [tuple0, tuple1, tuple2, tuple3, tuple4]

        self.data = (result for result in result_list)

        # note that in the dtg, the data passed out of the ocr DSO will include celph_file etc, and we would do:
        # has_label, lines_cleaned, label_txt_pair, label_conf_pair = data['ocr_result']

    def test_1(self):
        print('debug validate fields dso')

        model_config = ValidateFieldsDSO_Config()
        model_dso = model_config.get_dso()
        result = model_dso.calculate(self.data) #, res_config=res_config)

        print('Result:')
        for item in result:
            print(item)



        print('\ndone!')


        # example of assertion test
        # expected_result = ['outlier']
        #
        # h = InsuranceHeuristic_Age()
        #
        # actual_result = h.calculate(dataset=None)
        #
        #
        # self.assertEquals(actual_result, expected_result)
        #
