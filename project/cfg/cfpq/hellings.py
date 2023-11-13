import queue

from networkx import MultiDiGraph
from pyformlang.cfg import CFG

from project.cfg.transformers import transform_to_wcnf


def cfpq(cfg: CFG, graph: MultiDiGraph):
    wcnf = transform_to_wcnf(cfg)

    q = set()
    terminal_productions = dict()
    variable_productions = dict()

    for production in wcnf.productions:
        if not production.body:
            for node in graph.nodes:
                q.add((node, production.head, node))
        elif len(production.body) == 1:
            term = production.body[0]
            if term not in terminal_productions:
                terminal_productions[term.value] = []
            terminal_productions[term.value].append(production.head)
        else:
            var1, var2 = production.body
            if (var1, var2) not in variable_productions:
                variable_productions[var1, var2] = []
            variable_productions[var1, var2].append(production.head)

    for edge in graph.edges(data=True):
        term = edge[2]["label"]

        if term in terminal_productions:
            for var in terminal_productions[term]:
                q.add((edge[0], var, edge[1]))

    result = q.copy()
    while q:
        node1, cur_var, node2 = q.pop()

        next_result = set()
        for fst, var, snd in result:
            if snd == node1 and (var, cur_var) in variable_productions:
                for production_var in variable_productions[var, cur_var]:
                    transition = (fst, production_var, node2)
                    if transition not in result:
                        q.add(transition)
                        next_result.add(transition)
            if fst == node2 and (cur_var, var) in variable_productions:
                for production_var in variable_productions[cur_var, var]:
                    transition = (node1, production_var, snd)
                    if transition not in result:
                        q.add(transition)
                        next_result.add(transition)

        result = result.union(next_result)

    return result
