# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_schemetools_SchemeVectorConstant___setattr___01():
    r'''Scheme vector constants are immutable.
    '''

    scheme_vector_constant = schemetools.SchemeVectorConstant(True, True, False)
    assert py.test.raises(AttributeError, "scheme_vector_constant.foo = 'bar'")
