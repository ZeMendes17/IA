# Guiao de representacao do conhecimento
# -- Redes semanticas
#
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#


from collections import Counter
from functools import reduce
from statistics import mean


class Relation:
    def __init__(self, e1, rel, e2):
        self.entity1 = e1
        #       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2

    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + str(self.entity2) + ")"

    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self, e1, assoc, e2):
        Relation.__init__(self, e1, assoc, e2)


#   Exemplo:
#   a = Association('socrates','professor','filosofia')

class AssocOne(Association):
    def __init__(self, e1, assoc, e2):
        Association.__init__(self, e1, assoc, e2)

class AssocNum(Association):
    def __init__(self, e1, assoc, e2):
        Association.__init__(self, e1, assoc, e2)


# Subclasse Subtype
class Subtype(Relation):
    def __init__(self, sub, super):
        Relation.__init__(self, sub, "subtype", super)


#   Exemplo:
#   s = Subtype('homem','mamifero')


# Subclasse Member
class Member(Relation):
    def __init__(self, obj, type):
        Relation.__init__(self, obj, "member", type)


#   Exemplo:
#   m = Member('socrates','homem')


# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self, user, rel):
        self.user = user
        self.relation = rel

    def __str__(self):
        return "decl(" + str(self.user) + "," + str(self.relation) + ")"

    def __repr__(self):
        return str(self)


#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)


# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self, ldecl=None):
        self.declarations = [] if ldecl == None else ldecl

    def __str__(self):
        return str(self.declarations)

    def insert(self, decl):
        self.declarations.append(decl)

    def query_local(self, user=None, e1=None, rel_type=None, rel=None, e2=None):
        self.query_result = [
            d
            for d in self.declarations
            if (user == None or d.user == user)
            and (e1 == None or d.relation.entity1 == e1)
            and (rel_type == None or isinstance(d.relation, rel_type))
            and (rel == None or d.relation.name == rel)
            and (e2 == None or d.relation.entity2 == e2)
        ]
        return self.query_result

    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    ## ex1
    def list_associations(self):
        d = self.query_local(
            rel_type=Association
        )  # dá nos todas as declarações que têm associações
        return list(set([decl.relation.name for decl in d]))  # nome das associações

    ## ex2
    def list_objects(self):
        d = self.query_local(rel_type=Member)  # é a relação que pertença... ta em cima
        return list(set([decl.relation.entity1 for decl in d]))  # nome dos objetos

    ## ex3
    def list_users(self):
        d = self.query_local()
        return list(set([decl.user for decl in d]))  # nome dos users

    ## ex4
    def list_types(self):  # tipos existentes na rede. O subtype tem duas entidades
        # vamos ao subtype buscar as duas entidades
        # além disso no member temos a entidade 2 que é um tipo
        d1 = self.query_local(
            rel_type=Subtype
        )  # vai buscar as declarações que são subtypes
        d2 = self.query_local(
            rel_type=Member
        )  # vai buscar as declarações que são members

        return list(
            set(
                [decl.relation.entity1 for decl in d1]
                + [decl.relation.entity2 for decl in d1 + d2]
            )
        )

    ## ex5
    def list_local_associations(
        self, entity
    ):  # vai buscar todas as associações que têm a entidade
        # seja na entidade 1 ou na entidade 2 (de um lado ou de outro)
        d1 = self.query_local(e1=entity, rel_type=Association)
        d2 = self.query_local(e2=entity, rel_type=Association)

        # vai buscar os nomes somando as duas listas
        return list(set([decl.relation.name for decl in d1 + d2]))

    ## ex6
    def list_relations_by_user(self, user): # vai buscar as relações que o user declarou
        d = self.query_local(user=user)
        return list(set([decl.relation.name for decl in d]))
    
    ## ex7
    def associations_by_user(self, user):
        d = self.query_local(user=user, rel_type=Association)
        return len(list(set([decl.relation.name for decl in d]))) 
        # isto vai fazer uma lista com valores únicos devido ao set e
        # depois vai ver a length para ver as associações que este user fez

    ## ex8
    def list_local_associations_by_entity(self, entity):
        d1 = self.query_local(e1=entity, rel_type=Association)
        d2 = self.query_local(e2=entity, rel_type=Association)

        return list(set([(decl.relation.name, decl.user) for decl in d1 + d2]))
    
    ## ex9
    def predecessor(self, entity1, entity2):
        # retorna True se entity1 é predecessor de entity2
        # e False caso contrário
        d = self.query_local(e1=entity2, rel_type=(Subtype, Member))
        
        if d == []: # condição de paragem
            return False
        
        if entity1 in [decl.relation.entity2 for decl in d]: # condição de sucesso
            return True
        
        return any([self.predecessor(entity1, decl.relation.entity2) for decl in d])
    
    ## ex10
    def predecessor_path(self, a, b):
        d = self.query_local(e1=b, rel_type=(Subtype, Member))

        if d == []:
            return None
        
        if a in [decl.relation.entity2 for decl in d]:
            return [a, b]
        
        for pred in [decl.relation.entity2 for decl in d]:
            if res:= self.predecessor_path(a, pred):
                return res + [b]
            
        return None
    
    ## ex11
    def query(self, entity, rel=None):
        decl = self.query_local(e1=entity, rel=rel, rel_type=Association)

        pred = [d.relation.entity2 for d in self.query_local(e1=entity, rel_type=(Member, Subtype))]

        for p in pred:
            decl += self.query(p, rel=rel)

        return decl
    
    def query2(self, entity, rel=None):
        decl = self.query_local(e1=entity, rel_type=(Member, Subtype))

        return decl + self.query(entity, rel)
    
    # ex12
    def query_cancel(self, entity, rel=None):
        decl = self.query_local(e1=entity, rel=rel, rel_type=Association)

        pred = [d.relation.entity2 for d in self.query_local(e1=entity, rel_type=(Member, Subtype))]

        decl_name = [d.relation.name for d in decl]

        for p in pred:
            decl += [d for d in self.query_cancel(p, rel) if d.relation.name not in decl_name]

        return decl
    
    # ex13
    def query_down(self, entity, rel, first=True):
        decl = ([] if first else self.query_local(e1=entity, rel=rel, rel_type=Association))

        desc = [d.relation.entity1 for d in self.query_local(e2=entity, rel_type=(Member, Subtype))]

        for d in desc:
            decl += [d for d in self.query_down(d, rel, False)]

        return decl
    
    # ex14
    def query_induce(self, entity, rel):
        decl = self.query_down(entity, rel)

        return Counter([d.relation.entity2 for d in decl]).most_common(1)[0][0]
    
    # ex15
    def query_local_assoc(self, entity, rel):
        decl = self.query_local(e1=entity, rel=rel)

        for d in decl:
            if isinstance(d.relation, AssocOne):
                val, count = Counter([d.relation.entity2 for d in decl]).most_common(1)[0]

                return val, count/len(decl)
            
            elif isinstance(d.relation, AssocNum):
                return mean([d.relation.entity2 for d in decl])
            
            elif isinstance(d.relation, Association):
                l = Counter([d.relation.entity2 for d in decl]).most_common()

# com reduce()
                r = [(val, count/len(decl)) for val, count in l]

                def aux(carry, elem):
                    l, lim = carry
                    v, f = elem

                    return (l+[elem], lim+f) if lim < 0.75 else l
                    

                return reduce(aux, r, ([], 0))
# com for
                # also correct
                # lim = 0
                # res = []
                # for v, f in r:
                #     lim += f
                #     res.append((v, f))
                #     if lim >= 0.75:
                #         return res

                # return r

    # ex16
    def query_assoc_value(self, E, A):
        local = self.query_local(e1=E, rel=A)

        l_c = Counter([d.relation.entity2 for d in local]).most_common()

        if len(l_c) == 1:
            return l_c[0][0]
        
        herdados = self.query(entity=E, rel=A)

        h_c = Counter([d.relation.entity2 for d in herdados]).most_common()

        return h_c[0][0]
    