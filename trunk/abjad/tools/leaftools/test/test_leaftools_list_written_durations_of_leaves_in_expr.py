from abjad import *


def test_leaftools_list_written_durations_of_leaves_in_expr_01( ):

   staff = Staff(tuplettools.FixedDurationTuplet((2, 8), macros.scale(3)) * 2)
   durations = leaftools.list_written_durations_of_leaves_in_expr(staff)

   assert durations == [Duration(1, 8), Duration(1, 8), Duration(1, 8), 
      Duration(1, 8), Duration(1, 8), Duration(1, 8)]
