from abjad.tools.mathtools.is_integer_equivalent_number import is_integer_equivalent_number
import numbers


def integer_equivalent_number_to_integer(number):
   '''.. versionadded:: 1.1.2
   
   Integer-equivalent `number` to integer::

      abjad> mathtools.integer_equivalent_number_to_integer(17.0)
      17

   Return noninteger-equivalent number unchanged::

      abjad> mathtools.integer_equivalent_number_to_integer(17.5)
      17.5

   Raise type error on nonnumber input::

      abjad> mathtools.integer_equivalent_number_to_integer('foo')
      TypeError

   Return number.
   '''

   if not isinstance(number, numbers.Number):
      raise TypeError('input "%s"% must be number.' % number)

   if is_integer_equivalent_number(number):
      return int(number)
   else:
      return number
