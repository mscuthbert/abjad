from abjad import *


def test_componenttools_sum_duration_of_components_in_seconds_01( ):

   tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
   score = Score([Staff([tuplet])])
   contexttools.TempoMark(Duration(1, 4), 48)(score)

   r'''
   \new Score <<
      \new Staff {
         \times 2/3 {
            \tempo 4=48
            c'8
            d'8
            e'8
         }
      }
   >>
   '''

   assert componenttools.sum_duration_of_components_in_seconds(tuplet[:]) == Duration(5, 4)
