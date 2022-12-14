from ClassEva import Eva
import re
import ast

# function takes a string and returns the
# maximum depth nested parenthesis
def max_depth(sir):
    current_max = 0
    max = 0
    n = len(sir)

    # Traverse the input string
    for i in range(n):
        if sir[i] == '(':
            current_max += 1

            if current_max > max:
                max = current_max
        elif sir[i] == ')':
            if current_max > 0:
                current_max -= 1
            else:
                return -1

    # finally check for unbalanced string
    if current_max != 0:
        return -1

    return max

def facem_o_operatie_2(sir):
    #sir = [5, "+", 2]
    eva = Eva()

    sir_2 = list(sir)
    ok = 0
    i = 0
    n = len(sir)
    while i < n and ok == 0:
        if sir_2[i] == "+" or sir_2[i] == "-" and ok == 0:
            x = sir_2[i]
            sir_2[i] = sir_2[i - 1]
            sir_2[i - 1] = x
            # am facut swap si acum ne intoarcem pe pozitia in care avem operator
            i = i - 1
            lst = []
            lst.append(sir_2[i])
            lst.append(sir_2[i + 1])
            lst.append(sir_2[i + 2])
            sir_2[i] = eva.eval(lst)
            # stergem temermenii acare au participat la operatiunea de evaluare
            # sir[i] = sir_2[i]
            # print(sir_2[i])
            x = sir_2[0: (i + 1)]
            y = sir_2[(i + 3):]
            lst = x + y
            sir = lst
            ok = 1
        else:
            i = i + 1
    return sir

#cat timp avem de calculat adunari si scaderi
def calculam_lst_fara_paranteze_2(sir):
    sir_2 = facem_o_operatie_2(sir)
    while sir_2 != sir:
        sir = sir_2
        sir_2 = facem_o_operatie_2(sir)
    return sir


def list_to_string(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1

def recurse(node, lst):
    if isinstance(node, ast.BinOp):
        if isinstance(node.op, ast.Mult) or isinstance(node.op, ast.Div) or isinstance(node.op, ast.Pow):
            lst.append("(")
        recurse(node.left, lst)
        recurse(node.op, lst)
        recurse(node.right, lst)
        if isinstance(node.op, ast.Mult) or isinstance(node.op, ast.Div) or isinstance(node.op, ast.Pow):
            lst.append(")")
    elif isinstance(node, ast.Add):
        lst.append("+")
    elif isinstance(node, ast.Sub):
        lst.append("-")
    elif isinstance(node, ast.Mult):
        lst.append("*")
    elif isinstance(node, ast.Div):
        lst.append("/")
    elif isinstance(node, ast.Pow):
        lst.append("^^")

    elif isinstance(node, ast.Num):
        lst.append(str(node.n))
    else:
        for child in ast.iter_child_nodes(node):
            recurse(child, lst)
    return lst


def search_expr(node):
    returns = []
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.Expr):
            return child
        returns.append(search_expr(child))
    for ret in returns:
        if isinstance(ret, ast.Expr):
            return ret
    return

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def inlocuieste_cu_minus(sir):
    # sir = "3+5*-12.25-5.0-7.0"
    lst_valori = re.findall(r'[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?', sir)
    #
    #parcugem sir si salvam semnele in lst_semn
    n = len(sir)
    sir = list(sir)
    print("@@@", sir)
    #mai intai verificam daca avem un minus langa minus atunci devine plus
    #iar daca avem minus cu plus devine minus sau
    #plus cu minus obtinem minus
    #iar daca avem plus cu plus obtinem doar plus
    ok = 0
    while ok == 0:
        ok = 1
        ok_2 = 0
        i = 0
        while i < len(sir) and ok_2 == 0:
            if sir[i] == "+" and sir[i+1] == "+" and ok_2 == 0:
                x = sir[0: (i+1)]
                y = sir[(i+2):]
                sir = x + y
                ok_2 = 1
                ok = 0
            if sir[i] == "-" and sir[i+1] == "+" and ok_2 == 0:
                x = sir[0: (i + 1)]
                y = sir[(i + 2):]
                sir = x + y
                ok_2 = 1
                ok = 0
            if sir[i] == "+" and sir[i+1] == "-" and ok_2 == 0:
                sir[i] = sir[i+1]
                x = sir[0: (i + 1)]
                y = sir[(i + 2):]
                sir = x + y
                ok_2 = 1
                ok = 0
            if sir[i] == "-" and sir[i+1] == "-" and ok_2 == 0:
                x = sir[0: (i + 1)]
                y = sir[(i + 2):]
                sir = x + y
                ok_2 = 1
                ok = 0
            i = i + 1
    #avem de modificat sir daca avem: * langa - sau + si / langa - sau +
    ok = 0
    while ok == 0:
        ok = 1
        ok_2 = 0
        i = 0
        while i < len(sir) and ok_2 == 0:
            if sir[i] == "*" and sir[i + 1] == "-" and ok_2 == 0:

                pozitie_de_sters = i + 1

                i = i-1
                #parcugem de la semnul de inmultire in ordine inversa pana dam peste plus sau minu
                while sir[i] != "+" and sir[i] != "-" and i > 0:
                    i = i - 1


                if i > 0:
                    ok_3 = 0
                    if sir[i] == "+" and ok_3 == 0:
                        sir[i] = "-"
                        ok_3 = 1
                        #print("am intrat", sir[i])

                    if sir[i] == "-" and ok_3 == 0:
                        sir[i] = "+"
                if i == 0:
                    ok_3 = 0
                    if sir[i].isdigit() and ok_3 == 0:
                        sir.insert(0, "-")
                        pozitie_de_sters = pozitie_de_sters + 1
                        ok_3 = 1
                    if sir[i] == "-" and ok_3 == 0:
                        sir[i] = "+"

                x = sir[0: (pozitie_de_sters)]
                y = sir[(pozitie_de_sters + 1): ]
                sir = x + y
                ok_2 = 1
                ok = 0
            if sir[i] == "/" and sir[i + 1] == "-" and ok_2 == 0:
                pozitie_de_sters = i + 1

                i = i-1
                #parcugem de la semnul de inmultire in ordine inversa pana dam peste plus sau minu
                while sir[i] != "+" and sir[i] != "-" and i > 0:
                    i = i - 1

                if i > 0:
                    ok_3 = 0
                    if sir[i] == "+" and ok_3 == 0:
                        sir[i] = "-"
                        ok_3 = 1

                    if sir[i] == "-" and ok_3 == 0:
                        sir[i] = "+"
                if i == 0:
                    ok_3 = 0
                    if sir[i].isdigit() and ok_3 == 0:
                        sir.insert(0, "-")
                        pozitie_de_sters = pozitie_de_sters + 1
                        ok_3 = 1

                    if sir[i] == "-" and ok_3 == 0:
                        sir[i] = "+"

                x = sir[0: pozitie_de_sters]
                y = sir[(pozitie_de_sters + 1): ]
                sir = x + y
                ok_2 = 1
                ok = 0
            if sir[i] == "*" and sir[i + 1] == "+" and ok_2 == 0:
                pozitie_de_sters = i + 1

                x = sir[0: pozitie_de_sters]
                y = sir[(pozitie_de_sters + 1):]
                sir = x + y
                ok_2 = 1
                ok = 0

            if sir[i] == "/" and sir[i + 1] == "+" and ok_2 == 0:
                pozitie_de_sters = i + 1

                x = sir[0: pozitie_de_sters]
                y = sir[(pozitie_de_sters + 1):]
                sir = x + y
                ok_2 = 1
                ok = 0
            i = i + 1

    sir = list_to_string(sir)
    return sir

