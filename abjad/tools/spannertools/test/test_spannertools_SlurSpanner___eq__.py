# -*- encoding: utf-8 -*-
from abjad import *


def test_SlurSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = SlurSpanner()
    spanner_2 = SlurSpanner()

    assert not spanner_1 == spanner_2