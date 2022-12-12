#tworzenie wstępnej populacji
import operator
from math import sqrt
import random
import numpy as np
import os
import time
#print(os.getcwd())
# odczyt z pliku
filepath = r"Berlin.txt"
f = open(filepath, "r")

ilosc = int(f.readline())
punkty = []
for i in range(0, ilosc):
    linia = f.readline()
    punkty.append(linia.strip().split())
#print(punkty)
for i in range(0, ilosc):
    punkty[i].pop(0)
    punkty[i][0] = float(punkty[i][0])
    punkty[i][1] = float(punkty[i][1])
#print(punkty)
miasta = []
for i in range(ilosc):
    miasta.append(i)
#print(miasta)

def wybieranie_losowe(ilosc,wielkosc):
    populacja = []
    lista = []
    for i in range(ilosc):
        lista.append(i)
    print(lista)
    for i in range(0,wielkosc):
        droga = random.shuffle(lista)
        populacja.append(droga)
    return populacja
print(wybieranie_losowe(ilosc,5))

def algorytm_zachłanny(pierwszy,ilosc):
    odwiedzone = []
    odwiedzone.append(pierwszy)
    il = ilosc
    odleglosci = []
    while len(odwiedzone) != ilosc:
        x = 0
        l = 0
        akt = odwiedzone[-1]
        for i in range(0,il):
            if i not in odwiedzone:
                b = sqrt(((punkty[akt][0]-punkty[i][0])**2)+((punkty[akt][1]-punkty[i][1])**2))
                if x == 0:
                    x = b
                    l = i
                elif b < x:
                    x = b
                    l = i
        odwiedzone.append(l)
        odleglosci.append(x)
    return odwiedzone
#stworzenie pierwotnej populacji
#z pomocą algorytmu zachłannego
def pierwsza_populacja(wielkosc,ilosc):
    populacja = []
    for i in range(0,wielkosc):
        pierwszy = random.randint(0,ilosc-1)
        populacja.append(algorytm_zachłanny(pierwszy,ilosc))
    return populacja
populacja = pierwsza_populacja(4,ilosc)
#print(populacja)
#funkcja do oceny hromosomów
#
def fitness(hromosom,punkty):
    total = 0
    for i in range(1,len(hromosom)):
        k = hromosom[i-1]
        l = hromosom[i]
        total = total + sqrt(((punkty[k][0]-punkty[l][0])**2)+((punkty[k][1]-punkty[l][1])**2))
    total = total + sqrt(((punkty[hromosom[-1]][0]-punkty[hromosom[0]][0])**2)+((punkty[hromosom[-1]][1]-punkty[hromosom[0]][1])**2))
    return total
def ranking_odleglosci(populacja,punkty):
    wyniki_fitnesu = {}
    for i in range(0,len(populacja)):
        wyniki_fitnesu[i] = fitness(populacja[i],punkty)
    return sorted(wyniki_fitnesu.items(), key = operator.itemgetter(1), reverse= False)

rank_odl = ranking_odleglosci(populacja,punkty)
#print(rank_odl)
#print(len(rank_odl))
#print(rank_odl[0][1])
#print(rank_odl[[1][0]])
#print(rank_odl[2][0])
#turniej wybiernaie osobników do rozrodu
def wybranie(rank_odl, ilu_wybieramy):
    wybrane_wyniki = []
    wyniki = []
    for i in rank_odl:
        wyniki.append(i[0])
    for i in range(0,ilu_wybieramy):
        wybrane_wyniki.append(wyniki[i])
    return wybrane_wyniki
wyb = wybranie(rank_odl,4)
#print(wyb)

def gody(populacja,wybrane):
    gody = []
    for i in range(0,len(wybrane)):
        index = wybrane[i]
        gody.append(populacja[index])
    return gody
populacja_do_rozrodu = gody(populacja,wyb)
#print(populacja_do_rozrodu)

#tworzenie dzieciaczków
def crossover(a,b,ilosc):
    child = []
    childA = []
    childB = []
    z = random.randint(1,ilosc-1)
    for i in range(0,z):
        childA.append(a[i])
    childB = [item for item in b if item not in childA]
    child = childA + childB
    return child

def rozrody(populacja_do_rozrodu,ilosc):
    dzieciaki = []
    for i in range(0,len(populacja_do_rozrodu)):
        x = crossover(populacja_do_rozrodu[i-1],populacja_do_rozrodu[i],ilosc)
        dzieciaki.append(x)
    return dzieciaki
#r = rozrody(populacja_do_rozrodu)
#print(r)

def mutacja(droga,szansa_na_mutacje):
    route = droga
    for zamiana in range(1,len(route)-1):
        if (random.random() < szansa_na_mutacje):
            zamienione_z = random.randint(0,len(route)-1)
            wsp1 = route[zamiana]
            wsp2 = route[zamienione_z]
            route[zamienione_z] = wsp1
            route[zamiana] = wsp2
    return route
def mutacja_na_populacji(dzieci,szansa_na_mutacje):
    next_gen = []
    for i in dzieci:
        zmutowane_dziecko = mutacja(i,szansa_na_mutacje)
        next_gen.append(zmutowane_dziecko)
    return next_gen
#print(mutacja_na_populacji(r,0.5))
def nowa_generacja(punkty,obecna_populacja,szansa_na_zmutowanie,ilu_wybieramy,ilosc):
    ranking = ranking_odleglosci(obecna_populacja,punkty)

    wybrancy = wybranie(ranking,ilu_wybieramy)

    go_dy = gody(obecna_populacja,wybrancy)

    dzieci = rozrody(go_dy,ilosc)

    nowicjusze = mutacja_na_populacji(dzieci,szansa_na_zmutowanie)

    return nowicjusze
def algo_genteyczne(punkty,ilosc,ilosc_generacji,szansa_na_mutacje,ilu_wybieramy,rozmiar_populacji):
    popul = []
    postepy = []


    populacja = pierwsza_populacja(rozmiar_populacji, ilosc)
    r = ranking_odleglosci(populacja,punkty)[0]
    postepy.append(r[1])
    print(f"początkowy dystans {postepy[0]}")
    print(f"począktowa droga {populacja[r[0]]}")
    timeout = time.time() + 60 * 9
    for i in range(0,ilosc_generacji):
        popul = nowa_generacja(punkty, populacja, szansa_na_mutacje, ilu_wybieramy,ilosc)
        rank_ = ranking_odleglosci(popul, punkty)

        populacja = popul + populacja[len(popul):]
        print(len(populacja))
        if rank_[0][1] < postepy[-1]:
            postepy.append(ranking_odleglosci(popul, punkty)[0][1])
            rozwiazanie = popul[rank_[0][0]]

        if time.time() > timeout:
            break
    print(f"njalepszy wynik {postepy[-1]}")
    print(f"najlepsza droga {rozwiazanie}")
    print(min(postepy))
    return rank_, popul



if __name__ == "__main__":
    #punkty to współrzędne ilosc to ilosc punktów
    algo_genteyczne(punkty,ilosc,9000,0.01,1400,1700)