def facem_o_operatie(sir):
    eva = Eva()
    sir_2 = sir

    ok = 0
    i = 0
    n = len(sir)
    while i < n and ok == 0:
        if sir_2[i] == "*" or sir_2[i] == "/" and ok == 0:
            x = sir_2[i]
            sir_2[i] = sir_2[i - 1]
            sir_2[i - 1] = x
            # am facut swap si acum ne intoarcem pe pozitia in care avem operator
            i = i - 1
            lst = []
            lst.append(sir_2[i])
            lst.append(sir_2[i + 1])
            lst.append(sir_2[i + 2])
            sir_2[i] = eva.eval(lst)
            # stergem temermenii acare au participat la operatiunea de evaluare
            # sir[i] = sir_2[i]
            # print(sir_2[i])
            x = sir_2[0: (i + 1)]
            y = sir_2[(i + 3):]
            lst = x + y
            sir = lst
            ok = 1
        else:
            i = i + 1
    return sir


#facem conversia din string in float
def calculam_lst_fara_paranteze_1(sir):
    eva = Eva()
    # facem fara functia operator_first_lst aici
    n = len(sir)

    sir = list_to_string(sir)
    # daca primim un str transformam in forma adecvata de [float, str, float]



    if isinstance(sir, str):
        if len(sir) == 1:
            value = float(sir)
            sir = [value]
        else:
            lst = []
            lista_semne = []
            for i in range(0, len(sir)):
                if sir[i] == "*" or sir[i] == "/" or sir[i] == "^^" or sir[i] == "+" or sir[i] == "-":
                    lista_semne.append(sir[i])

            print("lista_semne=", lista_semne)
            lista_flaoturi = re.findall("\d+\.\d+", sir)
            res = re.findall(r"[-+]?(?:\d*\.*\d+)", sir)
            print("lista_floaturi_2=", res)
            print("lista_floaturi=", lista_flaoturi)

            #vedem care din cele 2 liste este mai mare parcurgem lista mai mica caci cea mare sigur are elementul
            #care incepe cu - in fata


            # if len(lista_flaoturi) < len(res):
            #     #inseram valoarea de pe prima pozitie din res in lista_floaturi
            #     value = res[0]
            #     lista_flaoturi.insert(0, value)
            #
            #     #stergem minusul de pe prima pozitie din lista de semne caci e deja pus la elementul din lista_floaturi
            #     lista_semne = lista_semne[1:]

            if len(lista_flaoturi) < len(res):

                value = res[0]
                value = float(value)
                if value < 0:
                    # inseram valoarea de pe prima pozitie din res in lista_floaturi
                    value = res[0]
                    lista_flaoturi.insert(0, value)

                    # stergem minusul de pe prima pozitie din lista de semne caci e deja pus la elementul din lista_floaturi
                    lista_semne = lista_semne[1:]

                    for i in range(1, len(res)):
                        y = float(res[i])
                        if y < 0:
                            y = -1 * y
                            res[i] = str(y)

                    lista_flaoturi = res

                else:
                    for i in range(0, len(res)):
                        y = float(res[i])
                        if y < 0:
                            y = -1 * y
                            res[i] = str(y)
                    lista_flaoturi = res


            for i in range(0, len(lista_flaoturi)):
                lista_flaoturi[i] = float(lista_flaoturi[i])


            for i in range(0, len(lista_flaoturi)):
                if i == 0:
                    lst.append(lista_flaoturi[i])
                if i > 0:
                    lst.append(lista_semne[i - 1])
                    lst.append(lista_flaoturi[i])
            sir = lst
            if isinstance(sir[0], float):
                value = sir[0]
                if value < 0:
                    #stermegm float de pe pozitia 0 din sir si facem in ele "-", float
                    value = -1 * value
                    sir[0] = value
                    sir.insert(0, "-")


    print("SIR=", sir)

    sir_2 = facem_o_operatie(sir)
    while sir_2 != sir:
        sir = sir_2
        sir_2 = facem_o_operatie(sir)

    return sir

