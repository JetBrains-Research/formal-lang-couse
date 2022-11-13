import pytest
from pyformlang.cfg import CFG, Variable

from project.hellings import cfpq_by_hellings, hellings
from tests.utils import get_data, dot_to_graph
import networkx as nx


@pytest.mark.parametrize(
    "graph, query, start_nodes, final_nodes, start_var, expected",
    get_data(
        "test_cfpq",
        lambda d: (
            dot_to_graph(d["graph"]),
            d["query"],
            d["start_nodes"],
            d["final_nodes"],
            d["start_var"] if d["start_var"] is not None else "S",
            {tuple(pair) for pair in d["expected"]},
        ),
    ),
)
def test_cfpq(
    graph: nx.Graph,
    query: str,
    start_nodes: set | None,
    final_nodes: set | None,
    start_var: str,
    expected: set[tuple],
):
    actual = cfpq_by_hellings(graph, query, start_nodes, final_nodes, start_var)

    assert actual == expected


@pytest.mark.parametrize(
    "graph, cfg, expected",
    get_data(
        "test_constrained_transitive_closure",
        lambda d: (
            dot_to_graph(d["graph"]),
            CFG.from_text(d["cfg"]),
            {
                (triple["from"], Variable(triple["var"]), triple["to"])
                for triple in d["expected"]
            },
        ),
    ),
)
def test_constrained_transitive_closure(
    graph: nx.Graph, cfg: CFG, expected: set[tuple]
):
    actual = hellings(graph, cfg)

    assert actual == expected
