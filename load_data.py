# -*- coding: utf-8 -*-
"""
Created on Sat May 14 10:51:58 2016

@author: aeidelman
"""

import os
import pandas as pd

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import Levenshtein

# path = '/home/sgmap/data/transparence'
# path_dest = '/home/sgmap/git/VizTransparence/data'
path = 'D:\\data\\transparence'
path_dest = 'C:\\git\\VizTransparence\\data'

# avantage
path_file = os.path.join(path, '2016_05_23', 'declaration_avantage_2016_05_23_04_00.csv')

categorical_vars = ['denomination_sociale', 'categorie', 'qualite',
                    'benef_speicalite_libelle', 'benef_qualification',
                    'avant_date_signature', 'avant_nature',
                    'benef_codepostal'
                    ]

av = pd.read_csv(path_file, sep=';', # nrows = 1500000,
                 usecols = categorical_vars + ['avant_montant_ttc'])
#av['year'] = av['avant_date_signature'].str[6:]

categorical_vars.remove('benef_codepostal')
for col in categorical_vars:
    av[col] = av[col].str.lower()


av['departement'] = av['benef_codepostal'].astype(str).str[:2]
categorical_vars += ['departement']

av_group = av.groupby(categorical_vars)
print(av_group.size().value_counts())
agg_av = av_group['avant_montant_ttc'].sum().reset_index()


var = 'benef_qualification'
uniformisee = agg_av[var]
liste = uniformisee.unique().tolist()

# idée : créer un réseau avec la force des liens.
# même si ce n'est pas réaliste à grande échelle
#
#for i in range(len(liste)):
#    for k in range(i + 1, len(liste)):
#        if fuzz.ratio(liste[i], liste[k]) > 90:
#            print(liste[i], fuzz.ratio(liste[i], liste[k]), liste[k],
#                 sum(av[var] == liste[i]), sum(av[var] == liste[k]))


# On a des groupes important avec médecine et chirurgie pour mettre
# moins d'importance à ces mots, on réduit leur taille
uniformisee = uniformisee.str.replace('chirurgie', 'chir')
uniformisee = uniformisee.str.replace('médecine', 'md')
liste = uniformisee.unique().tolist()

# agg_av.to_json(os.path.join(path, 'transp.json'), orient='records')
agg_av.to_csv(os.path.join(path_dest, 'transp2.csv'), index=False)


### table par date
# TODO:
