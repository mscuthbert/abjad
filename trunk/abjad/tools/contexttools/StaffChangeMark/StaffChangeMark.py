from abjad.tools.contexttools.ContextMark import ContextMark


class StaffChangeMark(ContextMark):
   '''.. versionadded:: 1.1.2

   Abjad model of a staff change::

      abjad> staff = Staff([ ])
      abjad> staff.name = 'RH Staff'

   ::

      abjad> contexttools.StaffChangeMark(staff)
      StaffChangeMark(Staff-"RH Staff"{ })
   '''

   _format_slot = 'opening'

   def __init__(self, staff, target_context = None):
      from abjad.components import Staff
      ContextMark.__init__(self, target_context = target_context)
      if self.target_context is None:
         self._target_context = Staff
      if not isinstance(staff, Staff):
         raise TypeError('staff change mark input value "%s" must be staff instance.' % str(staff))
      self._staff = staff

   ## OVERLOADS ##

   def __copy__(self, *args):
      return type(self)(self.staff, target_context = self.target_context)

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self.staff is arg.staff
      return False

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents_repr_string(self):
      return repr(self.staff)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return r'\change Staff = %s' % self.staff.name

   @property
   def staff(self):
      return self._staff
