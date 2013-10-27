# -*- encoding: utf-8 -*-
from abjad import *


def test_contexttools_ContextMark___repr___01():
    r'''Context mark returns a nonempty string repr.
    '''

    repr = contexttools.ContextMark().__repr__()
    assert isinstance(repr, str) and 0 < len(repr)
