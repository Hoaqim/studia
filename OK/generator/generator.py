import random
from pathlib import Path

print("podaj ilość punktów")
ilosc = int(input())
print("podaj przedział z którgo chcesz otzrymac wsp. punktów")
x = int(input())
y = int(input())
filepath = r"testy_1.txt"
f = open(filepath, "w+")

f.write(str(ilosc))
f.write("\n")
for i in range(0,ilosc):
    x1 = random.randint(x, y)
    y1 = random.randint(x, y)
    f.write(str(x1))
    f.write(" ")
    f.write(str(y1))
    f.write("\n")
print(Path.cwd())
