import operator
from math import sqrt
import random
import numpy as np
import os
import time
import datetime
def pierwsza_losowa_populacja(wielkosc,ilosc):
    populacja = []
    for i in range(0,wielkosc):
        p = np.random.permutation(ilosc)
        populacja.append(p)
    return populacja

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

#funkcja do oceny hromosomów
def fitness(hromosom,punkty):
    total = 0
    for i in range(1,len(hromosom)):
        k = hromosom[i-1]
        l = hromosom[i]
        total = total + sqrt(((punkty[k][0]-punkty[l][0])**2)+((punkty[k][1]-punkty[l][1])**2))
    total = total + sqrt(((punkty[hromosom[-1]][0]-punkty[hromosom[0]][0])**2)+((punkty[hromosom[-1]][1]-punkty[hromosom[0]][1])**2))
    return total

def macierz(ilosc,punkty):
    macierz = []
    for i in range(ilosc):
        macierz.append([])

    for i in range(ilosc):
        for j in range(ilosc):
            x = sqrt(((punkty[i][0]-punkty[j][0])**2)+((punkty[i][1]-punkty[j][1])**2))
            macierz[i].append(x)
    return macierz

def nowy_fitnes(macierz,hromosom):
    total = 0
    for i in range(1,len(hromosom)):
        x = hromosom[i-1]
        y = hromosom[i]
        total = total + macierz[x][y]
    total = total + macierz[hromosom[0]][hromosom[-1]]
    return total
def ranking_odleglosci(populacja,macierz):
    wyniki_fitnesu = {}
    for i in range(0,len(populacja)):
        wyniki_fitnesu[i] = nowy_fitnes(macierz,populacja[i])
    return sorted(wyniki_fitnesu.items(), key = operator.itemgetter(1), reverse= False)

#turniej wybiernaie osobników do rozrodu
def wybranie(rank_odl, ilu_wybieramy):
    wybrane_wyniki = []
    wyniki = []
    for i in rank_odl:
        wyniki.append(i[0])
    for i in range(0,ilu_wybieramy):
        wybrane_wyniki.append(wyniki[i])
    return wybrane_wyniki

def gody(populacja,wybrane):
    gody = []
    for i in range(0,len(wybrane)):
        index = wybrane[i]
        gody.append(populacja[index])
    return gody

#tworzenie dzieciaczków
def crossover(a,b,ilosc):

    childA = []
    childB = []
    z = random.randint(0,ilosc-1)
    g = random.randint(0,ilosc-1)
    gene_a = min(z,g)
    gene_b = max(z,g)
    for i in range(gene_a,gene_b):
        childA.append(a[i])
        childB.append(b[i])
    childB_1 = [item for item in a if item not in childB]
    childA_1 = [item for item in b if item not in childA]
    child1 = childA + childA_1
    child2 = childB + childB_1
    return child1,child2

def cross_over(p_1, p_2,ilosc):
    one_point = random.randint(1, ilosc-1)

    child_1 = p_1[1:one_point]
    child_2 = p_2[1:one_point]

    child_1_remain = [item for item in p_2[1:-1] if item not in child_1]
    child_2_remain = [item for item in p_1[1:-1] if item not in child_2]

    child_1 += child_1_remain
    child_2 += child_2_remain

    child_1.insert(0, p_1[0])
    child_1.append(p_1[0])

    child_2.insert(0, p_2[0])
    child_2.append(p_2[0])

    return child_1, child_2

def large_scale_cross(a,ilosc):

    z = random.randint(0,ilosc-1)
    g = random.randint(0,ilosc-1)
    dolna_granica = min(z,g)
    gorna_granica = max(z,g)
    podzial = random.randint(dolna_granica,gorna_granica)
    child = []
    for i in range(0,dolna_granica):
        child.append(a[i])
    for i in range(dolna_granica,podzial):
        child.append(a[i])
    for i in range(podzial,gorna_granica):
        child.append(a[i])
    for i in range(gorna_granica,ilosc):
        child.append(a[i])

    return child
def rozrody(populacja_do_rozrodu,ilosc):
    dzieciaki = []
    for i in range(0,len(populacja_do_rozrodu)):
        x,y = crossover(populacja_do_rozrodu[i-1],populacja_do_rozrodu[i],ilosc)
        dzieciaki.append(x)
        dzieciaki.append(y)

    dzieciaki = dzieciaki + populacja_do_rozrodu
    return dzieciaki
#r = rozrody(populacja_do_rozrodu)
#print(r)
def mutacja_2(droga,szansa_na_mutacje):
    route = droga
    for zamiana in range(1,len(route)-1):
        if (random.random() < szansa_na_mutacje):
            zamienione_z = random.randint(0,len(route)-1)
            wsp1 = route[zamiana]
            wsp2 = route[zamienione_z]
            route[zamienione_z] = wsp1
            route[zamiana] = wsp2
    return route
