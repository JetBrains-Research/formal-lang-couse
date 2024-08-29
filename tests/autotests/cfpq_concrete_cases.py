from typing import Callable
from pyformlang.cfg import CFG
from copy import copy
from graphs import *
from pyformlang.rsa import RecursiveAutomaton


class TestCaseCFPQ:
    """
    class that contains all information about test case
    """

    def __init__(self, graph: MultiDiGraph, query: CFG, actual_answer: set[tuple[int, int]],
                 start_nodes: set[int] = None, final_nodes: set[int] = None):
        self.graph = copy(graph)
        self.query = copy(query)
        self.expected_answer = copy(actual_answer)
        self.start_nodes = copy(start_nodes) if start_nodes else graph.nodes
        self.final_nodes = copy(final_nodes) if final_nodes else graph.nodes

    def check_answer_cfg(self, function: Callable[
        [CFG, MultiDiGraph, set[int], set[int]],
        set[tuple[int, int]],
    ]):
        """
        assertion function to algorithms with cfg
        :param function: testing function (*hellings_based_cfpq* or *matrix_based_cfpq*)
        :return: assertion
        """
        actual_res = function(self.query, self.graph, self.start_nodes, self.final_nodes)
        assert actual_res == self.expected_answer

    def check_answer_rsm(self, function: Callable[
        [RecursiveAutomaton, MultiDiGraph, set[int], set[int]], set[tuple[int, int]]
    ], cfg_to_rsm: Callable[[CFG], RecursiveAutomaton]):
        """
        assertion function to algorithms with rsm
        :param function: testing function (*tensor_based_cfpq* or *gll_based_cfpq*)
        :param cfg_to_rsm: function that convert CFG to RecursiveAutomaton
        :return: assertion
        """
        actual_res = function(cfg_to_rsm(self.query), self.graph, self.start_nodes, self.final_nodes)
        assert actual_res == self.expected_answer

    def __str__(self):
        return f"expected result: {self.expected_answer}\n" + \
            f"query: {self.query.to_text()}" + \
            f"graph: {self.graph.edges(data=True)}"


CASES_CFPQ = [
    TestCaseCFPQ(
        point_graph,
        CFG.from_text("S -> a"),
        set()
    ),
    TestCaseCFPQ(
        point_graph,
        CFG.from_text("S -> S a | $"),
        {(1, 1)}
    ),
    TestCaseCFPQ(
        set_of_vertices_without_edges,
        CFG.from_text("S -> S a | $"),
        {(0, 0), (2, 2), (1, 1)}
    ),
    TestCaseCFPQ(
        b_graph,
        CFG.from_text("S -> a"),
        set()
    ),
    TestCaseCFPQ(
        b_graph,
        CFG.from_text("S -> b"),
        {(0, 1)}
    ),
    TestCaseCFPQ(
        b_graph,
        CFG.from_text("S -> S b | $"),
        {(0, 1), (0, 0), (1, 1)}
    ),
    TestCaseCFPQ(
        bbb_graph,
        CFG.from_text("S -> S b b | $"),
        {(0, 1), (0, 0), (0, 2), (1, 1), (1, 2), (1, 0), (2, 2), (2, 1), (2, 0)}
    ),
    TestCaseCFPQ(
        bab_graph,
        CFG.from_text("S -> S a | S b | $"),
        {(0, 1), (0, 0), (0, 2), (1, 1), (1, 2), (1, 0), (2, 2), (2, 1), (2, 0)}
    ),
    TestCaseCFPQ(
        baa_graph,
        CFG.from_text("S -> a S b | $"),
        {(0, 0), (1, 1), (1, 0)}
    ),
    TestCaseCFPQ(
        baa_graph,
        CFG.from_text("S -> a S b | a b"),
        {(0, 0), (1, 0)}
    ),
    TestCaseCFPQ(
        set_of_vertices_without_edges,
        CFG.from_text("S -> $"),
        {(0, 0), (2, 2), (1, 1)}
    ),
    TestCaseCFPQ(
        aaa_graph,
        CFG.from_text("S -> a | S S"),
        {(0, 1), (0, 0), (0, 2), (1, 1), (1, 2), (1, 0), (2, 2), (2, 1), (2, 0)}
    )
]