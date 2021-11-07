from typing import Set, Tuple

import networkx as nx
from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import Regex

from project.automaton_tools import get_min_dfa_from_regex, get_nfa_from_graph
from project.grammar_tools import hellings
from project.matrix_tools import BooleanAdjacencies

__all__ = [
    "regular_path_querying",
    "regular_str_path_querying",
    "context_free_path_querying",
]


def regular_str_path_querying(
    graph: nx.MultiDiGraph,
    query_str: str,
    start_node_nums: Set[int] = None,
    final_node_nums: Set[int] = None,
) -> Set[Tuple[int, int]]:
    """
    Using the specified graph and a regular string query,
    finds all pairs of reachable node numbers.

    If start_nodes or final_nodes are not specified,
    all nodes are considered start or final respectively.

    Parameters
    ----------
    graph: nx.MultiDiGraph
        Graph for queries
    query_str: str
        Query to graph as a string
    start_node_nums: Set[int], default = None
        Set of start node numbers to configure Nondeterministic Finite Automaton,
        which must exist in the graph
    final_node_nums: Set[int], default = None
        Set of final node numbers to configure Nondeterministic Finite Automaton,
        which must exist in the graph

    Returns
    -------
    Set[Tuple[int, int]]
        Set of all pairs of reachable node numbers

    Raises
    ------
    ValueError
        If non-existent in the specified graph node number is used
    MisformedRegexError
        If specified regex_str has an irregular format
    """

    return regular_path_querying(
        graph, Regex(query_str), start_node_nums, final_node_nums
    )


def regular_path_querying(
    graph: nx.MultiDiGraph,
    query_regex: Regex,
    start_node_nums: Set[int] = None,
    final_node_nums: Set[int] = None,
) -> Set[Tuple[int, int]]:
    """
    Using the specified graph and a regular expression query,
    finds all pairs of reachable node numbers.

    If start_nodes or final_nodes are not specified,
    all nodes are considered start or final respectively.

    Parameters
    ----------
    graph: nx.MultiDiGraph
        Graph for queries
    query_regex: Regex
        Query to graph as complete Regex
    start_node_nums: Set[int], default = None
        Set of start node numbers to configure Nondeterministic Finite Automaton,
        which must exist in the graph
    final_node_nums: Set[int], default = None
        Set of final node numbers to configure Nondeterministic Finite Automaton,
        which must exist in the graph

    Returns
    -------
    Set[Tuple[int, int]]
        Set of all pairs of reachable node numbers

    Raises
    ------
    ValueError
        If non-existent in the specified graph node number is used
    """

    graph = BooleanAdjacencies(
        get_nfa_from_graph(graph, start_node_nums, final_node_nums)
    )

    query = BooleanAdjacencies(get_min_dfa_from_regex(query_regex))

    intersection = graph.intersect(query)
    transitive_closure = intersection.get_transitive_closure()

    reachable_state_nums = set()

    for state_from_num, state_to_num in zip(*transitive_closure.nonzero()):
        state_from = intersection.nums_states[state_from_num]
        state_to = intersection.nums_states[state_to_num]

        if (
            state_from in intersection.start_states
            and state_to in intersection.final_states
        ):
            reachable_state_from_num = state_from_num // query.states_num
            reachable_state_to_num = state_to_num // query.states_num

            reachable_state_nums.add((reachable_state_from_num, reachable_state_to_num))

    return reachable_state_nums


def context_free_path_querying(
    cfg: CFG,
    graph: nx.MultiDiGraph,
    start_symbol: str = Variable("S"),
    start_node_nums: Set[int] = None,
    final_node_nums: Set[int] = None,
) -> Set[Tuple[int, int]]:
    cfg._start_symbol = start_symbol

    reachable_node_nums = {
        (node_num_l, node_num_r)
        for node_num_l, head, node_num_r in hellings(cfg, graph)
        if head == cfg.start_symbol
    }

    if start_node_nums:
        reachable_node_nums = {
            (node_num_l, node_num_r)
            for node_num_l, node_num_r in reachable_node_nums
            if node_num_l in start_node_nums
        }

    if start_node_nums:
        reachable_node_nums = {
            (node_num_l, node_num_r)
            for node_num_l, node_num_r in reachable_node_nums
            if node_num_r in final_node_nums
        }

    return reachable_node_nums
