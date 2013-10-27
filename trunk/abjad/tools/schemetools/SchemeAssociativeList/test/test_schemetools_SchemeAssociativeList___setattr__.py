# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_schemetools_SchemeAssociativeList___setattr___01():
    r'''Scheme associative lists are immutable.
    '''

    scheme_alist = schemetools.SchemeAssociativeList(('space', 2), ('padding', 0.5))
    assert py.test.raises(AttributeError, "scheme_alist.foo = 'bar'")
