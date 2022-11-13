
from math import sqrt
import random


if __name__ == "__main__":
    # odczyt z pliku

    filepath = r"zadanie_1.txt"
    f = open(filepath,"r")
    ilosc = int(f.readline())
    punkty = []
    for i in range(0,ilosc):
        linia = f.readline()
        punkty.append(linia.strip().split())
    print(punkty)
    for i in range(0,ilosc):
        punkty[i][0] = float(punkty[i][0])
        punkty[i][1] = float(punkty[i][1])
    print(punkty)
    odwiedzone = []
    rozwiazanie = []
    print(len(punkty),ilosc)
    pierwszy = 0
    odwiedzone.append(pierwszy)
    il = ilosc
    o = 0
    odleglosci = []
    while len(odwiedzone) != ilosc:
        """aktualny wieżchołek"""
        x = 0
        l = 0
        akt = odwiedzone[-1]
        for i in range(il):
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

    print(odwiedzone)
    print(odleglosci)
    """"
    sprawdzanie odleglosci od danego punktu wszystkich innych punktów
    odleglosci_od_3 = []
    for i in range(ilosc):
        k = sqrt(((punkty[3][0]-punkty[i][0])**2)+((punkty[3][1]-punkty[i][1])**2))
        odleglosci_od_3.append(k)
    print(odleglosci_od_3)
    """
