# encoding: utf8

# YOUR NAME: José Mendes
# YOUR NUMBER: 107188

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT (names, numbers):
# - Filipe Obrist 107471
# - Bernardo Pinto 105926

from semantic_network import *
from constraintsearch import *


class MySN(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)
        # ADD CODE HERE IF NEEDED
        self.assoc_stats = {}
        self.rules = []

    def query_local(self, user=None, e1=None, rel=None, e2=None):
        # IMPLEMENT HERE
        self.query_result = [
            Declaration(
                key,
                Association(
                    tup[0], tup[1], ent if isinstance(entity2, set) else entity2
                ),
            )
            for key, value in self.declarations.items()
            if user is None or key == user
            for tup, entity2 in value.items()
            if e1 is None or tup[0] == e1
            if rel is None or tup[1] == rel
            for ent in (entity2 if isinstance(entity2, set) else [entity2])
            if e2 is None
            or ent == e2
            or entity2 == e2  # Checking both for sets and single values (lower case)
        ]
        return self.query_result  # Your code must leave the output in
        # self.query_result, which is returned here

    def query(self, entity, assoc=None):
        # IMPLEMENT HERE
        decl = self.query_local(e1=entity, rel=assoc)

        pred = [
            d.relation.entity2
            for d in (
                self.query_local(e1=entity, rel="subtype")
                + self.query_local(e1=entity, rel="member")
            )
        ]

        for p in pred:
            decl += self.query(p, assoc)

        self.query_result = [
            d
            for d in decl
            if d.relation.name != "subtype" and d.relation.name != "member"
        ]
        return self.query_result  # Your code must leave the output in
        # self.query_result, which is returned here

    def update_assoc_stats(self, assoc, user=None):
        # IMPLEMENT HERE
        # get all declarations where the relation is assoc and the user is user
        decl = self.query_local(user, rel=assoc)
        assoc_stats_entity1 = {}
        assoc_stats_entity2 = {}
        self.rules = []

        for d in decl:
            if d.relation.entity1[0].islower():
                self.rules.append(d)
                continue

            assoc_stats_entity1 = self.process_entity(
                user, d.relation.entity1, assoc_stats_entity1
            )
            assoc_stats_entity2 = self.process_entity(
                user, d.relation.entity2, assoc_stats_entity2
            )

        unknown_e1, unknown_e2, total_declarations = self.count_unknown_objects(decl)

        assoc_stats_entity1 = self.calculate_stats(
            assoc_stats_entity1, unknown_e1, total_declarations
        )
        assoc_stats_entity2 = self.calculate_stats(
            assoc_stats_entity2, unknown_e2, total_declarations
        )

        self.assoc_stats[(assoc, user)] = (assoc_stats_entity1, assoc_stats_entity2)
        return self.assoc_stats

    ## Auxiliary functions
    # Processes the entity and returns the number of times a certain association appears
    def process_entity(self, user, entity, assoc_stats):
        member_decl_entity = self.query_local(user=user, e1=entity, rel="member")
        for m in member_decl_entity:
            next_subtypes_entity = [m.relation.entity2]
            while next_subtypes_entity:
                subtype_decl_entity = self.query_local(
                    user=user, e1=next_subtypes_entity[0], rel="subtype"
                )
                next_subtypes_entity.extend(
                    [d.relation.entity2 for d in subtype_decl_entity]
                )
                if next_subtypes_entity[0] not in assoc_stats:
                    assoc_stats[next_subtypes_entity[0]] = 1
                else:
                    assoc_stats[next_subtypes_entity[0]] += 1
                next_subtypes_entity.pop(0)
        return assoc_stats

    # Counts the number of unknown objects for each entity (e1 and e2)
    def count_unknown_objects(self, decl):
        unknown_e1 = 0
        unknown_e2 = 0
        total_declarations = len(decl) - len(self.rules)
        for d in decl:
            if (
                self.query_local(e1=d.relation.entity1, rel="member") == []
                and self.query_local(e1=d.relation.entity1, rel="subtype") == []
            ):
                unknown_e1 += 1
            if (
                self.query_local(e1=d.relation.entity2, rel="member") == []
                and self.query_local(e1=d.relation.entity2, rel="subtype") == []
            ):
                unknown_e2 += 1
        return unknown_e1, unknown_e2, total_declarations

    # Calculates the association statistics using the formula given in the assignment
    def calculate_stats(self, assoc_stats_entity, unknown_objects, total_declarations):
        for key, value in assoc_stats_entity.items():
            unknown_objects_count = unknown_objects
            total_objects = (
                total_declarations
                - unknown_objects_count
                + (unknown_objects_count**0.5)
            )
            assoc_stats_entity[key] = min(value / total_objects, 1.0)
        return assoc_stats_entity


class MyCS(ConstraintSearch):
    def __init__(self, domains, constraints):
        ConstraintSearch.__init__(self, domains, constraints)
        # ADD CODE HERE IF NEEDED

    def search_all(self, domains=None, xpto=None):
        if domains is None:
            domains = self.domains

        # if any variable has an empty list of values, fail
        if any([lv == [] for lv in domains.values()]):
            return []

        # if no variable has more than one possible value, success
        if all([len(lv) == 1 for lv in list(domains.values())]):
            # if values violate constraints, fail
            for var1, var2 in self.constraints:
                constraint = self.constraints[var1, var2]
                if not constraint(var1, domains[var1][0], var2, domains[var2][0]):
                    return []
            return [{v: lv[0] for (v, lv) in domains.items()}]

        # continuation of the search
        for var in domains.keys():
            if len(domains[var]) > 1:
                solutions = []
                for val in domains[var]:
                    new_domains = dict(domains)
                    new_domains[var] = [val]
                    # constraint propagation
                    new_domains = self.propagate(new_domains, var, val)
                    if new_domains is None:
                        continue

                    sub_solutions = self.search_all(new_domains)
                    solutions.extend(sub_solutions)

                return solutions
        return []

    ## Auxiliary function
    # propagate constraints
    def propagate(self, domains, var, value):
        for v, domain in domains.items():
            if v == var:
                continue
            if (v, var) in self.constraints:
                constraint = self.constraints[v, var]
                new_domain = [val for val in domain if constraint(v, val, var, value)]

                if new_domain == []:
                    return None

                domains[v] = new_domain

        return domains