def calculam_lst_fara_paranteze(sir):
    eva = Eva()

    n = len(sir)

    formula = sir
    #print(type(formula))
    #formula = list(formula)
    #formula = list_to_string(formula)

    #trebuie calculat mai intaii rad, log, sin, cos
    # in formula o sa avem rad termen , fara paranteze

    contor = 0
    lst = []
    lst_2 = []
    numar = ""
    i = 0
    n = len(formula)
    while i < n:
        if formula[i] == "*" or formula[i] == "/" or formula[i] == "^" or formula[i] == "+" or formula[i] == "-":
            contor = 0
        if formula[i] == "r" or formula[i] == "l" or formula[i] == "s" or formula[i] == "c" and contor == 0:
            lst_2 = []
            operator = formula[i] + formula[i+1] + formula[i+2]
            numar = ""
            lst_2.append(operator)
            i = i + 2
            contor = 1
        if contor == 1:
            if formula[i] == ".":
                numar = numar + "."
            if formula[i].isdigit():
                numar = numar + formula[i]
            if i + 1 == n:
                lst_2.append(numar)
                lst.append(lst_2)
                contor = 0
            if contor == 1:
                if formula[i+1] == "*" or formula[i+1] == "/" or formula[i+1] == "^" or formula[i+1] == "+" or formula[i+1] == "-":
                    lst_2.append(numar)
                    lst.append(lst_2)
                    contor = 0

        i = i + 1

    #schimbam din lst toate valorile in care avem numar sub forma de str si il transformam in float si calculam
    #valoarea sa matematica

    n = len(lst)
    for i in range(0, n):
        lst_2 = lst[i]
        lst_2[1] = float(lst_2[1])
        value = eva.eval(lst_2)
        lst[i] = str(value)

    #trebuie sa modificam valorile din formula cu cele din lst

    formula = list(formula)
    print("formula_2=", formula)
    n = len(formula)
    contor = 0
    pozitie_initiala = -1
    pozitie_finala = -1
    for k in range(0, len(lst)):
        ok = 0
        n = len(formula)
        contor = 0
        i = 0
        while ok == 0 and i < n:
            if formula[i] == "r" and formula[i+1] == "a" and formula[i+2] == "d" and contor ==0:
                pozitie_initiala = i
                print("pozitie_initiala=", pozitie_initiala)
                formula[i] = lst[k]
                contor = 1
            if formula[i] == "l" and formula[i+1] == "o" and formula[i+2] == "g" and contor ==0:
                pozitie_initiala = i
                formula[i] = lst[k]
                contor = 1
            if formula[i] == "s" and formula[i+1] == "i" and formula[i+2] == "n" and contor ==0:
                pozitie_initiala = i
                formula[i] = lst[k]
                contor = 1
            if formula[i] == "c" and formula[i+1] == "o" and formula[i+2] == "s" and contor ==0:
                pozitie_initiala = i
                formula[i] = lst[k]
                contor = 1
            if contor == 1:
                if i+1 == n:
                    pozitie_finala = i
                    x = formula[0: (pozitie_initiala+1)]
                    formula = x
                    contor = 0
                    ok = 1
                if contor == 1:
                    if formula[i] == "*" or formula[i] == "/" or formula[i] == "^" or formula[i] == "+" or formula[i] == "-":
                        pozitie_finala = i
                        x = formula[0: (pozitie_initiala+1)]
                        y = formula[(pozitie_finala):]
                        formula = x + y
                        contor = 0
                        ok = 1
            i = i + 1

    #trebuie sa modificam din caracterul ^^ in **
    print("formula_3 = ", formula)

    ok_3 = 0

    if "rad" not in formula and "log" not in formula and "sin" not in formula and "cos" not in formula:
        #facem formula din lista in str
        formula = list_to_string(formula)

        formula = inlocuieste_cu_minus(formula)

        #print("formula=", formula)

        #am inlucuit semnul de putere cu **
        res = formula.replace("^", "*")

        formula = res

        print("formula=", formula)

        # extragem numerele din formula si le punem in lst_3

        # adaugam paranteze cu unde avem operatiile de putere, inmultire si impartire
        #result = re.findall(r'[-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?', formula)
        #print("result = ", result)

        #in formula daca avem semnul minus langa un alt semn:inmnultire, impartire atunci schimbam valoarea celui mai apropiat semn de el
        # ce are valoare + din partea sa stanga cu -
        # daca e minus langa plus atunci pastram doar -


        a = ast.parse(formula)

        expr = search_expr(a)

        lst = []
        afisat = recurse(expr, lst)

        if formula[0] == "-":
            #parcurgem afisat pana cand dam peste primul numar, in drum putem avea paranteze
            ok = 0
            i = 0
            while i < len(afisat) and ok == 0:
                if afisat[i].isdigit() and ok == 0:
                    afisat[i] = "-" + afisat[i]
                    ok = 1
                i = i + 1

        print("afisat= ", afisat)
        sir = list_to_string(afisat)
    else:
        #aici formula poate sa arate de forma: ["1", "+", "rad", "2", ".", "6"]
        #trebuie sa extragem din formula_3 incepand de la rad si sa inlocuim cu valoarea adecvata
        n = len(formula)
        ok_2 = 0
        i = 0
        while i < n and ok_2 == 0:
            if formula[i] == "rad" or formula[i] == "log" or formula[i] == "sin" or formula[i] == "cos" and ok_2 == 0:
                #extragem pana dam peste un semn
                x = formula[i+1:]
                sir_temporar = []
                ok_7 = 0
                j = 0

                while j < len(x) and ok_7 == 0:
                    if x[j] != "+" and x[j] != "-" and x [j] != "*" and x[j] != "/":
                        sir_temporar.append(x[j])
                        j = j + 1
                    else:
                        ok_7 = 1

                # continuam sa luam restul din x ca sa repunem la final dupa ce am calculat radicalul
                sir_temporar_2 = x[j:]

                print("sir_temporar=", sir_temporar_2)
                x = sir_temporar

                x = list_to_string(x)
                x = float(x)
                lst_3 = [formula[i]]
                lst_3.append(x)
                value = eva.eval(lst_3)
                formula[i] = str(value)
                formula = formula[0:(i+1)]
                sir_prelucrat = formula[i]
                #stergem ultimul element si il facem intr-o lista
                sir_prelucrat = list(sir_prelucrat)

                formula = formula[:-1]

                #il bagam caracter cu caracter din sir_prelucrat in formula
                for j in range(0, len(sir_prelucrat)):
                    formula.append(sir_prelucrat[j])
                #print("sir_prelucrat= ", formula)

                #trebuie sa adaugam la formula restul de calcul dupa ce am calculat radicalul
                formula = formula + sir_temporar_2

                ok_2 = 1
            i = i + 1
        print("formula=", formula)
        afisat = formula
        sir = list_to_string(afisat)



    adancime = max_depth(sir)

    if adancime > 0:
        while adancime > 0:
            n = len(afisat)
            contor = 0
            # in lst vom avea avea toate perechile de paranteze in care avem si adancimea maxima
            lst = []
            lst_2 = []
            i = 0
            while i < n:
                if afisat[i] == "(":
                    contor = contor + 1
                    lst_2 = []
                if contor == adancime and afisat[i] == ")":
                    lst.append(lst_2)
                if afisat[i] == ")":
                    contor = contor - 1
                if contor == adancime and afisat[i] != "(":
                    lst_2.append(afisat[i])
                i = i + 1
            print("lst =", lst)
            # de calculat valoarea pentru fiecare pereche de paranteze si de inlocuit in formula

            n = len(lst)
            for i in range(0, n):
                lst_2 = lst[i]
                if len(lst_2) > 1:
                    # facem swap intre valoarea din lst_2 de pe pozitia 0 cu cea de pe pozitia 1 unde se afla semn
                    x = float(lst_2[0])
                    lst_2[0] = lst_2[1]
                    lst_2[1] = x
                    # transformam al doilea termen din lst_2 in float
                    lst_2[2] = float(lst_2[2])
                else:
                    lst_2 = float(lst_2[0])
                # calculam expresia
                value = eva.eval(lst_2)
                # inseram value in lst sub forma de str
                lst[i] = str(value)
            print("lst=", lst)

            # schimbam ceea ce se afla intre parantezele cand ajungem la valoarea adancimii= max_depth cat si parantezele se modifica
            # inlocuind tot cu valoarea corespunzatoare din lst, prima valoare pentru prima pereche gasita de paranteze
            # a doua pentru a doua etc.
            for k in range(0, len(lst)):
                n = len(afisat)
                contor = 0
                # in lst vom avea avea toate perechile de paranteze in care avem si adancimea maxima
                pozitie_initiala = -1
                pozitie_finala = -1
                i = 0
                ok = 0
                while i < n and ok == 0:
                    if afisat[i] == "(":
                        contor = contor + 1

                    if contor == adancime and afisat[i] == "(":
                        afisat[i] = lst[k]
                        pozitie_initiala = i

                    if contor == adancime and afisat[i] == ")":
                        pozitie_finala = i
                        ok = 1

                    if afisat[i] == ")":
                        contor = contor - 1
                        if ok == 1:
                            x = afisat[0: (pozitie_initiala+1)]
                            y = afisat[(pozitie_finala+1):]
                            afisat = x + y
                    i = i + 1
            print("afisat= ", afisat)
            adancime = adancime - 1
    #adancime are nivel 0 deci avem de rezolvat doar adunari, scaderi caci radicalii i-am rezolvat la inceput



    if "*" in afisat or "/" in afisat:
        # facem ca afisat sa aiba forma lui sir de mai jos
        # adica trebuie sa transformam numerele in float
        # sir = [5, "*", 2]
        afisat = list_to_string(afisat)
        afisat = inlocuieste_cu_minus(afisat)

        print("@@@@@@", afisat)
        afisat = calculam_lst_fara_paranteze_1(afisat)
        print("@@@@@@", afisat)


    print("@@", afisat)
    #convertim floaturile din afisat in str
    for i in range(0, len(afisat)):
        if isinstance(afisat[i], float) or isinstance(afisat[i], int):
            afisat[i] = str(afisat[i])

    #daca avem doar un numar
    if "+" not in afisat and "-" not in afisat and "*" not in afisat and "/" not in afisat:
        afisat = list_to_string(afisat)
        afisat = [float(afisat)]
    else:
        #if ok_3 == 0:
        #facem afisat mai intai sa fie string si extragem toate floaturile din el
        afisat = list_to_string(afisat)

        print("afisat_nou", afisat)
        lst = []
        lista_semne = []
        for i in range(0, len(afisat)):
            if afisat[i] == "+" or afisat[i] == "-":
                lista_semne.append(afisat[i])

        print("lista_semne=", lista_semne)
        lista_flaoturi = re.findall("\d+\.\d+", afisat)
        res = re.findall(r"[-+]?(?:\d*\.*\d+)", afisat)
        print("lista_floaturi_2=", res)
        print("lista_floaturi=", lista_flaoturi)

        # vedem care din cele 2 liste este mai mare parcurgem lista mai mica caci cea mare sigur are elementul
        # care incepe cu - in fata


        ok_8 = 0

        if len(lista_flaoturi) < len(res):

            value = res[0]
            value = float(value)
            if value < 0:
                # inseram valoarea de pe prima pozitie din res in lista_floaturi
                value = res[0]
                lista_flaoturi.insert(0, value)

                # stergem minusul de pe prima pozitie din lista de semne caci e deja pus la elementul din lista_floaturi
                lista_semne = lista_semne[1:]

                for i in range(1, len(res)):
                    y = float(res[i])
                    if y < 0:
                        y = -1 * y
                        res[i] = str(y)

                ok_8 = 1

            else:
                for i in range(0, len(res)):
                    y = float(res[i])
                    if y < 0:
                        y = -1 * y
                        res[i] = str(y)


        elif len(res) == len(lista_flaoturi):
            value = res[0]
            value = float(value)

            if value < 0:
                # stermegm float de pe pozitia 0 din sir si facem in ele "-", float
                value = -1 * value
                res[0] = str(value)
                res.insert(0, "-")

                ok_8 = 1

            res = lista_flaoturi


        lista_flaoturi = res
        print("lista_floaturi=", lista_flaoturi)

        for i in range(0, len(lista_flaoturi)):
            lista_flaoturi[i] = float(lista_flaoturi[i])

        for i in range(0, len(lista_flaoturi)):
            if i == 0:
                lst.append(lista_flaoturi[i])
            if i > 0:
                lst.append(lista_semne[i - 1])
                lst.append(lista_flaoturi[i])

        if ok_8 == 1:
            lst[0] = -1 * lst[0]
        afisat = lst

        print("printat=", afisat)


        n = len(afisat)
        for i in range(0, n):
            if afisat[i] != "+" and afisat[i] != "-":
                afisat[i] = float(afisat[i])

    print("afisat= ", afisat)
    afisat = calculam_lst_fara_paranteze_2(afisat)
    print("afisat= ", afisat)
    #else:
        #transformam din str in float numerele

    return  afisat

