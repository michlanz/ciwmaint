import ciw
import pandas as pd
import numpy as np

#in questo primo esempio costruiamo un network con
#- 4 macchine in serie con un MTTF di (i+1)*100 minuti e un MTTR di 10/(i+1)
#- 2 categorie di prodotti di priorità 2 - FIFO
#    ° "prodotto A" ha un ciclo macchina [2, 3, 0, 1]
#    ° "prodotto B" ha un ciclo macchina [0, 1, 2, 3]
#- 1 categorie di di entità "manutenzione"
#    ° "breakdown" ha priorità 1 e valore MTTR, avviene ogni MTTF come definito sopra
#
#I valori plottati sono:
#...
#
## prodotto A tot 12
## 0 - 2
## 1 - 2.66
## 2 - 3.33
## 3 - 4
#
## prodotto B tot 11
## 0 - 1
## 1 - 2.5
## 2 - 3
## 3 - 4.5

#itera sulla lunghezza delle macchine e metti none tutte le volte che l'indice non è quello del primo elemento.
#non serve un "else" perché tanto genera tutto comunque
dict_arrivals = {
        'Product_A': [
            None,
            None,
            ciw.dists.Exponential(rate=60/50),
            None
        ], 'Product_B': [
            ciw.dists.Exponential(rate=60/55),
            None,
            None,
            None
        ]
}


dict_services = {
    'Product_A': [ciw.dists.Exponential(rate=60/(2*i/3 + 2)) for i in range(4)],
    'Product_B': [ciw.dists.Exponential(rate=60/(3*i/2 + 1)) for i in range(4)]
}

#per il route: lista di liste per la matrice - ciclo for di list comprehension