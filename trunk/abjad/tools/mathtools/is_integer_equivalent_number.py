from numbers import Number


def is_integer_equivalent_number(expr):
   '''.. versionadded:: 1.1.2

   True `expr` is a number and `expr` is equivalent to an integer::

      abjad> mathtools.is_integer_equivalent_number(12.0)
      True

   Otherwise false::

      abjad> mathtools.is_integer_equivalent_number(Duration(1, 2))
      False

   Return boolean.
   '''

   if isinstance(expr, Number):
      if int(expr) == expr:
         return True

   return False