def rezolva_parantezele(sir):
    #facem sir din lst intr-un str
    #vedem care este max depth-ul maxim
    #parcurgem pana la max dept-ul maxim transformam in lst, cream intr-un alt list lista_fianala
    sir = list_to_string(sir)
    n = len(sir)
    lst =[]
    lst_nivele = []
    lst_max_aparitii_paranteza = []
    #max_depth nu functioneaza trebuie sa luam separat
    #max_depth returneaza adancitura maxima posibila

    #parcugem prin sir pana ajungem la nivelul max_depth rezolvam paranteza in care ne aflam
    #update la sir
    #max_depth din nou pe sir
    #parcugem prin sir pana ajungem la nivelul max_depth rezolvam paranteza in care ne aflam
    #pana cand max_depth devine 0 si calculam tot sirul

    #in lst_2 vor aparea toate valorile distince ale lui lst

    print(sir)
    print(max_depth(sir))
    adancime = max_depth(sir)

    ok_2 = 0
    while ok_2 == 0:
        contor = 0
        i = 0
        lst = []
        lst_2 = []
        while i < n:
            if sir[i] == "(":
                contor = contor + 1
            if contor == adancime and sir[i] == "(":
                lst = []
            if contor == adancime and sir[i] != "(" and sir[i] != ")":
                #daca dam peste rad, log, sin, cos atunci le facem un singur str si inseram in lista
                if sir[i] == "r" or sir[i] == "l" or sir[i] == "s" or sir[i] == "c":
                    value = ""
                    value = sir[i] + sir[i+1] + sir[i+2]
                    i = i + 2
                else:
                    value = sir[i]
                lst.append(value)
            if sir[i] == ")":
                #verificam ca nu e gol lst
                if len(lst) > 0:
                    if (lst in lst_2) == False:
                        lst_2.append(lst)
                contor = contor - 1
            i = i + 1
        n = len(lst_2)
        #in lst_2_value vom avea toate valorile calculate pentru lst_2
        lst_2_value = []
        #in lst_3 vom avea sub forma de tuple pe lst_2
        lst_3 = []
        for i in range(0, n):
            #am facut in tuplu lista curenta din lst_2
            value_2 = tuple(lst_2[i])
            lst_3.append(value_2)
            #punem aceasta lista curenta in lst_3
            value = list(lst_3[i])
            #extragem sub forma de lista lista_curenta si calculam pe lista curenta valoarea
            print("value=", value)
            value = calculam_lst_fara_paranteze(value)
            #inserama valoare sub forma de str in lista de valori
            if isinstance(value, list) == False:
                #inseram valoarea in lista de valori
                value = str(value)
                lst_2_value.append(value)
            else:
                #print("values=", value)
                #value = value[0]
                value = str(value[0])
                lst_2_value.append(value)

        print("lst_2=", lst_2)
        print("lst_2_value=", lst_2_value)

        #parcurgem din nou sirul si cand ajungem la adancimea maxima salvam pozitia de start si final si
        #inlucuim cu valoarea din lst_2_value adecvata

        lst_parcurs = list(sir)
        for i in range(0, len(lst_2_value)):
            n = len(lst_parcurs)
            j = 0
            pozitie_initiala = -1
            pozitie_finala = -1
            ok = 0
            contor = 0
            while j < n and ok == 0:
                if lst_parcurs[j] == "(":
                    contor = contor + 1
                    if contor == adancime:
                        pozitie_initiala = j
                        lst_parcurs[pozitie_initiala] = lst_2_value[i]

                if lst_parcurs[j] == ")":
                    pozitie_finala = j
                    if contor == adancime:
                        ok =1
                    contor = contor - 1

                j = j + 1
            if pozitie_finala != -1 and pozitie_initiala != -1:
                x = lst_parcurs[0: (pozitie_initiala+1)]
                y = lst_parcurs[(pozitie_finala+1):]
                lst_parcurs = x + y
        sir_nou = list_to_string(lst_parcurs)
        print("sir_before_update_depth", sir_nou)
        adancime = max_depth(sir_nou)
        n = len(sir_nou)
        sir = sir_nou
        if adancime > 0:
            ok_2 = 0
        else:
            ok_2 = 1

    # am ajuns la adancime 0 adica nu mai avem paranteze de rezolvat deci
    # aplicam o singura data functia calculeaza_lst_fara_paranteze

    sir = inlocuieste_cu_minus(sir)

    sir = calculam_lst_fara_paranteze(sir)

    # trebuie sa prelucram sir daca avem minus langa inmultit etc

    return  sir


