#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
import re


replace_dict_ingrs = {'': ['&', "'n",'%', ',', '.', '#', '[', ']','*', '/',
                                               '!', '?',  "©","®","™" , "chopped", "fresh", "minced",
                                               'peeled', 'grated', 'taste', 'frozen'], "_":["-"]}


re_list = ['or','s','fillet(s)*','cube([sd])*', 'ma', 'square(s)*', 'to', 'and',
           'can(ned)*','each(es)*','piece(s)*', 'bag(s)*',
           'slice([sd])*','package(s)*', 'packet(s)*', 'inch(es)*', 'thin(ly)*',
           'container',
           'rinsed','mashed','torn','into','fine(ly)*','(un)*salted','more',
           'as', 'desired','crushed', 'fresh(ly)','raw', 'smoked', 'mixed',
           'refrigerated','rough(ly)*','flat','reduced', 'jar',
           'prepared','small','tray(s)*',
           'seeded','quarter(ed)*','(d)*iced','poach(es)*','strip(s)*','luke',
           'warm','bite','size(d)*','drained','shredded','co(lo)r*ed','cubed','at',
           'discard(ed)*','whole','meat','trim(med)*','wedge(s)*','split','broken', 'cut(s)*',
           'needed','room','temperature','(pre(-)*)*(un)*cooked','medium', 'small','large','flavored','based',
           'cocktail','crumble(d)*', 'undyed','dressed','granules','thick','several','in','half','halved','with',
           'well','marbled','crisp(l)*y', 'lean(est)*', 'grain','other','adjustable','light(ly)*', 'baked','lengthwise','crosswise'
           ]

re_patterns = {' ':[]}
for r in re_list:
    space_pattern = ""
    space_pattern += '\s*\\b'
    space_pattern += r
    space_pattern += '\\b\s*'
    re_patterns[' '].append(space_pattern)

# re_patterns = {' ': {r'\s*\bor\b\s*', r'\s*\bs\b\s*', r'\s*\bfillet(s)*\b\s*', r'\s*\bcube(s)*\b\s*',
#                      r'\s*\bma\b\s*', r'\s*\bsquare(s)*\b\s*', r'\s*\bto\b\s*', r'\s*\band\b\s*',
#                      r'\s*\bcan\b\s*', r'\s*\beaches\b\s*' , r'\s*\bpiece(s)*\b\s*',
#                      r'\s*\bbag(s)*\b\s*', r'\s*\bslice([sd])*\b\s*', r'\s*\bpackage(s)*\b\s*',
#                      r'\bpacket(s)*\b', r'\binch(es)*\b', r'\bthin(ly)*\b',
#                      r'\bcontainer\b', r'\brinsed\b', r'\bmashed\b',
#                      r'\btorn\s+(into)\b', r'bfine(ly)*\b', r'\bunsalted\b',
#                      r'\bmore\b', r'\bas\b', r'\bdesired\b', r'\bcrushed\b',
#                      r'\bfresh(ly)*\b', r'\braw\b', r'\bsmoked\b', r'\bmixed\b',
#                      r'\brefrigerated\b',r'\brough(ly)\b', r'\bflat\b',
#                      r'\breduced\b', r'\bjar\b', r'\bprepared\b', r'\bsmall\b',
#                      r'\btray(s)*\b', r'\bcanned\b', r'\bseeded\b',
#                      r'\bquartered\b' , r'\bdiced\b', r'\bpoaches\b',
#                      r'\bstrip(s)*\b', r'\b(luke\s)*warm\b', r'\bice(d)*\b',
#                      r'\bbite\s+size(d)*\b', r'\bdrained\b', r'\bshredded\b',
#                      r'\bcolored\b', r'\bcube(d)*\b', r'\bat\b', r'\bdiscard\b',
#                      r'\bcored\b', r'\bseeded\b', r'\bwhole\b', r'\bmeat\b',
#                      r'\btrimmed\b',r'\bwedge(s)*\b', r'\bsplit\b',
#                      r'\bbroken\b', r'(\s*\bcut\b)*\s*\binto\b\s*',
#                      r'\s+cut\s+into\b', r'\s+as\s+needed\b',
#                      r'(\bat\b)*room\s+temperature\b', r'\bcan(s)+\base',
#                      r'\b(pre\s*)*(un\s*)*cooked\b', r'\bmedium\b(sized)*' },
re_patterns.update({'': {r'\(.*\)', r'^\s*', r"'(s)*\s", r'$\s*'},
               r'\1':{
                   r'\b(\w+)\b\w+\b(\1\b)+'}})

#breakpoint()
base_words = ['peppers', 'tomato', 'spinach_leaves', 'turkey_breast',
              'lettuce_leaf', 'chicken_thighs', 'milk_powder',
              'bread_crumbs', 'onion_flakes', 'red_pepper', 'pepper_flakes',
              'juice_concentrate', 'cracker_crumbs', 'hot_chili',
              'seasoning_mix', 'dill_weed', 'pepper_sauce', 'sprouts',
              'cooking_spray', 'cheese_blend', 'basil_leaves',
              'pineapple_chunks', 'marshmallow', 'chile_powder',
              'cheese_blend', 'corn_kernels', 'tomato_sauce', 'chickens',
              'cracker_crust', 'lemonade_concentrate', 'red_chili',
              'mushroom_caps', 'mushroom_cap', 'breaded_chicken',
              'frozen_pineapple', 'pineapple_chunks', 'seasoning_mix',
              'seaweed', 'onion_flakes', 'bouillon_granules',
              'lettuce_leaf', 'stuffing_mix', 'parsley_flakes',
              'chicken_breast', 'basil_leaves', 'baguettes', 'green_tea',
              'peanut_butter', 'green_onion', 'fresh_cilantro',
              'breaded_chicken', 'hot_pepper', 'dried_lavender',
              'white_chocolate', 'dill_weed', 'cake_mix', 'cheese_spread',
              'turkey_breast', 'chicken_thighs', 'basil_leaves',
              'mandarin_orange', 'laurel', 'cabbage_head', 'pistachio',
              'cheese_dip', 'thyme_leave', 'boneless_pork', 'red_pepper',
              'onion_dip', 'skinless_chicken', 'dark_chocolate',
              'canned_corn', 'muffin', 'cracker_crust', 'bread_crumbs',
              'frozen_broccoli', 'philadelphia', 'cracker_crust',
              'chicken_breast','dressing_mix', 'salad_dressing']


def get_ingredient(det_ingr, replace_dict):
    det_ingr_undrs = det_ingr.lower().encode('utf-8')
    for k,vs in re_patterns.items():
        for v in vs:
            det_ingr_undrs = re.sub(v, k, det_ingr_undrs)

    det_ingr_undrs = ''.join(i for i in det_ingr_undrs if not i.isdigit())

    for rep, char_list in replace_dict.items():
        for c_ in char_list:
            if c_ in det_ingr_undrs:
                det_ingr_undrs = det_ingr_undrs.replace(c_, rep)
    det_ingr_undrs = det_ingr_undrs.strip()
    det_ingr_undrs = det_ingr_undrs.replace(' ', '_')
    det_ingr_undrs = re.sub(r'_+', r'_', det_ingr_undrs)
    return det_ingr_undrs

def get_ing_cleaner():
    ing_cleaner = partial(get_ingredient, replace_dict=replace_dict_ingrs)
    return ing_cleaner









