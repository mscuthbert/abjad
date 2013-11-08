# -*- encoding: utf-8 -*-
from abjad.tools import spannertools
from abjad.tools.topleveltools import iterate


def iterate_nontrivial_tie_chains_in_expr(expr, reverse=False):
    r'''Iterate nontrivial tie chains forward in `expr`:

    ::

        >>> staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'4 ~
            \times 2/3 {
                c'16
                d'8
            }
            e'8
            f'4 ~
            f'16
        }

    ::

        >>> for x in \
        ...     iterationtools.iterate_nontrivial_tie_chains_in_expr(staff):
        ...     x
        ...
        TieChain(Note("c'4"), Note("c'16"))
        TieChain(Note("f'4"), Note("f'16"))

    Iterate nontrivial tie chains backward in `expr`:

    ::

        >>> for x in \
        ...     iterationtools.iterate_nontrivial_tie_chains_in_expr(
        ...     staff, reverse=True):
        ...     x
        ...
        TieChain(Note("f'4"), Note("f'16"))
        TieChain(Note("c'4"), Note("c'16"))

    Returns generator.
    '''
    from abjad.tools import scoretools
    spanner_classes = (spannertools.TieSpanner, )
    if not reverse:
        for leaf in iterate(expr).by_class(scoretools.Leaf):
            tie_spanners = leaf._get_spanners(spanner_classes)
            if not tie_spanners or \
                tuple(tie_spanners)[0]._is_my_last_leaf(leaf):
                tie_chain = leaf._get_tie_chain()
                if not tie_chain.is_trivial:
                    yield tie_chain
    else:
        for leaf in iterate(expr).by_class(scoretools.Leaf, reverse=True):
            tie_spanners = leaf._get_spanners(spanner_classes)
            if not(tie_spanners) or \
                tuple(tie_spanners)[0]._is_my_first_leaf(leaf):
                tie_chain = leaf._get_tie_chain()
                if not tie_chain.is_trivial:
                    yield tie_chain