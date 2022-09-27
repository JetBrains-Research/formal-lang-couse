from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex

from project.automata_utils import (
    from_regex_to_dfa,
    boolean_decompose_enfa,
    intersect_enfa,
)
from project.graph_utils import from_graph_to_nfa

__all__ = ["regular_path_query"]


def regular_path_query(
    regex: Regex,
    graph: MultiDiGraph,
    start_states: list[any] = None,
    final_states: list[any] = None,
) -> set[tuple[any, any]]:
    """
    Performs rpq (regular path query) in graph with regex
    :param regex: regex to define regular path query
    :param graph: graph to be inspected
    :param start_states: start nodes to rpq inside graph
    :param final_states: final nodes to rpq inside graph
    :return: 2 element tuples with nodes satisfying rpq
    """
    if start_states is None:
        start_states = list(graph.nodes)

    if final_states is None:
        final_states = list(graph.nodes)

    graph_as_enfa = from_graph_to_nfa(graph, start_states, final_states)
    regex_as_enfa = from_regex_to_dfa(regex)
    intersection_enfa = intersect_enfa(graph_as_enfa, regex_as_enfa)

    boolean_decompose_intersection = boolean_decompose_enfa(intersection_enfa)
    intersection_states = boolean_decompose_intersection.states()
    transitive_closure_of_intersection = (
        boolean_decompose_intersection.transitive_closure()
    )
    transitive_closure_connected_states = zip(
        *transitive_closure_of_intersection.nonzero()
    )
    results = set()
    for (i, j) in transitive_closure_connected_states:
        (graph_start_state, regex_start_state) = intersection_states[i].value
        (graph_final_state, regex_final_state) = intersection_states[j].value
        if (
            graph_start_state in start_states
            and graph_final_state in final_states
            and regex_start_state in regex_as_enfa.start_states
            and regex_final_state in regex_as_enfa.final_states
        ):
            results.add((graph_start_state, graph_final_state))

    return results