def mutacja_na_populacji_2(dzieci,szansa_na_mutacje):
    next_gen = []
    for i in dzieci:
        zmutowane_dziecko = mutacja_2(i,szansa_na_mutacje)
        next_gen.append(zmutowane_dziecko)
    return next_gen
def mutacja(droga,szansa_na_mutacje):
    route = droga

    zamiana = random.randint(0, len(route)-1)
    zamienione_z = random.randint(0, len(route)-1)
    wsp1 = route[zamiana]
    wsp2 = route[zamienione_z]
    route[zamienione_z] = wsp1
    route[zamiana] = wsp2
    return route
def mutacja_na_populacji(dzieci, szansa_na_mutacje):
    next_gen = []
    for i in dzieci:
        if (random.random() < szansa_na_mutacje):
            zmutowane_dziecko = mutacja(i, szansa_na_mutacje)
            next_gen.append(zmutowane_dziecko)
        else:
            next_gen.append(i)
    return next_gen
#print(mutacja_na_populacji(r,0.5))
def nowa_generacja(macierz, obecna_populacja, szansa_na_zmutowanie, ilu_wybieramy, ilosc):
    ranking = ranking_odleglosci(obecna_populacja,macierz)

    wybrancy = wybranie(ranking,ilu_wybieramy)

    go_dy = gody(obecna_populacja,wybrancy)

    dzieci = rozrody(go_dy,ilosc)

    nowicjusze = mutacja_na_populacji(dzieci,szansa_na_zmutowanie)

    return nowicjusze
def algo_genteyczne(warunek_stop,czesc,punkty,ilosc,ilosc_generacji,szansa_na_mutacje,ilu_wybieramy,rozmiar_populacji):
    popul = []
    postepy = []
    matrix = macierz(ilosc,punkty)

    z = int(rozmiar_populacji*czesc)
    d = rozmiar_populacji - z
    populacja = pierwsza_populacja(z,ilosc) + pierwsza_losowa_populacja(d, ilosc)
    x = populacja
    r = ranking_odleglosci(populacja,matrix)[0]
    postepy.append(r[1])
    print(f"początkowy dystans {postepy[0]}")
    print(f"począktowa droga {populacja[r[0]]}")
    timeout = time.time() + 60 * 5
    for i in range(0,ilosc_generacji):
        popul = nowa_generacja(matrix, populacja, szansa_na_mutacje, ilu_wybieramy,ilosc)
        rank_ = ranking_odleglosci(popul, matrix)

        populacja = popul + x[len(popul):]
        print(len(populacja))
        if rank_[0][1] < postepy[-1]:
            postepy.append(ranking_odleglosci(popul, matrix)[0][1])
            rozwiazanie = popul[rank_[0][0]]

        print(postepy[-1])
        print(i)
        if time.time() > timeout:
            break
        if postepy[-1] < warunek_stop:
            break
    print(f"njalepszy wynik {postepy[-1]}")
    print(f"najlepsza droga {rozwiazanie}")
    print("heh",min(postepy))
    return rank_, popul



if __name__ == "__main__":
    filepath = r"tsp1000.txt"
    f = open(filepath, "r")
    ilosc = int(f.readline())
    punkty = []
    for i in range(0, ilosc):
        linia = f.readline()
        punkty.append(linia.strip().split())
    for i in range(0, ilosc):
        punkty[i].pop(0)
        punkty[i][0] = float(punkty[i][0])
        punkty[i][1] = float(punkty[i][1])
    miasta = []
    for i in range(ilosc):
        miasta.append(i)
    #funkcja fitens na podstawie macierzy wypełnionej odległosciami
    #punkty to współrzędne ilosc to ilosc punktów
    start = datetime.datetime.now()
    #berlin52 znajduje optimum szybko w 90% przypadków
    #wykozystuje mutacja dla populacji
    #algo_genteyczne(7_545,1.0,punkty,ilosc,3000,0.3,300,1000)

    #bier127 zazwyczaj daje wyniki w okolicy najlepszego aktualnie wyniku w rankingu
    # wykozystuje mutacja dla populacji
    #algo_genteyczne( 120_000, 1.0, punkty, ilosc, 1500, 0.1, 1550, 1550)

    #tsp250 daje wyniki ok takie jak najlepszy jaki jest w obecnym rankingu
    # wykozystuje mutacja dla populacji
    #algo_genteyczne(13_000,0.1,punkty,ilosc,1500,0.18,600,1800)

    #tsp500 daje wyniki gorsze niz obecnie najlepszy w rankingu
    # wykozystuje mutacja dla populacji
    #algo_genteyczne(91_000, 0.01, punkty, ilosc, 1000, 0.1, 100, 800)

    #tsp1000 daje zazwyczaj wynik lepszy troche niz ten z rankingu
    #wykozystuje mutacja dla populacji 2
    algo_genteyczne(27_000, 0.01, punkty, ilosc, 500, 0.15, 100, 600)

    #wszystkie daja wynik lepszy niz alg zachłanny z rankingu
    end = datetime.datetime.now() - start
    print(end)