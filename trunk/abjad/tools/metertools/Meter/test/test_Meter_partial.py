from abjad import *


def test_Meter_partial_01( ):

   t = Staff(macros.scale(4))
   contexttools.TimeSignatureMark(2, 8, partial = Duration(1, 8))(t)

   r'''
   \new Staff {
           \time 2/8
           \partial 8
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   #assert t.format == "\\new Staff {\n\t\\partial 8\n\t\\time 2/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
   assert t.format == "\\new Staff {\n\t\\partial 8\n\t\\time 2/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
