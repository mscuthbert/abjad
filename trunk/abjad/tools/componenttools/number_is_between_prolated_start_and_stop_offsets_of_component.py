from abjad.tools import durtools


def number_is_between_prolated_start_and_stop_offsets_of_component(timepoint, component):
   '''.. versionadded:: 1.1.2

   True when `timepoint` is within the prolated duration of `component`::
   
      abjad> staff = Staff(macros.scale(4))
      abjad> leaf = staff.leaves[0]
      abjad> componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Duration(1, 16), leaf)
      True
      abjad> componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Duration(1, 12), leaf)
      True

   Otherwise false::

      abjad> componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Duration(1, 4), leaf)
      False

   Return boolean.
   '''

   try:
      timepoint = durtools.Duration(timepoint)
   except TypeError:
      pass

   return component._offset.start <= timepoint < \
      component._offset.stop
