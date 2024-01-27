from constraintsearch import *

"""
André, Bernardo e Cláudio dão um passeio de bicicleta. Cada um anda na
bicicleta de um dos amigos e leva o chapéu de um dos outros. O que leva o
chapéu de Cláudio anda na bicicleta de Bernardo. Que bicicleta e que chapéu
levam cada um dos amigos? (Retirado de Pierre Berloquin. 100 Jogos Lógicos.
Gradiva, 1990.)
"""

amigos = ["Andre", "Bernardo", "Claudio"]


def constraint(a1, i1, a2, i2):
    bike1, chapeu1 = i1
    bike2, chapeu2 = i2

    if a1 in i1 or a2 in i2:  # nao posso levar as minhas coisas
        return False

    if bike1 == chapeu1 or bike2 == chapeu2:  # nao posso levar as coisas do mesmo amigo
        return False

    if chapeu1 == "Claudio" and bike1 != "Bernardo":
        return False

    if chapeu2 == "Claudio" and bike2 != "Bernardo":
        return False

    return True


def make_constraint_graph(amigos):
    return {(X, Y): constraint for X in amigos for Y in amigos if X != Y}


def make_domain(amigos):
    return {
        amigo: [(bike, chapeu) for bike in amigos for chapeu in amigos]
        for amigo in amigos
    }


cs = ConstraintSearch(make_domain(amigos), make_constraint_graph(amigos))

print(cs.search())