# in matrice vom avea combinat sub forma de lista de 2 elemente rad si cu termenul pe care aplicam

#exemplu de cum functioneaza rezolva matrice
#sir = ['3', '+', '5', '*', ['6', '/', '(', '7', '+', '1', ')', '-', '4']]
#print(rezolva_matrice(sir))
#print()

eva = Eva()
# print(eva.eval(1))
# print(eva.eval(['+', 1, 5]))
# print(eva.eval(['+', ['+', 3, 2], 5]))
# print(eva.eval(['+', ['-', 3, 2], 5]))
# print(eva.eval(['+', ['*', 3, 2], 5]))
# print(eva.eval(['+', ['/', 3, 2], 5]))
# print(eva.eval(['+', ['^^', 3, 2], 5]))
# print(eva.eval(['+', ['rad', 4], 5]))
# print(eva.eval(['+', ['log', 3], 5]))
# print(eva.eval(['+', ['sin', 2], 5]))
# print(eva.eval(['+', ['sin', 2], 5]))

# avem functie de max depth de paranteze pe net
# inlocuim unde intalnim prima data cu paranteze cu z
# ca sa evaluam doar facem swapuri ca sa avem pozitia potrivita pentru eval
#sir = "2 * (3 + 5 / 4) - (5 ^^ 2 + 8) / rad(9)"
#sir = "2 * (3 + 5 * ( 6 - 4)) - (5 ^^ 2 + 8) / rad(9)"
#sir = "2 * (3 + 5 * ( 6 / (7 + 1)- 4)) - (3 + 5 ^^ 2 / 8) / rad(9+5)"
#sir = "1 + (2 * (3 + 5 * ( 6 / (7 + 1)- 4)) - rad(9+5) / (3 + 5 ^^ 2 / 8))"
sir = "2 * (3 + 5 * ( 6 / (7 + 1) - ( 8 + 5)) - (((5))) - (((7))) ) - (3 + 5 * ( 6 / (7 + 1)- 4)) / (1 + rad(log(9+5)))"
#sir = "1 + 2 - rad(5+3) + sin(3)"
#sir = "0 + ( 6 / (7 + 1)- 4) / 1"

#sir = "5 + 3 ^^ 2 / 4 - 7 + rad 5 * cos 7 + rad 12 / cos 3.5"

#stergem toate spatiile goale (whitespaces-urile) din sir
sir = sir.replace(" ", "")

#verificare formule cu wolframalpha

sir = rezolva_parantezele(sir)

print('@', sir)

print("rezultat = ",sir)

#print(eva.eval(["cos", 3.5]))


