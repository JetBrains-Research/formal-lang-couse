import pytest
from pyformlang.cfg import CFG

from project.context_free_path_query import context_free_path_query
from tests.test_utils import create_graph

testdata = [
    (
        context_free_path_query(
            cfg=CFG.from_text(
                """
                S -> A B
                A -> a
                B -> b
            """
            ),
            graph=create_graph(nodes=[0, 1, 2], edges=[(0, "a", 1), (1, "b", 2)]),
        ),
        {(0, 2)},
    ),
    (
        context_free_path_query(
            cfg=CFG.from_text(
                """
                S -> $
            """
            ),
            graph=create_graph(nodes=[0, 1], edges=[(0, "a", 1), (1, "b", 0)]),
        ),
        {(0, 0), (1, 1)},
    ),
    (
        context_free_path_query(
            cfg=CFG.from_text(
                """
                S -> A B C
                A -> a
                B -> b
                C -> c
            """
            ),
            graph=create_graph(
                nodes=[0, 1, 2, 3], edges=[(0, "a", 1), (1, "b", 2), (2, "c", 3)]
            ),
        ),
        {(0, 3)},
    ),
    (
        context_free_path_query(
            cfg=CFG.from_text(
                """
                S -> A B C | S S | s
                A -> a
                B -> b
                C -> c
            """
            ),
            graph=create_graph(
                nodes=[0, 1, 2, 3],
                edges=[(0, "s", 0), (0, "a", 1), (1, "b", 2), (2, "c", 3)],
            ),
        ),
        {(0, 3), (0, 0)},
    ),
    (
        context_free_path_query(
            cfg=CFG.from_text(
                """
                S -> A B | S S
                A -> a | $
                B -> b
            """
            ),
            graph=create_graph(
                nodes=[0, 1, 2, 3, 4],
                edges=[(0, "a", 1), (1, "b", 2), (2, "a", 3), (3, "b", 4)],
            ),
        ),
        {(0, 4), (2, 4), (1, 2), (3, 4), (1, 4), (0, 2)},
    ),
]


@pytest.mark.parametrize("actual,expected", testdata)
def test_context_free_path_query(
    actual: set[tuple[any, any]], expected: set[tuple[any, any]]
):
    assert actual == expected
