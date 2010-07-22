from abjad.tools import iterate
from abjad.tools import pitchtools


def leaf_pitch_numbers(expr):
   r'''Label the pitch of every leaf in `expr`.

   ::

      abjad> staff = Staff(leaftools.make_leaves([None, 12, [13, 14, 15], None], [(1, 4)]))
      abjad> label.leaf_pitch_numbers(staff)
      abjad> f(staff)
      \new Staff {
              r4
              c''4 _ \markup { \small 12 }
              <cs'' d'' ef''>4 _ \markup { \column { \small 15 \small 14 \small 13 } }
              r4
      }
   '''

   for leaf in iterate.leaves_forward_in_expr(expr):
      for pitch in reversed(pitchtools.get_pitches(leaf)):
         pitch_number = r'\small %s' % pitch.number
         leaf.markup.down.append(pitch_number)
