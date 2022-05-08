'''Pravidlá su jemne zjednodušené:
- hráč priamo hádže kockou a ide, 
- do domčeka nie je potrebné hodiť presné číslo, 
- hráč sa automaticky dostáva na posledný voľný domček,
- po hodení 6tky ide aj tak ďalší hráč, 
- nevybíjajú sa. 
Žiaľ, moji panáčikovia sa navzájom nestretávajú. Hra teda prebieha tak, že na striedačku prejde celú trasu 
panáčik jedného hráča a až keď dôjde do domčeka, štartuje hráč 2. Takto dookola, až kým nie sú všetci doma.
.. asi tušia, že tu máme koronu, tak si držia odstupy.'''

from random import randint

def kocka(n): #vopred vygeneruje vsetky hody podla velkosti sachovnice
    steps = []
    pocet_policok = 8 * (n // 2)
    pocet_panacikov = int(n - 3)
    okruh = pocet_policok + pocet_panacikov/2

    for i in range(pocet_panacikov):
        count = 1
        steps.append([1]) #vytvori tolko listov, kolko je panacikov - vsetky zacinaju 1tkou, pretoze kazdy panacik najprv stoji na "starte"

        while count <= pocet_policok:
            num = randint(1,6)
            count = count + num
            steps[i].append(num)
    return steps

def gensachovnicu(n):
    if n % 2 == 0 or n < 5: #ak by bol zly input
        print('n musi byt neparne a n >= 5')

    #cislovanie
    pole = []
    for row in range(n + 1):
        pole.append([]) #vlozi tolko listov, kolko je radov
        for col in range(n + 1):
            pole[-1].append('')
            pole[0][0] = ' '

            pole[0][col] = col - 1 #ak ide o prvy rad, zmeni sa na 01234
            if col >= 10: 
               pole[0][col] = (col - 1) % 10 #cisla vacsie ako 10 sa budu zapisovat len poslednou cifrou

            for k in range(len(pole)):
                pole[row][0] = k - 1
                if k >= 10:
                    pole[row][0] = (k - 1) % 10 
            
            if row != 0 and col != 0:
                pole[row][col] = ' ' #body mimo sachovnice ostavaju prazdne

    #sachovnica
    mid = (n // 2) + 1
    
    for row in range(n + 1):
        for col in range(n + 1):
            pole[row][mid] = 'D'    
            pole[mid][mid-1] = 'D'
            pole[mid][mid+1] = 'D'
            pole[mid][col] = 'D'
            pole[mid-1][mid] = 'D'
            pole[mid+1][mid] = 'D'

            pole[1][mid] = '*' 
            pole[-1][mid] = '*'
            pole[row][mid-1] = '*'
            pole[row][mid+1] = '*'
            pole[mid][1] = '*'
            pole[mid][-1] = '*'
            pole[mid-1][col] = '*'
            pole[mid+1][col] = '*'

            pole[0][mid] = (mid - 1) % 10 #D a * sa zapisuju do celych riadkov/stlpcov, preto treba naspat nastavit cisla
            pole[0][mid-1] = (mid - 2) % 10 #hned je osetrene aj to, ak by boli vacsie ako 10
            pole[0][mid+1] = mid % 10
            pole[mid][0] = (mid - 1) % 10
            pole[mid-1][0] = (mid - 2) % 10
            pole[mid+1][0] = mid % 10
    pole[mid][mid] = 'X'
    return pole 

def tlacsachovnicu(sachovnica): 
    for row in range (len(sachovnica)):
        for col in sachovnica[row]:
            print(col, end = '  ') #vypise sachovnicu bez zatvoriek, ciarok
        print() 

n = int(input('zadaj rozmer n: '))
sachovnica = gensachovnicu(n)
hody_kockou = kocka(n)

#zadefinovanie podstatnych bodov a cisel na sachovnici
mid = (n // 2) + 1
pocet_D = n - 3
pol_D = pocet_D / 2
pocet_panacikov = int(pol_D * 2)
half_n = n // 2

roh1 = half_n #vnutorne rohy sachovnice
roh2 = half_n * 3 
roh3 = half_n * 5
roh4 = half_n * 7

vrch1 = half_n * 2 #vrcholy sachovnice
vrch2 = half_n * 4
vrch3 = half_n * 6
vrch4 = half_n * 8

pocet_A_panacikov = 0
pocet_B_panacikov = 0
pocet_A_krokov = 0
pocet_B_krokov = 0

for hrac in range(pocet_panacikov): #striedavo vybera bud hraca A alebo B
    if hrac % 2 == 0: #zadefinovane veci k hracom + pocitanie panacikov pre neskorsie ukladanie do domceka
        count = 0 #hraci idu striedavo - preto rozdelenie podla delitelnosti
        row = 1
        col = mid + 1
        pocet_A_panacikov = pocet_A_panacikov + 1
    elif hrac  % 2 == 1:
        count = 4 * half_n #aby pre hraca B platili rovnake pravidla pre pohyb, count nemoze zacat od 0 ale od polovice sachovnice
        row = -1
        col = mid - 1   
        pocet_B_panacikov = pocet_B_panacikov + 1

    for i in range(len(hody_kockou[hrac])): #prejde sa cely list s cislami hodenymi kockou u daneho panacika
        print('hráč hodil: ' + str(hody_kockou[hrac][i]))

        count = count + hody_kockou[hrac][i] #pocita kroky pre orientovanie po sachovnici

        if hrac % 2 == 0: 
            a_or_b = 'A' #premenna pre ulahcenie neskorsieho vypisovania A/B do sachovnice
            pocet_A_krokov = pocet_A_krokov + 1 #pocitadlo krokov hraca, aby sa dalo urcit, kto vyhral
        elif hrac % 2 == 1:
            a_or_b = 'B'
            pocet_B_krokov = pocet_B_krokov + 1           

        if hrac % 2 == 1 and count > vrch4: #B ma na zaciatku priratanu polovicu sachovnice, za vrcholom sa musi cela odratat, aby zacalo od 0 a nadalej fungovalo ako A
            count = count - vrch4

        if count <= roh1: #podmienky pohybu v danych castiach sachovnice
            sachovnica[row][col] = '*'
            count2 = roh1 - count
            row = mid - count2 -1
            col = mid + 1
            sachovnica[row][col] = a_or_b

        elif count <= vrch1-1:
            sachovnica[row][col] = '*'
            count2 = count - roh1
            col = mid+1 + count2
            row = mid-1
            sachovnica[row][col] = a_or_b

        elif count <= vrch1+1:
            sachovnica[row][col] = '*'
            count2 = count - vrch1+1
            row = mid-1 + count2
            col = -1
            sachovnica[row][col] = a_or_b

        elif count <= roh2:
            sachovnica[row][col] = '*'
            count2 = count - vrch1 
            row = mid+1
            col = -count2
            sachovnica[row][col] = a_or_b

        elif count <= vrch2-1:
            sachovnica[row][col] = '*'
            count2 = vrch2 - count 
            row = -count2
            col = mid+1
            sachovnica[row][col] = a_or_b

        #podmienka pre hraca B, aby skocil na posledne volne miesto v domceku, ak pocet krokov prekroci obvod sachovnice 
        elif hrac % 2 == 1 and count > vrch2 and i > len(hody_kockou[hrac]) - 2: #musi obsahovat podmienku pre i, aby si to nemylilo s prvymi krokmi B
            sachovnica[row][col] = '*'                                           #B nezacina od 0, ale od "0 + vrch2" - preto by to mohlo kazit priebeh hry
            if col == mid and row < -1:
                sachovnica[row][col] = 'D' 
            col = mid
            row = mid + pocet_B_panacikov
            sachovnica[row][col] = 'B'

        elif count <= vrch2+1:
            sachovnica[row][col] = '*'
            count2 = count - vrch2
            row = -1
            col = mid - count2
            sachovnica[row][col] = a_or_b

        elif count <= roh3:
            sachovnica[row][col] = '*'
            count2 = count - vrch2
            row = -count2
            col = mid-1
            sachovnica[row][col] = a_or_b

        elif count <= vrch3-1:
            sachovnica[row][col] = '*'
            count2 = count - roh3
            row = mid+1
            col = mid-1 - count2
            sachovnica[row][col] = a_or_b

        elif count <= vrch3+1:
            sachovnica[row][col] = '*'
            count2 = count - vrch3
            row = mid - count2
            col = 1
            sachovnica[row][col] = a_or_b

        elif count <= roh4:
            sachovnica[row][col] = '*'
            count2 = count - vrch3
            row = mid-1
            col = count2
            sachovnica[row][col] = a_or_b

        elif count <= vrch4-1:
            sachovnica[row][col] = '*'
            count2 = count - roh4
            row = mid-1 - count2
            col = mid-1
            sachovnica[row][col] = a_or_b

        elif hrac % 2 == 1 and count == vrch4: 
            sachovnica[row][col] = '*'
            row = 1
            col = mid
            sachovnica[row][col] = 'B'
            count = 0

        elif hrac % 2 == 0 and count == vrch4:
            sachovnica[row][col] = '*'
            row = 1
            col = mid
            sachovnica[row][col] = 'A'

        elif hrac % 2 == 0 and count > vrch4: #presun hraca A do domceka
            sachovnica[row][col] = '*'
            if col == mid and row > 1:
                sachovnica[row][col] = 'D'
            row = mid - pocet_A_panacikov
            col = mid
            sachovnica[row][col]='A'

        if hrac % 2 == 0: #vypisuje, kolke kolo hrac ide
            print('A round:'+ str(pocet_A_krokov))
        else:
            print('B round:'+ str(pocet_B_krokov))
        tlacsachovnicu(sachovnica)
        print()

if pocet_A_krokov < pocet_B_krokov: #podla poctu kol urci vitaza
    print('Vyhral hráč A!')
elif pocet_A_krokov == pocet_B_krokov:
    print('Bola to tesnotka, ale vyhral hráč A.')
else:
    print('Vyhral hráč B!')
