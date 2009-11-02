from abjad import *


def test_text_spanner_interface_grob_handling_01( ):
   '''Handle LilyPond TextSpanner grob.'''

   t = Staff(construct.scale(4))
   t.text_spanner.staff_padding = 6
   Text(t[:])

   r'''
   \new Staff \with {
           \override TextSpanner #'staff-padding = #6
   } {
           c'8 \startTextSpan
           d'8
           e'8
           f'8 \stopTextSpan
   }
   '''
   
   assert check.wf(t)
   assert t.format == "\\new Staff \\with {\n\t\\override TextSpanner #'staff-padding = #6\n} {\n\tc'8 \\startTextSpan\n\td'8\n\te'8\n\tf'8 \\stopTextSpan\n}"
