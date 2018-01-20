import os

TYPES = ['8', '1s', '>1s', '10+', '12+', 'alg', 'All types']
ALL_TYPES = TYPES[-1]

CURRENT_DIR = os.path.dirname(__file__)

PATH_TO_JSON = CURRENT_DIR + '\\data\\corners.json'
PATH_TO_BACKUP_JSON = CURRENT_DIR + '\\data\\corners.json.backup'

CORNERS = 'corners'
ALG = 'alg'
BAD_ANSWERS = 'badAnswers'
GOOD_ANSWERS = 'goodAnswers'
CHECKED = 'checked'
STICKER1 = 'sticker1'
STICKER2 = 'sticker2'
TYPE = 'type'

MAIN_MENU = ('List of available commends:\n\n'
             '\t1 - Train commutators\n'
             '\t2 - Add commutators\n'
             '\t3 - Check correctness of commutators\n'
             '\t4 - Sort dictionary by stickers\n'
             '\t5 - Set all scores to 0\n'
             '\t6 - Dictionary backup\n'
             '\t0 - Save and exit\n')

WORKTYPE_MENU = ('List of available types of commutators:\n\n'
                 '\t0 - 8 moves\n'
                 '\t1 - 8 moves with 1 setup\n'
                 '\t2 - 8 moves with more than 1 setup\n'
                 '\t3 - 10 moves (including with setups)\n'
                 '\t4 - 12 moves (including with setups)\n'
                 '\t5 - Variations of permutation A\n'
                 '\t6 - All of above types\n')
