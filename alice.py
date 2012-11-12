cards = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
suits = ['S','H','C','D']
suits_threes = [[suits[0],suits[1],suits[2]],[suits[1],suits[2],suits[3]],[suits[0],suits[1],suits[3]],[suits[0],suits[2],suits[3]]]

order = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']

all_cards_order = [y+x for x in order for y in suits]

word_scores = {'ANDRIES':21,'CRUELTY':70,'DANDIES':13,'DRACHMA':50,'DRUMMER':49,'EYEBROW':28,'GAMIEST':31,'GASPERS':43,'MAESTRO':39,'MERCURY':67,'NOVELTY':70,'PERTAIN':55,'PINCERS':49,'PRAISED':13,'REVISED':34,'SEARING':30,'SPINACH':63,'SPRAYED':16,'TERRAIN':48,'TROUBLE':67}


three_straights = [[y+order[x],y+order[x+1],y+order[x+2]] for x in range(len(order)) for y in suits if len(order[x:x+3])==3]
four_straights = [[y+order[x],y+order[x+1],y+order[x+2],y+order[x+3]] for x in range(len(order)) for y in suits if len(order[x:x+4])==4]
three_of_a_kind = [[y[0]+order[x],y[1]+order[x],y[2]+order[x]] for x in range(len(order)) for y in suits_threes]
four_of_a_kind = [[suits[0]+order[x],suits[1]+order[x],suits[2]+order[x],suits[3]+order[x]] for x in range(len(order))]
valid_combos_1 = [[x,y] for x in three_straights for y in four_of_a_kind if not x[0] in y and not x[1] in y and not x[2] in y]
valid_combos_2 = [[x,y] for x in four_straights for y in three_of_a_kind if not x[0] in y and not x[1] in y and not x[2] in y and not x[3] in y]
all_valid_combos = valid_combos_1
for combo in valid_combos_2:
    if not combo in all_valid_combos:
        all_valid_combos.append(combo)


score_dict = {}
for combo in all_valid_combos:
    score = 0
    for card in combo[0]:
        score += cards[card[1:]]
    for card in combo[1]:
        score += cards[card[1:]]
    if score in score_dict.keys():
        score_dict[score].append(combo)
    else:
        score_dict[score] = [combo]

possible_groupings = {}
for word in word_scores:
    possible_groupings[word] = score_dict[word_scores[word]]


#restrict DRUMMER straight to spades
to_remove = []
for grouping in possible_groupings['DRUMMER']:
    if not grouping[0][0][0] == 'S':
        to_remove.append(grouping)
for grouping in to_remove:
    possible_groupings['DRUMMER'].remove(grouping)
#restrict EYEBROW straight to diamonds    
to_remove = []
for grouping in possible_groupings['EYEBROW']:
    if not grouping[0][0][0] == 'D':
        to_remove.append(grouping)
for grouping in to_remove:
    possible_groupings['EYEBROW'].remove(grouping)
#restrict NOVELTY straight to clubs
to_remove = []
for grouping in possible_groupings['NOVELTY']:
    if not grouping[0][0][0] == 'C':
        to_remove.append(grouping)
for grouping in to_remove:
    possible_groupings['NOVELTY'].remove(grouping)
#restrict PRAISED straight to hearts    
to_remove = []
for grouping in possible_groupings['PRAISED']:
    if not grouping[0][0][0] == 'H':
        to_remove.append(grouping)
for grouping in to_remove:
    possible_groupings['PRAISED'].remove(grouping)


words = possible_groupings.keys()

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
all_letters = [x+'1' for x in letters] + [x+'2' for x in letters]

straight_possibilities = {}

all_straight_subs = {}
for word in words:
    all_straight_subs[word] = [word[:3],word[:4],word[3:],word[4:]]
    for substr in all_straight_subs[word]:
        for grouping in possible_groupings[word]:
            if len(grouping[0]) == len(substr):
                if not substr in straight_possibilities.keys():
                    straight_possibilities[substr] = [grouping[0]]
                else:
                    if not grouping[0] in straight_possibilities[substr]:
                        straight_possibilities[substr].append(grouping[0])


substrings = straight_possibilities.keys()

letter_possibilities = {}
less_divided = {}
for letter in letters:
    letter_possibilities[letter] = {}
    less_divided[letter] = {}
    
for word in words:
    for substr in all_straight_subs[word]:
        for x in range(len(substr)):
            letter = substr[x]
            if substr in substrings:
                if not word in letter_possibilities[letter]:
                    less_divided[letter][word] = [y[x] for y in straight_possibilities[substr]]
                    letter_possibilities[letter][word] = {substr:[y[x] for y in straight_possibilities[substr]]}
                else:
                    letter_possibilities[letter][word][substr] = [y[x] for y in straight_possibilities[substr]]
                    for y in straight_possibilities[substr]:
                        less_divided[letter][word].append(y[x])

for word in words:
    for grouping in possible_groupings[word]:
        torf = grouping[1]
        for card in torf:
            for letter in letters:
                if letter in word:
                    if not card in less_divided[letter][word]:
                        less_divided[letter][word].append(card)

#print less_divided

possible_pairs_dict = {}
for letter in less_divided:
    possible_answers = []
    for word in less_divided[letter].keys():
        for card in less_divided[letter][word]:
            possible_answers.append(card)

    pairs = [possible_answers[x:x+2] for x in range(len(possible_answers)) if len(possible_answers[x:x+2])==2]
    possible_pairs = []
    for pair in pairs:
        possible = True
        for word in less_divided[letter].keys():
            if not pair[0] in less_divided[letter][word] and not pair[1] in less_divided[letter][word]:
                possible = False
        if possible:
            if not pair in possible_pairs:
                possible_pairs.append(pair)

    possible_pairs_dict[letter] = possible_pairs


for letter in possible_pairs_dict.keys():
    print str(letter) + ':\t' + str(possible_pairs_dict[letter]) + '\n'

"""
possible_answers = []
for word in less_divided['A'].keys():
    for card in less_divided['A'][word]:
        possible_answers.append(card)

pairs = [possible_answers[x:x+2] for x in range(len(possible_answers)) if len(possible_answers[x:x+2])==2]
print pairs
"""

