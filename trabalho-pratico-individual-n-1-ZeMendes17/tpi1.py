# STUDENT NAME: José Pedro Santos Mendes
# STUDENT NUMBER: 107188

# DISCUSSED TPI-1 WITH: (names and numbers):
# Filipe Obrist 107471
# Bernardo Pinto 105926
# João Santos 110555


import math
from tree_search import *


class OrderDelivery(SearchDomain):
    def __init__(self, connections, coordinates):
        self.connections = connections
        self.coordinates = coordinates
        # ANY NEEDED CODE CAN BE ADDED HERE
        self.initial_city = None
        self.visited = []
        self.visited.append(self.initial_city)
        self.goal_cities_found = []
        self.goal_cities_found_count = 0
        self.method = None
        # used because if the method is depth, a lot of loops will occur
        # like this we are able to check if the city was already visited
        # thus avoiding the loops, but if we track the visited cities and the method is not depth
        # the algorithm will not work properly brecause we will run out of cities to visit

    def actions(self, state):
        city = state[0]
        actlist = []
        for C1, C2, D in self.connections:
            if C1 == city:
                actlist += [(C1, C2)]
            elif C2 == city:
                actlist += [(C2, C1)]
        return actlist

    def result(self, state, action):
        # IMPLEMENT HERE
        city = state[0]
        self.visited.append(city)
        C1, C2 = action
        if C1 == city:
            if self.method == "depth" and C2 in self.visited:
                return state
            return (C2, state[1] + [C1])
        elif C2 == city:
            if self.method == "depth" and C1 in self.visited:
                return state
            return (C1, state[1] + [C2])

    def satisfies(self, state, goal):
        # IMPLEMENT HERE
        if (
            self.method == "depth"
            and state[0] in goal
            and state[0] not in self.goal_cities_found
        ):
            self.goal_cities_found.append(state[0])
            self.goal_cities_found_count += 1
            self.visited = []

        if self.initial_city == state[0] and all(
            goal_city in state[1] for goal_city in goal
        ):
            self.goal_cities_found = []
            self.goal_cities_found_count = 0
            self.visited = []
            return True
        return False

    def cost(self, state, action):
        # IMPLEMENT HERE
        city = state[0]
        C1, C2 = action
        if C1 == city:
            for x1, x2, d in self.connections:
                if (x1, x2) == action or (x2, x1) == action:
                    return d

    def heuristic(self, state, goal):
        # IMPLEMENT HERE
        distance = 0
        for city in goal:
            if city not in state[1]:
                c1_x, c1_y = self.coordinates[state[0]]
                c2_x, c2_y = self.coordinates[city]
                distance += round(math.hypot(c1_x - c2_x, c1_y - c2_y))
        if distance == 0:
            c1_x, c1_y = self.coordinates[state[0]]
            c2_x, c2_y = self.coordinates[self.initial_city]
            distance += round(math.hypot(c1_x - c2_x, c1_y - c2_y))
        return distance


class MyNode(SearchNode):
    def __init__(self, state, parent, depth=0, cost=0, heuristic=None, eval=None):
        super().__init__(state, parent)
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.eval = eval
        self.deletion = False


class MyTree(SearchTree):
    def __init__(self, problem, strategy="breadth", maxsize=None):
        self.problem = problem
        root = MyNode(state=problem.initial, parent=None)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.non_terminals = 0
        self.maxsize = maxsize

    def astar_add_to_open(self, lnewnodes):
        # IMPLEMENT HERE
        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key=lambda x: (x.eval, x.state))

    def search2(self):
        # IMPLEMENT HERE
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes) + 1
                return self.get_path(node)
            self.non_terminals += 1
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state, a)
                if newstate not in self.get_path(node):
                    newnode = MyNode(
                        newstate,
                        node,
                        node.depth + 1,
                        node.cost + self.problem.domain.cost(node.state, a),
                        self.problem.domain.heuristic(newstate, self.problem.goal),
                    )
                    newnode.eval = newnode.cost + newnode.heuristic
                    lnewnodes.append(newnode)
                    if (
                        self.strategy == "A*"
                        and self.maxsize != None
                        and (
                            (len(self.open_nodes) + 1 + self.non_terminals)
                            > self.maxsize
                        )
                    ):
                        self.manage_memory()
            self.add_to_open(lnewnodes)
        return None

    def manage_memory(self):
        # IMPLEMENT HERE
        while (len(self.open_nodes) + 1 + self.non_terminals) > self.maxsize:
            # first we sort the list of nodes by eval, if the eval is the same, we sort alphabetically
            self.open_nodes.sort(key=lambda x: (x.eval, x.state))
            # then mark for deletion the nodes with the highest eval

            for i in range(len(self.open_nodes) - 1, -1, -1):
                if not self.open_nodes[i].deletion:
                    self.open_nodes[i].deletion = True
                    node_to_delete = self.open_nodes[i]
                    break

            if node_to_delete.parent == None or node_to_delete == None:
                continue

            # get all the node's siblings
            siblings = [
                node for node in self.open_nodes if node.parent == node_to_delete.parent
            ]

            if all(node.deletion for node in siblings):
                for sibling in siblings:
                    self.open_nodes.remove(sibling)
                node_to_delete.parent.eval = min(node.eval for node in siblings)
                self.non_terminals -= 1

            self.open_nodes.sort(key=lambda x: (x.eval, x.state))

    # if needed, auxiliary methods can be added here


def orderdelivery_search(domain, city, targetcities, strategy="breadth", maxsize=None):
    # IMPLEMENT HERE
    domain.initial_city = city
    domain.method = strategy
    p = SearchProblem(domain, (city, []), targetcities)
    t = MyTree(p, strategy, maxsize)
    path = t.search2()
    path = path[-1][1] + [
        path[-1][0]
    ]  # only used this line to get the path in the correct format as in the results file
    # adding the corrent city to the end of the path and displaying like a list
    return (t, path)


# If needed, auxiliary functions can be added here
