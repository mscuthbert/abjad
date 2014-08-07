# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class DivisionMaker(AbjadValueObject):
    r'''Division-maker.

    ..  container:: example

        ::

            >>> maker = makertools.DivisionMaker(pattern=[(1, 4)])

        ::

            >>> print(format(maker, 'storage'))
            makertools.DivisionMaker(
                pattern=(
                    mathtools.NonreducedFraction(1, 4),
                    ),
                )

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a (possibly empty) nested 
    list of divisions as output (structured one output list per input
    division).

    Follows the two-step configure-once / call-repeatedly pattern established
    for the rhythm-makers.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_cyclic',
        '_fuse_remainder',
        '_pattern',
        '_pattern_rotation_index',
        '_remainder',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        cyclic=None,
        fuse_remainder=None,
        pattern=None,
        pattern_rotation_index=None,
        remainder=None,
        ):
        if cyclic is not None:
            assert isinstance(cyclic, bool), repr(cyclic)
        self._cyclic = cyclic
        if fuse_remainder is not None:
            assert isinstance(fuse_remainder, bool), repr(fuse_remainder)
        self._fuse_remainder = fuse_remainder
        if pattern is not None:
            pattern_ = []
            for division in pattern:
                division = mathtools.NonreducedFraction(division)
                pattern_.append(division)
            pattern = tuple(pattern_)
        self._pattern = pattern
        if not remainder is None:
            assert remainder in (Left, Right), repr(remainder)
        if pattern_rotation_index is not None:
            assert isinstance(pattern_rotation_index, int)
        self._pattern_rotation_index = pattern_rotation_index
        self._remainder = remainder

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Calls division-maker on `divisions`.

        ..  container:: example

            Calls division-maker on division with no remainder:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 4)],
                ...     )
                >>> lists = maker([(3, 4)])
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 4)]

        ..  container:: example

            Calls division-maker on division with remainder:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 4)],
                ...     remainder=Right,
                ...     )
                >>> lists = maker([(7, 8)])
                >>> for list_ in lists:
                ...     list_ 
                [NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 8)]

            Positions remainder at right of output because divison-maker
            `remainder` defaults to right.

        ..  container:: example

            Calls division-maker with pattern set to none:

            ::

                >>> maker = makertools.DivisionMaker()
                >>> lists = maker([(6, 32)])
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(6, 32)]

            Returns input division unchanged.

        ..  container:: example

            Calls division-maker on nothing:

            ::

                >>> maker = makertools.DivisionMaker(pattern=[(1, 4)])
                >>> maker()
                []

            Returns empty list.

        Returns possibly empty list of divisions.
        '''
        divisions = divisions or []
        if not divisions:
            return []
        division_lists = []
        for i, division in enumerate(divisions):
            input_division = mathtools.NonreducedFraction(division)
            input_duration = durationtools.Duration(input_division)
            assert 0 < input_division, repr(input_division)
            if not self.pattern:
                division_list = [input_division]
                division_lists.append(division_list)
                continue
            division_list = list(self.pattern)
            pattern_rotation_index = self.pattern_rotation_index or 0
            pattern_rotation_index *= i
            division_list = sequencetools.rotate_sequence(
                division_list,
                pattern_rotation_index,
                )
            if self.cyclic:
                division_list = sequencetools.repeat_sequence_to_weight(
                    division_list,
                    input_division,
                    allow_total=Less,
                    )
            total_duration = durationtools.Duration(sum(division_list))
            if total_duration == input_duration:
                division_lists.append(division_list)
                continue
            if self.remainder is None:
                message = 'can not fill {} from {} exactly.'
                message = message.format(input_division, self.pattern)
                raise Exception(message)
            remainder = input_division - total_duration
            remainder = durationtools.Duration(remainder)
            remainder = mathtools.NonreducedFraction(remainder)
            if self.remainder is Left and not self.fuse_remainder:
                division_list.insert(0, remainder)
            elif self.remainder is Left and self.fuse_remainder:
                division_list[0] += remainder
            elif self.remainder is Right and not self.fuse_remainder:
                division_list.append(remainder)
            elif self.remainder is Right and self.fuse_remainder:
                division_list[-1] += remainder
            else:
                raise ValueError((self.remainder, fuse_remainder))
            total_duration = durationtools.Duration(sum(division_list))
            pair = total_duration, input_duration
            assert total_duration == input_duration, pair
            division_lists.append(division_list)
        return division_lists

    ### PUBLIC PROPERTIES ###

    @property
    def cyclic(self):
        r'''Is true when division-maker reads pattern cyclically.
        Otherwise false.

        ..  container:: example

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 4)],
                ...     )

            ::

                >>> maker.cyclic
                True

        Returns boolean or none.
        '''
        return self._cyclic

    @property
    def fuse_remainder(self):
        r'''Is true when remainder fuses to first or last division.
        Otherwise false.

        ..  container:: example

            **Example 1.** Remainder unfused to the right:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     fuse_remainder=False,
                ...     pattern=[(1, 4)],
                ...     remainder=Right,
                ...     )

            ::

                >>> lists = maker([(5, 8)])
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 8)]

        ..  container:: example

            **Example 2.** Remainder fused to the right:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     fuse_remainder=True,
                ...     pattern=[(1, 4)],
                ...     remainder=Right,
                ...     )

            ::

                >>> lists = maker([(5, 8)])
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 4), NonreducedFraction(3, 8)]

        ..  container:: example

            **Example 3.** Remainder unfused to the left:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     fuse_remainder=False,
                ...     pattern=[(1, 4)],
                ...     remainder=Left,
                ...     )

            ::

                >>> lists = maker([(5, 8)])
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 8), NonreducedFraction(1, 4), NonreducedFraction(1, 4)]

        ..  container:: example

            **Example 4.** Remainder fused to the left:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     fuse_remainder=True,
                ...     pattern=[(1, 4)],
                ...     remainder=Left,
                ...     )

            ::

                >>> lists = maker([(5, 8)])
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(3, 8), NonreducedFraction(1, 4)]

        Returns boolean or none.
        '''
        return self._fuse_remainder

    @property
    def pattern(self):
        r'''Gets pattern of division-maker.

        ..  container:: example

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 4)],
                ...     )

            ::

                >>> maker.pattern
                (NonreducedFraction(1, 4),)

        Returns (possibly empty) tuple of divisions or none.
        '''
        return self._pattern

    @property
    def pattern_rotation_index(self):
        r'''Gets pattern rotation index of division-maker.

        ..  container:: example

            **Example 1.** Does not rotate pattern:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 16), (1, 8), (1, 4)],
                ...     )

            ::

                >>> lists = maker([(7, 16), (7, 16), (7, 16)])
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 16), NonreducedFraction(1, 8), NonreducedFraction(1, 4)]
                [NonreducedFraction(1, 16), NonreducedFraction(1, 8), NonreducedFraction(1, 4)]
                [NonreducedFraction(1, 16), NonreducedFraction(1, 8), NonreducedFraction(1, 4)]

            All input divisions treated the same.

        ..  container:: example

            **Example 2.** Rotates pattern one element to the left on each new
            input division:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 16), (1, 8), (1, 4)],
                ...     pattern_rotation_index=-1,
                ...     )

            ::

                >>> lists = maker([(7, 16), (7, 16), (7, 16)])
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 16), NonreducedFraction(1, 8), NonreducedFraction(1, 4)]
                [NonreducedFraction(1, 8), NonreducedFraction(1, 4), NonreducedFraction(1, 16)]
                [NonreducedFraction(1, 4), NonreducedFraction(1, 16), NonreducedFraction(1, 8)]

        ..  container:: example

            **Example 3.** Rotates pattern one element to the right on each new
            input division:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 16), (1, 8), (1, 4)],
                ...     pattern_rotation_index=1,
                ...     )

            ::

                >>> lists = maker([(7, 16), (7, 16), (7, 16)])
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 16), NonreducedFraction(1, 8), NonreducedFraction(1, 4)]
                [NonreducedFraction(1, 4), NonreducedFraction(1, 16), NonreducedFraction(1, 8)]
                [NonreducedFraction(1, 8), NonreducedFraction(1, 4), NonreducedFraction(1, 16)]

        Returns integer or none.
        '''
        return self._pattern_rotation_index

    @property
    def remainder(self):
        r'''Gets direction to which any remainder will be positioned.

        ..  container:: example

            Positions remainder to right of noncyclic pattern:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=False,
                ...     pattern=[(4, 16), (1, 16)],
                ...     remainder=Right,
                ...     )
                >>> lists = maker([(3, 4)])
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(4, 16), NonreducedFraction(1, 16), NonreducedFraction(7, 16)]

        ..  container:: example

            Positions remainder to right of cyclic pattern:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(4, 16), (1, 16)],
                ...     remainder=Right,
                ...     )
                >>> lists = maker([(3, 4)])
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(4, 16), NonreducedFraction(1, 16), NonreducedFraction(4, 16), NonreducedFraction(1, 16), NonreducedFraction(1, 8)]

        ..  container:: example

            Positions remainder to left of noncyclic pattern:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=False,
                ...     pattern=[(1, 4), (1, 16)],
                ...     remainder=Left,
                ...     )
                >>> lists = maker([(3, 4)])
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(7, 16), NonreducedFraction(1, 4), NonreducedFraction(1, 16)]

        ..  container:: example

            Positions remainder to left of cyclic pattern:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 4), (1, 16)],
                ...     remainder=Left,
                ...     )
                >>> lists = maker([(3, 4)])
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 8), NonreducedFraction(1, 4), NonreducedFraction(1, 16), NonreducedFraction(1, 4), NonreducedFraction(1, 16)]

        Returns left, right or none.
        '''
        return self._remainder