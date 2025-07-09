# ciwmaint
DES maintenance model w CIW library (python)

in questo primo esempio costruiamo un network con
- 4 macchine in serie con un MTTF di (i+1)*100 minuti e un MTTR di 10/(i+1)
- 2 categorie di prodotti di priorità 2 - FIFO
    ° "prodotto A" ha un tempo di servizio esponenziale di (2i/3 + 2) minuti, tempo di interarrivo ogni 50 minuti. il ciclo macchina è [2, 3, 0, 1]
    ° "prodotto B" ha un tempo di servizio esponenziale di (3i/2 + 1) minuti, tempo di interarrivo ogni 55 minuti. il ciclo macchina è [0, 1, 2, 3]
- 1 categorie di di entità "manutenzione"
    ° "breakdown" ha priorità 1 e valore MTTR, avviene ogni MTTF come definito sopra

I valori plottati sono:
...

# prodotto A tot 12
# 0 - 2
# 1 - 2.66
# 2 - 3.33
# 3 - 4

# prodotto B tot 11
# 0 - 1
# 1 - 2.5
# 2 - 3
# 3 - 4.5

nello scrivere l'esempio mi sono resa conto che se strutturo in questo modo gli eventi di manutenzione non ho controllo sulle risorse disponibili per fare la manutenzione. domani penso a come posso strutturare un esempio che possa valutare l'utilizzo di risorse