"""
# facem ca listele cu un singur element sa devina str
def list_to_str(sir):
    for i in range(0, len(sir)):
        sir_2 = sir[i]
        if isinstance(sir_2, list):
            if len(sir_2) == 1:
                numar = ""
                for j in range(0, len(sir_2)):
                    numar = numar + sir_2[j]
                sir[i] = numar
    return sir

def avem_lista(sir):
    if type(sir) is list:
        return True
    else:
        return False

def sterge_o_paranteza(sir):
    ok_sinus = 0
    count = 0
    matrice = []
    for i in range(0, len(sir)):
        if (sir[i] == "(" and ok_sinus == 0):
            sir[i] = "z"
            ok_sinus = 1
            # numaram cate paranteze ) avem
            count = 1
            continue

        if ok_sinus == 1:
            if sir[i] == "(":
                count = count + 1
            if sir[i] == ")":
                count = count - 1
                if count == 0:
                    sir[i] = "z"
                    ok_sinus = 0

    ok_sinus = 0
    lst = []
    for i in range(0, len(sir)):
        if sir[i] == "z" and ok_sinus == 0:
            lst = []
            ok_sinus = 1
            continue
        if sir[i] == "z" and ok_sinus == 1:
            ok_sinus = 0
            matrice.append(lst)
            continue
        if ok_sinus == 1:
            lst.append(sir[i])
        if ok_sinus == 0 and i < len(sir):
            matrice.append(sir[i])
    return matrice

#primeste ca input o lista in care avem paranteze si extragem tot ce avem intre paranteze intr-o lista pe care
#o salvam intr-o matrice dupa repetam aceasi operatiune pana nu mai avem paranteze iar la final in matrice vom
#avea tot intre primul grup de paranteze dupa al doilea etc.
#in print avem cum functioneaza
def rezolva_matrice(sir):
    matrice = []
    sir_initial = sir
    matrice.append(sir)
    sir = sterge_o_paranteza(sir)
    sir = list_to_str(sir)
    #print()
    ok = 1
    while ok != 0:
        ok = 0
        i = 0
        #print(sir)
        while i < len(sir) and ok == 0:
            if isinstance(sir[i], list) and ok == 0:
                #daca am ajuns la ultima lista doar o adaugam si terminam cu tot
                if max_depth(sir[i]) == 0:
                    matrice.append(sir[i])
                    break
                else:
                    sir_2 = sir[i]
                    sir_2 = sterge_o_paranteza(sir_2)
                    sir_2 = list_to_str(sir_2)
                    matrice.append(sir_2)
                    sir = matrice[len(matrice) - 1]
                    ok = 1
            i = i + 1

    print(matrice)
    #dupa ce am spart expresia in expresii mai mici vom avea niste delimitari de z atunci cand le-am spart si trebuie eliminat
    #z se afla in lista din lista
    n = len(matrice)
    for i in range(0, n):
        sir_2 = matrice[i]
        m = len(sir_2)
        for j in range(0, m):
            if isinstance(sir_2[j], list) and "z" in sir_2[j]:
                lst = []
                lst_2 = []
                sir_3 = sir_2[j]
                #cand dam peste o valoare z crestem ok la 1 ca sa bagam in lst_2
                ok = 0
                for k in range(0, len(sir_3)):
                    # am dat a doua oara peste z, inseram in lst pe lst_2 si ok devine 0
                    if sir_3[k] == "z" and ok == 1:
                        lst.append(lst_2)
                        lst_2 = []
                        ok = 0
                    if sir_3[k] != "z" and ok == 1:
                        lst_2.append(sir_3[k])
                    if sir_3[k] != "z" and ok == 0:
                        lst.append(sir_3[k])
                    # am dat prima oara peste z
                    if sir_3[k] == "z" and ok == 0:
                        ok = 1
                sir_2[j] = lst
        matrice[i] = sir_2
    return matrice

def intalnim_rad_log_trigo(matrice):
    n = len(matrice)
    for i in range(0, n):
        if matrice[i] == "rad" or matrice[i] == "log" or matrice[i] == "sin" or matrice[i] == "cos":
            lst = []
            lst.append(matrice[i])
            i = i + 1
            lst.append(matrice[i])
            matrice[i - 1] = lst
            x = matrice[0: i]
            y = matrice[i+1:]
            matrice = x + y
            break
    return matrice

# punem intr-o lista de 2 elemente rad, log, ...
def facem_lista_2_elemente(matrice):
    matrice_2 = intalnim_rad_log_trigo(matrice)
    while matrice_2 != matrice:
        matrice = matrice_2
        matrice_2 = intalnim_rad_log_trigo(matrice)
    return matrice

# punem intr-o lista de 3 elemente Operatie termen1 termen2
def facem_lista_3_elemente(matrice):
    ok = 0
    pozitie_inserat_lst = 0
    pozitie_sters_1 = 0
    pozitie_sters_2 = 0

    #ok = 0 nu am dat peste o pereche de operatie termen1 termen2
    while ok == 0:
        n = len(matrice)
        ok = 1
        ok_2 = 0
        #ok_2 = 0 nu am bagat in lst operatie termen1 termen2
        #ok_2 = 1 am bagat in lst si iesim cu pzotiile necesare de sarit pentru lst curent
        i = 0
        while i < n and ok_2 == 0:
            if matrice[i] == "*" or matrice[i] == "/" or matrice[i] == "^^":
                lst = []
                lst.append(matrice[i])
                pozitie_inserat_lst = i

                i = i + 1
                pozitie_sters_1 = i
                lst.append(matrice[i])

                i = i + 1
                pozitie_sters_2 = i
                lst.append(matrice[i])
                matrice[pozitie_inserat_lst] = lst

                ok_2 = 1
                ok = 0
            i = i + 1

        # punem in matrice_2 toate elementele pana la pozitie_de_sters 1 si 2 sarim pozitia de sters si punem iar tot ce prindem
        if ok == 0:
            n = len(matrice)
            matrice_2 = []
            for i in range(0, n):
                if i != pozitie_sters_1 and i != pozitie_sters_2:
                    matrice_2.append(matrice[i])
            matrice = matrice_2
    return matrice

#facem ca operator sa fie primul in lista
#interschimbam valoarile astfel incat in operatie de inmultire si impartire sa fie mai intai caracterul *
def operator_first_lst(matrice):
    n = len(matrice)
    for i in range(0, n):
        if matrice[i] == "*" or matrice[i] == "/" or matrice[i] == "^^":
            x = matrice[i]
            matrice[i] = matrice[i - 1]
            matrice[i - 1] = x
    return matrice

def facem_o_operatie(sir):
    eva = Eva()
    sir_2 = sir
    ok = 0
    i = 0
    n = len(sir)
    while i < n and ok == 0:
        if sir_2[i] == "*" or sir_2[i] == "/" or sir_2[i] == "^^" and ok == 0:
            x = sir_2[i]
            sir_2[i] = sir_2[i - 1]
            sir_2[i - 1] = x
            # am facut swap si acum ne intoarcem pe pozitia in care avem operator
            i = i - 1
            lst = []
            lst.append(sir_2[i])
            lst.append(sir_2[i + 1])
            lst.append(sir_2[i + 2])
            sir_2[i] = eva.eval(lst)
            # stergem temermenii acare au participat la operatiunea de evaluare
            # sir[i] = sir_2[i]
            # print(sir_2[i])
            x = sir_2[0: (i + 1)]
            y = sir_2[(i + 3):]
            lst = x + y
            sir = lst
            ok = 1
        else:
            i = i + 1
    return sir

#facem conversia din string in float
def calculam_lst_fara_paranteze_1(sir):
    eva = Eva()
    # facem fara functia operator_first_lst aici
    n = len(sir)

    sir = list_to_string(sir)
    # daca primim un str transformam in forma adecvata de [float, str, float]
    if isinstance(sir, str):
        if len(sir) == 1:
            value = float(sir)
            sir = [value]
        else:
            lst = []
            lista_semne = []
            for i in range(0, len(sir)):
                if sir[i] == "*" or sir[i] == "/" or sir[i] == "^^" or sir[i] == "+" or sir[i] == "-":
                    lista_semne.append(sir[i])
            lista_flaoturi = re.findall("\d+\.\d+", sir)
            for i in range(0, len(lista_flaoturi)):
                lista_flaoturi[i] = float(lista_flaoturi[i])
            for i in range(0, len(lista_flaoturi)):
                if i == 0:
                    lst.append(lista_flaoturi[i])
                if i > 0:
                    lst.append(lista_semne[i - 1])
                    lst.append(lista_flaoturi[i])
            sir = lst


    sir_2 = facem_o_operatie(sir)
    while sir_2 != sir:
        sir = sir_2
        sir_2 = facem_o_operatie(sir)

    return sir

#la fel ca la operatiile de *, / si ^^ doar ca pentru + sau -
def facem_o_operatie_2(sir):
    #sir = [5, "+", 2]
    eva = Eva()

    sir = list_to_string(sir)
    #daca primim un str transformam in forma adecvata de [float, str, float]
    if isinstance(sir, str):
        if len(sir) == 1:
            value = float(sir)
            sir = [value]
        else:
            lst = []
            lista_semne = []
            for i in range(0 ,len(sir)):
                if sir[i] == "+" or sir[i] == "-":
                    lista_semne.append(sir[i])
            lista_flaoturi = re.findall("\d+\.\d+", sir)
            for i in range(0, len(lista_flaoturi)):
                lista_flaoturi[i] = float(lista_flaoturi[i])
            for i in range(0, len(lista_flaoturi)):
                if i == 0:
                    lst.append(lista_flaoturi[i])
                if i > 0:
                        lst.append(lista_semne[i-1])
                        lst.append(lista_flaoturi[i])
            sir = lst

    sir_2 = sir
    ok = 0
    i = 0
    n = len(sir)
    while i < n and ok == 0:
        if sir_2[i] == "+" or sir_2[i] == "-" and ok == 0:
            x = sir_2[i]
            sir_2[i] = sir_2[i - 1]
            sir_2[i - 1] = x
            # am facut swap si acum ne intoarcem pe pozitia in care avem operator
            i = i - 1
            lst = []
            lst.append(sir_2[i])
            lst.append(sir_2[i + 1])
            lst.append(sir_2[i + 2])
            sir_2[i] = eva.eval(lst)
            # stergem temermenii acare au participat la operatiunea de evaluare
            # sir[i] = sir_2[i]
            # print(sir_2[i])
            x = sir_2[0: (i + 1)]
            y = sir_2[(i + 3):]
            lst = x + y
            sir = lst
            ok = 1
        else:
            i = i + 1
    return sir

#cat timp avem de calculat adunari si scaderi
def calculam_lst_fara_paranteze_2(sir):
    sir_2 = facem_o_operatie_2(sir)
    while sir_2 != sir:
        sir = sir_2
        sir_2 = facem_o_operatie_2(sir)
    return sir

def facem_o_operatie_3(sir):
    eva = Eva()
    sir_2 = facem_lista_2_elemente(sir)
    n = len(sir_2)
    for i in range(0, n):
        if isinstance(sir_2[i], list):
            sir_3 = sir_2[i]
            m = len(sir_3)
            for j in range(0, m):
                if sir_3[j].isnumeric():
                    sir_3[j] = float(sir_3[j])
            sir_3 = eva.eval(sir_3)
            sir_2[i] = sir_3
    sir = sir_2
    return sir

def calculam_lst_fara_paranteze_3(sir):
    sir_2 = facem_o_operatie_3(sir)
    while sir_2 != sir:
        sir = sir_2
        sir_2 = facem_o_operatie_3(sir)
    return sir

def calculam_lst_fara_paranteze(sir):
    #sir = [5, "*", 2]
    # daca primim un str transformam in forma adecvata de [float, str, float]
    print("value_sir=", sir)


    #daca avem lungime 1 atunci il punem in sir ca float daca e numar si semn altfel
    if len(sir) == 1 and isinstance(sir[0], list) == False:
        if sir[0] == "+" or sir[0] == "-" or sir[0] == "*" or sir[0] == "/" or sir[0] == "^^" or sir[0] == "rad" \
            or sir[0] == "sin" or sir[0] == "cos" or sir[0] == "log":
                return sir
        else:
            valoare = str(sir[0])
            return float(valoare)
    else:
        #daca avem doar o forma simpla operator termen
        if isinstance(sir, list) and (len(sir) == 2):
            sir[1] = float(sir[1])
            sir = eva.eval(sir)
            return sir
        else:
            #mai intai calculam radicalii, logaritmii, sin, cos
            sir = calculam_lst_fara_paranteze_3(sir)
            sir = calculam_lst_fara_paranteze_1(sir)
            sir = calculam_lst_fara_paranteze_2(sir)
            return sir
"""


