from abjad import *


def test_iotools_underscore_delimited_lowercase_to_lowercamelcase_01( ):

   assert iotools.underscore_delimited_lowercase_to_lowercamelcase('foo_bar_blah') == 'fooBarBlah'
