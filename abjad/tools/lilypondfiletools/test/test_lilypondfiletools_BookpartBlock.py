# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_BookpartBlock_01():

    bookpart_block = lilypondfiletools.BookpartBlock()

    assert testtools.compare(
        bookpart_block,
        r'''
        \bookpart {}
        '''
        )