"""
lst = []
# despartem elminam spatiile goale si facem ca si caracter separat in lista functiile calulatorului + parantezele
for i in range(0, len(sir)):
    ok = 0
    if len(sir[i]) > 1:
        if "rad" in sir[i] or "log" in sir[i] or "sin" in sir[i] or "cos" in sir[i]:
            sir_2 = sir[i]
            numar = sir_2[0] + sir_2[1] + sir_2[2]
            lst.append(numar)
            lst.append(sir_2[3])
            sir[i] = sir_2[4:]
            sir_2 = sir[i]
            # daca avem doar numar si paranteza la final ex: 123) stergem paranteza si verificam daca e numar
            sir_3 = sir_2[:-1]
            if sir_3.isnumeric() == True:
                lst.append(sir_3)
                lst.append(")")
            else:
                for j in range(0, len(sir_2)):
                    lst.append(sir_2[j])

        elif "^^" in sir[i]:
            sir_2 = "^^"
            lst.append(sir_2)

        else:
            # aici avem doar numere de forma : 123, (456, 789)
            # daca avem numar il punem cu totul ca string in matrice
            if "(" in sir[i] or ")" in sir[i]:
                # daca avem numar care incepe mai intai cu ( ex : (888 sau ((888
                if "(" in sir[i]:
                    sir_2 = sir[i]
                    contor = 0
                    for j in range(0, len(sir_2)):
                        if sir_2[j] == "(":
                            # punem paranteza
                            lst.append(sir_2[j])
                            contor = contor + 1
                    sir_2 = sir_2[contor:]
                    # punem numar
                    lst.append(sir_2)

                # daca numarul se termina cu ) ex: 777) sau 777))
                if ")" in sir[i]:
                    sir_2 = sir[i]
                    numar = ""
                    for j in range(0, len(sir_2)):
                        if sir_2[j] >= '0' and sir_2[j] <= '9':
                            numar = numar + sir_2[j]
                    # punem numar
                    lst.append(numar)
                    # punem paranteza
                    index = len(numar)
                    # taiem numarul din sir
                    sir_2 = sir_2[index:]
                    for j in range(0, len(sir_2)):
                        lst.append(sir_2[j])
            else:
                sir_2 = sir[i]
                if sir_2.isnumeric() == True:
                    lst.append(sir_2)
    else:
        lst.append(sir[i])
sir = lst

matrice = sterge_o_paranteza(sir)
matrice = list_to_str(matrice)

#aici vedem cum am prelucrat paranteleze inlocuind cu z in sir
#iar matrice inlocuieste ceea ce este intre z cu o lista
print(sir)
print(matrice)
print()
print()
matrice = facem_lista_2_elemente(matrice)

#interschimbam valoarile astfel incat in operatie de inmultire si impartire sa fie mai intai caracterul *
matrice = operator_first_lst(matrice)

matrice = facem_lista_3_elemente(matrice)
print("@@",matrice)


#trebuie sa transformam toate parantezele in list
lst_nivele = []
lst_max_dept_fiecare_paranteza = []
#facem o functie in care dam un list si facem ca fiecare paranteza sa devina un list
n = len(matrice)
for i in range(0, n):
    sir_5 = matrice[i]
    if isinstance(sir_5, list):
        m = len(sir_5)
        for j in range(0, m):
            if isinstance(sir_5[j], list):
                #verificam daca lista incepe cu rad, log, sin, cos, daca da atunci trebuie sa mai extragem o lista
                sir_6 = sir_5[j]
                if sir_6[0] == "rad" or sir_6 == "log" or sir_6 == "sin" or sir_6 == "cos":
                    sir_5[j] = sir_6[1]
                    print("sir_5_2", sir_5[j])
                    print("sir_5=", rezolva_parantezele(sir_5[j]))
                else:
                    print("sir_5_2", sir_5[j])
                    print("sir_5=", rezolva_parantezele(sir_5[j]))




#sir = ["1", "+", "rad", "5", "*", "3"]
#print("raspuns=", calculam_lst_fara_paranteze(sir))


n = len(matrice)
ecuatie_finala = []
for i in range(0, n):
    #de la rezolva matrice avem afisata in bucatele fiecare termen din ecuatie
    matrice_2 = rezolva_matrice(matrice[i])
    lst_value_2 = matrice_2
    tuplu = []
    valoare = []
    lst_key = []
    lst_value = []

    #de facut separat pentru fiecare paranteza
    matrice_3 = matrice_2[0]

    if matrice_3[0] == "/" or matrice_3[0] == "*" or matrice_3[0] == "^^":
        if isinstance(matrice_3[1], list) and isinstance(matrice_3[2], list):
            primu = matrice_3[1]
            primu = rezolva_matrice(primu)


            lst_value_2 = primu

            m = len(lst_value_2)
            if m > 1:
                for j in reversed(range(m)):
                    if j == m - 1:
                        valoare = tuple(lst_value_2[j])
                        tuplu.append(valoare)
                    else:
                        lst = []
                        t = len(lst_value_2[j])
                        sir_4 = lst_value_2[j]
                        for k in range(0, t):
                            if isinstance(sir_4[k], list):
                                lst.append(tuple(valoare))
                            else:
                                lst.append(sir_4[k])
                        valoare = tuple(lst)
                        tuplu.append(valoare)
                tuplu = tuple(tuplu)
                lst_value_2 = []
                c = len(tuplu)
                for j in range(0, c):
                    valoare = tuplu[c - 1 - j]
                    lst_value_2.append(valoare)
            else:
                tuplu = primu[0]
                lst_value_2 = []
                c = len(tuplu)
                for j in range(0, c):
                    valoare = tuplu[j]
                    lst_value_2.append(valoare)


            print("@@@", lst_value_2)
            #print(calculam_lst_fara_paranteze(lst_value_2))
            ok = 0
            # verificam ca nu avem nici o lista
            c = len(primu)
            for j in range(0, c):
                if isinstance(primu[j], list):
                    ok = 1
            # aici intram daca avem doar un simplu semn
            if ok == 0:
                primu = calculam_lst_fara_paranteze(primu)
                if isinstance(primu, float):
                    ecuatie_finala.append(primu)
                else:
                    # facem ca operatorii sa fie de tip str si ii punem in ecuatia finala
                    value = str(primu[0])
                    # print("matrice@", type(value))
                    ecuatie_finala.append(value)
                    print("value= ", value)
            else:
                # aici intra daca in matrice_2 avem doar o lista in care calculam sin, cons, rad, log
                if len(primu) == 1:
                    primu = calculam_lst_fara_paranteze(primu)
                    # extragem float-ul din matrice_2
                    value = primu[0]
                    ecuatie_finala.append(value)
                else:
                    m = len(primu)
                    # deoarece intr-un dictionar nu putem avea lista ca si key vom folosi 2 liste
                    lst_key = []
                    lst_value = []

                    for j in reversed(range(m)):
                        # in lst_key vom avea valoarea expresiei
                        # calculam fiecare expresie pana cand vom avea un doar 1 numar
                        if j == m - 1:
                            termen = lst_value_2[j]
                            valoare = calculam_lst_fara_paranteze(primu[j])
                            # am luat floatul din lista
                            valoare = valoare[0]
                            # matrice_2[j] = valoare
                            primu[j] = list(lst_value_2[j])

                            lst = []
                            sir_parcurs = primu[j - 1]
                            for b in range(0, len(primu[j - 1])):
                                if isinstance(sir_parcurs[b], list):
                                    lst.append(primu[j])
                                else:
                                    lst.append(sir_parcurs[b])
                            primu[j - 1] = lst
                            # ramas aici
                            print("VALOARE = ", primu)
                            lst_key.append(valoare)
                            lst_value.append(termen)
                            print("lst_key=", lst_key)
                            print("lst_value=", lst_value)
                        else:
                            l = len(lst_value_2[j])
                            sir = lst_value_2[j]
                            for k in range(0, l):
                                # parcurgem lst_value ca sa inlocuim in relatia curenta cu cea calculata anterior
                                for t in range(0, len(lst_value)):
                                    if isinstance(sir[k], tuple):
                                        if lst_value[t] == sir[k]:
                                            # dam valoare din matrice_2
                                            sir = primu[j]

                                            sir[k] = str(lst_key[t])

                                            valoare = calculam_lst_fara_paranteze(sir)
                                            print("valoare= ", valoare)
                                            valoare = valoare[0]
                                            lst_key.append(valoare)
                                            lst_value.append(lst_value_2[j])
                                            print("lst_key =", lst_key)
                                            print("lst_value = ", lst_value)
                    m = len(lst_key)
                    # ultima valoarea din lst_key are valoarea de float a primei expresii din lst_value_2
                    ecuatie_finala.append(lst_key[m - 1])
                    primu = lst_key[len(lst_key) - 1]
                    print("primu =", primu)
                    matrice_3[1] = str(primu)
                    print("matrice_3 = ", matrice_3)
                    # de la rezolva matrice avem afisata in bucatele fiecare termen din ecuatie

                            #matrice_3 = rezolva_matrice(matrice_2[pozitie])
                            #print("matrice_3_2 = ", matrice_3)
                    lst_value_2 = matrice_2
                    tuplu = []
                    valoare = []
                    lst_key = []
                    lst_value = []


    tuplu = []
    lst = []
    #print(lst)
    #print(rezolva_matrice(matrice_2))
    print("@", matrice_2)
    #facem ca matrice_2 sa fie salvat in forma de tuplu in lst_value_2
    m = len(lst_value_2)
    if m > 1:
        for j in reversed(range(m)):
            if j == m - 1:
                valoare = tuple(lst_value_2[j])
                tuplu.append(valoare)
            else:
                lst = []
                t = len(lst_value_2[j])
                sir_4 = lst_value_2[j]
                for k in range(0, t):
                    if isinstance(sir_4[k], list):
                        lst.append(tuple(valoare))
                    else:
                        lst.append(sir_4[k])
                valoare = tuple(lst)
                tuplu.append(valoare)
        tuplu = tuple(tuplu)
        lst_value_2 = []
        c = len(tuplu)
        for j in range(0, c):
            valoare = tuplu[c - 1 - j]
            lst_value_2.append(valoare)
    else:
        tuplu = matrice_2
        lst_value_2 = []
        c = len(tuplu)
        for j in range(0, c):
            valoare = tuplu[j]
            lst_value_2.append(valoare)
    #lst_value_2 = tuple(lst_value_2)
    #avem in lst_2 forma de tuplu a lui matrice_2

    ok = 0
    #verificam ca nu avem nici o lista
    m = len(matrice_2)
    for j in range(0, m):
        if isinstance(matrice_2[j], list):
            ok = 1

    print("lst_value_2 = ", lst_value_2)
    #aici intram daca avem doar un simplu semn
    if ok == 0:
        matrice_2 = calculam_lst_fara_paranteze(matrice_2)
        if isinstance(matrice_2, float):
            ecuatie_finala.append(matrice_2)
        else:
            #facem ca operatorii sa fie de tip str si ii punem in ecuatia finala
            value = str(matrice_2[0])
            #print("matrice@", type(value))
            ecuatie_finala.append(value)
    else:
        #aici intra daca in matrice_2 avem doar o lista in care calculam sin, cons, rad, log
        if len(matrice_2) == 1:
            matrice_2 = calculam_lst_fara_paranteze(matrice_2)
            #extragem float-ul din matrice_2
            value = matrice_2[0]
            ecuatie_finala.append(value)
        else:
            m = len(matrice_2)
            # deoarece intr-un dictionar nu putem avea lista ca si key vom folosi 2 liste
            lst_key = []
            lst_value = []

            for j in reversed(range(m)):
            #in lst_key vom avea valoarea expresiei
            # calculam fiecare expresie pana cand vom avea un doar 1 numar
                if j == m - 1:
                    termen = lst_value_2[j]
                    valoare = calculam_lst_fara_paranteze(matrice_2[j])
                    #am luat floatul din lista
                    valoare = valoare[0]
                    #matrice_2[j] = valoare
                    matrice_2[j] = list(lst_value_2[j])

                    lst = []
                    sir_parcurs = matrice_2[j-1]
                    for b in range(0, len(matrice_2[j-1])):
                        if isinstance(sir_parcurs[b], list):
                            lst.append(matrice_2[j])
                        else:
                            lst.append(sir_parcurs[b])
                    matrice_2[j-1] = lst
                    #ramas aici
                    print("VALOARE = ", matrice_2)
                    lst_key.append(valoare)
                    lst_value.append(termen)
                    print("lst_key=", lst_key)
                    print("lst_value=", lst_value)
                else:
                    l = len(lst_value_2[j])
                    sir = lst_value_2[j]
                    for k in range(0, l):
                        #parcurgem lst_value ca sa inlocuim in relatia curenta cu cea calculata anterior
                        for t in range(0, len(lst_value)):
                            if isinstance(sir[k], tuple):
                                if lst_value[t] == sir[k]:
                                    #dam valoare din matrice_2
                                    sir = matrice_2[j]

                                    sir[k] = str(lst_key[t])

                                    valoare = calculam_lst_fara_paranteze(sir)
                                    print("valoare= ", valoare)
                                    valoare = valoare[0]
                                    lst_key.append(valoare)
                                    lst_value.append(lst_value_2[j])
                                    print("lst_key =", lst_key)
                                    print("lst_value = ", lst_value)
            m = len(lst_key)
            #ultima valoarea din lst_key are valoarea de float a primei expresii din lst_value_2
            ecuatie_finala.append(lst_key[m-1])


print("ecuatie_finala = ", ecuatie_finala)
ecuatie_finala = calculam_lst_fara_paranteze(ecuatie_finala)
print("rezultat ecuatie_finala = ", ecuatie_finala)

"""
# Am terminat de calculat_lst_fara_paranteze