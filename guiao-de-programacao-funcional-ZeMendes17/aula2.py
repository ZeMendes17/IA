import math

#Exercicio 4.1
impar = lambda x: x % 2 != 0

#Exercicio 4.2
positivo = lambda x: x > 0

#Exercicio 4.3
comparar_modulo = lambda x, y: abs(x) < abs(y)

#Exercicio 4.4
cart2pol = lambda x, y: (math.hypot(x,y), math.atan2(y,x))

#Exercicio 4.5
ex5 = lambda f, g, h: lambda x, y, z: h(f(x, y), g(y, z))

#Exercicio 4.6
def quantificador_universal(lista, f):
    # f é uma função booleana unária

    ## also works
    # if lista == []:
    #     return True
    # if not f(lista[0]):
    #     return False
    # return quantificador_universal(lista[1:], f)

    return [e for e in lista if not f(e)] == []

#Exercicio 4.8
def subconjunto(lista1, lista2):
    ## also works
    # if lista1 == []:
    #     return True
    # if lista1[0] not in lista2:
    #     return False
    # return subconjunto(lista1[1:], lista2)

    ## also works
    # return [e for e in lista1 if e not in lista2] == []

    return quantificador_universal(lista1, lambda x: x in lista2)

#Exercicio 4.9
def menor_ordem(lista, f):
    # f é função booleana binária para comparação elemento a elemento

    ## also works
    # if lista == []:
    #     return None
    # if len(lista) == 1:
    #     return lista[0]
    # if f(lista[0], menor_ordem(lista[1:], f)):
    #     return lista[0]
    # return menor_ordem(lista[1:], f)

    if lista == []:
        return None
    elif len(lista) == 1:
        return lista[0]
    
    m = menor_ordem(lista[1:], f)
    return lista[0] if f(lista[0], m) else m

#Exercicio 4.10
def menor_e_resto_ordem(lista, f):
    # f é como em menor_ordem
    
    ## also works
    # if len(lista) == 1:
    #     return lista[0], []
    # menor, resto = menor_e_resto_ordem(lista[1:], f)
    # if f(lista[0], menor):
    #     return lista[0], resto + [menor]
    # return menor, [lista[0]] + resto

    if lista == []:
        return None, []
    if len(lista) == 1:
        return lista[0], []
    
    m, r = menor_e_resto_ordem(lista[1:], f)
    return (lista[0], r + [m]) if f(lista[0], m) else (m, [lista[0]] + r)

#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    # ordem é uma função de ordenação
    if lista == []:
        return []
    menor, resto = menor_e_resto_ordem(lista, ordem)
    return [menor] + ordenar_seleccao(resto, ordem)

