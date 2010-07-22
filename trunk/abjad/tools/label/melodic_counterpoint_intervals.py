from abjad.leaf import _Leaf
from abjad.note import Note
from abjad.tools import iterate


def melodic_counterpoint_intervals(expr):
   r""".. versionadded:: 1.1.2

   Label the melodic counterpoint interval between every leaf in `expr`. ::

      abjad> staff = Staff(leaftools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Rational(1, 8)]))
      abjad> label.melodic_counterpoint_intervals(staff)
      abjad> f(staff)
      \new Staff {
              c'8 ^ \markup { +15 }
              cs'''8 ^ \markup { -9 }
              b'8 ^ \markup { -9 }
              af8 ^ \markup { -7 }
              bf,8 ^ \markup { 1 }
              b,8 ^ \markup { +14 }
              a'8 ^ \markup { +2 }
              bf'8 ^ \markup { -4 }
              fs'8 ^ \markup { 1 }
              f'8
      }
   """
   from abjad.tools import pitchtools
   
   for note in iterate.naive_forward_in_expr(expr, Note):
      thread_iterator = iterate.thread_forward_from_component(note, _Leaf)
      try:
         thread_iterator.next( )
         next_leaf = thread_iterator.next( )
         if isinstance(next_leaf, Note):
            #mdi = note.pitch - next_leaf.pitch
            #counterpoint_interval_number = mdi.staff_spaces
            #note.markup.up.append(counterpoint_interval_number)
            cpi = pitchtools.melodic_counterpoint_interval_from_to(
               note, next_leaf)
            note.markup.up.append(cpi)
      except StopIteration:
         pass
