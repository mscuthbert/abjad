from abjad.tools import iterate


def leaf_indices(expr, direction = 'below'):
   r'''Label leaf indices in `expr` from 0.

   ::

      abjad> staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> label.leaf_indices(staff)
      \new Staff {
              c'8 _ \markup { \small 0 }
              d'8 _ \markup { \small 1 }
              e'8 _ \markup { \small 2 }
              f'8 _ \markup { \small 3 }
      } 

   .. versionadded:: 1.1.2
      new `direction` keyword parameter.
   '''

   for i, leaf in enumerate(iterate.leaves_forward_in_expr(expr)):
      label = r'\small %s' % i
      if direction == 'below':
         leaf.markup.down.append(label)
      elif direction == 'above':
         leaf.markup.up.append(label)
      else:
         raise ValueError("must be 'above' or 'below'.")
