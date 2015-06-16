# -*- encoding: utf-8 -*-
import collections
import fractions
import functools
import math
import numbers
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import schemetools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.topleveltools import new


@functools.total_ordering
class Tempo(AbjadValueObject):
    r'''Tempo indicator.

    ..  container:: example

        **Example 1.** Fifty-two eighth notes per minute:

        ::

            >>> score = Score([])
            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> score.append(staff)
            >>> tempo = Tempo(Duration(1, 8), 52)
            >>> attach(tempo, staff[0])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    \tempo 8=52
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    ..  container:: example

        **Example 2.** Ninety quarter notes per minute:

        ::

            >>> score = Score([])
            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> score.append(staff)
            >>> tempo = Tempo(Duration(1, 4), 90)
            >>> attach(tempo, staff[0])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    \tempo 4=90
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    ..  container:: example

        **Example 3.** Float-valued tempo:

        ::

            >>> score = Score([])
            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> score.append(staff)
            >>> tempo = Tempo(Duration(1, 4), 90.1)
            >>> attach(tempo, staff[0])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    \tempo \markup {
                        \scale
                            #'(0.75 . 0.75)
                            \score
                                {
                                    \new Score \with {
                                        \override SpacingSpanner #'spacing-increment = #0.5
                                        proportionalNotationDuration = ##f
                                    } <<
                                        \new RhythmicStaff \with {
                                            \remove Time_signature_engraver
                                            \remove Staff_symbol_engraver
                                            \override Stem #'direction = #up
                                            \override Stem #'length = #5
                                            \override TupletBracket #'bracket-visibility = ##t
                                            \override TupletBracket #'direction = #up
                                            \override TupletBracket #'padding = #1.25
                                            \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                            \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                            tupletFullLength = ##t
                                        } {
                                            c'4
                                        }
                                    >>
                                    \layout {
                                        indent = #0
                                        ragged-right = ##t
                                    }
                                }
                        =
                        \general-align
                            #Y
                            #-0.5
                            90.1
                        }
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        '_markup',
        '_reference_duration',
        '_textual_indication',
        '_units_per_minute',
        )

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(
        self, 
        reference_duration=None,
        units_per_minute=None,
        textual_indication=None,
        markup=None,
        ):
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        self._default_scope = scoretools.Score
        assert isinstance(textual_indication, (str, type(None)))
        arguments = (reference_duration, units_per_minute, textual_indication)
        if all(_ is None for _ in arguments):
            reference_duration = (1, 4)
            units_per_minute = 60
        if reference_duration:
            reference_duration = durationtools.Duration(reference_duration)
        prototype = (
            int, 
            float, 
            fractions.Fraction,
            collections.Sequence, 
            type(None),
            )
        assert isinstance(units_per_minute, prototype)
        if isinstance(units_per_minute, collections.Sequence):
            assert len(units_per_minute) == 2
            prototype = (int, float, durationtools.Duration)
            assert all(isinstance(x, prototype) for x in units_per_minute)
            units_per_minute = tuple(sorted(units_per_minute))
        if isinstance(units_per_minute, float):
            units_per_minute = mathtools.integer_equivalent_number_to_integer(
                units_per_minute)
        self._reference_duration = reference_duration
        self._textual_indication = textual_indication
        self._units_per_minute = units_per_minute
        if markup is not None:
            assert isinstance(markup, markuptools.Markup), repr(markup)
        self._markup = markup

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Adds tempo to `expr`.

        ..  container:: example

            **Example 1.** Adds one tempo to another:

            ::

                >>> Tempo(Duration(1, 4), 60) + Tempo(Duration(1, 4), 90)
                Tempo(reference_duration=Duration(1, 4), units_per_minute=150)

        ..  container:: example

            **Example 2.** Returns none when `expr` is not a tempo:

            ::

                >>> Tempo(Duration(1, 4), 60) + 90 is None
                True

        Returns new tempo or none.
        '''
        if isinstance(expr, type(self)):
            if self.is_imprecise or expr.is_imprecise:
                raise ImpreciseTempoError
            new_quarters_per_minute = \
                self.quarters_per_minute + expr.quarters_per_minute
            minimum_denominator = \
                min((self.reference_duration.denominator, expr.reference_duration.denominator))
            nonreduced_fraction = \
                mathtools.NonreducedFraction(new_quarters_per_minute / 4)
            nonreduced_fraction = \
                nonreduced_fraction.with_denominator(minimum_denominator)
            new_units_per_minute, new_reference_duration_denominator = \
                nonreduced_fraction.pair
            new_reference_duration = \
                durationtools.Duration(1, new_reference_duration_denominator)
            new_tempo = type(self)(
                new_reference_duration,
                new_units_per_minute,
                )
            return new_tempo

    def __div__(self, expr):
        r'''Divides tempo by `expr`.

        ..  container:: example

            **Example 1.** Divides tempo by number:

            ::

                >>> Tempo(Duration(1, 4), 60) / 2
                Tempo(reference_duration=Duration(1, 4), units_per_minute=30)

        ..  container:: example

            **Example 2.** Divides tempo by other tempo:

            ::

                >>> Tempo(Duration(1, 4), 60) / Tempo(Duration(1, 4), 40)
                Multiplier(3, 2)

        Returns new tempo or multiplier.
        '''
        if self.is_imprecise:
            raise ImpreciseTempoError
        if getattr(expr, 'is_imprecise', False):
            raise ImpreciseTempoError
        if isinstance(expr, type(self)):
            result = self.quarters_per_minute / expr.quarters_per_minute
            return durationtools.Multiplier(result)
        elif isinstance(expr, numbers.Number):
            units_per_minute = self.units_per_minute / expr
            result = new(self, units_per_minute=units_per_minute)
            return result
        else:
            message = 'must be number or tempo indication: {!r}.'
            message = message.format(expr)
            raise TypeError(message)

    def __format__(self, format_specification=''):
        r'''Formats tempo.

        Set `format_specification` to `''`', `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            **Example 1.** Works without markup:
            
            ::

                >>> tempo = Tempo((1, 4), 84, 'Allegro')
                >>> print(format(tempo))
                indicatortools.Tempo(
                    reference_duration=durationtools.Duration(1, 4),
                    units_per_minute=84,
                    textual_indication='Allegro',
                    )

        ..  container:: example

            **Example 2.** Works with markup:
            
            ::

                >>> markup = Markup(r'\italic { Allegro }')
                >>> tempo = Tempo((1, 4), 84, markup=markup)
                >>> print(format(tempo))
                indicatortools.Tempo(
                    reference_duration=durationtools.Duration(1, 4),
                    units_per_minute=84,
                    markup=markuptools.Markup(
                        contents=(
                            markuptools.MarkupCommand(
                                'italic',
                                ['Allegro']
                                ),
                            ),
                        ),
                    )

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        elif format_specification == 'lilypond':
            return self._lilypond_format
        return str(self)

    def __lt__(self, arg):
        r'''Is true when `arg` is a tempo with quarters per minute greater than
        that of this tempo. Otherwise false.

        Returns boolean.
        '''
        assert isinstance(arg, type(self)), repr(arg)
        return self.quarters_per_minute < arg.quarters_per_minute

    def __mul__(self, multiplier):
        r'''Multiplies tempo by `multiplier`.

        ..  container:: example

            **Example 1.** Doubles tempo:

            ::

                >>> tempo = Tempo(Duration(1, 4), 84)
                >>> 2 * tempo
                Tempo(reference_duration=Duration(1, 4), units_per_minute=168)

        ..  container:: example

            **Example 2.** Triples tempo:

            ::

                >>> tempo = Tempo(Duration(1, 4), 84)
                >>> 3 * tempo
                Tempo(reference_duration=Duration(1, 4), units_per_minute=252)

        Returns new tempo.
        '''
        if not isinstance(multiplier, (int, float, durationtools.Duration)):
            return
        if self.is_imprecise:
            raise ImpreciseTempoError
        new_units_per_minute = multiplier * self.units_per_minute
        new_reference_duration = durationtools.Duration(
            self.reference_duration)
        new_tempo = type(self)(
            reference_duration=new_reference_duration, 
            units_per_minute=new_units_per_minute,
            )
        return new_tempo

    def __rmul__(self, multiplier):
        r'''Multiplies `multiplier` by tempo.

        ..  container::: example

            **Example 1.** Doubles tempo:

            ::

                >>> tempo = Tempo(Duration(1, 4), 84)
                >>> tempo * 2
                Tempo(reference_duration=Duration(1, 4), units_per_minute=168)

        ..  container::: example

            **Example 2.** Triples tempo:

            ::

                >>> tempo = Tempo(Duration(1, 4), 84)
                >>> tempo * 3
                Tempo(reference_duration=Duration(1, 4), units_per_minute=252)

        Returns new tempo.
        '''
        if not isinstance(multiplier, (int, float, durationtools.Duration)):
            return
        if self.is_imprecise:
            raise ImpreciseTempoError
        new_units_per_minute = multiplier * self.units_per_minute
        new_reference_duration = durationtools.Duration(
            self.reference_duration)
        new_tempo = type(self)(
            reference_duration=new_reference_duration, 
            units_per_minute=new_units_per_minute,
            )
        return new_tempo

    def __str__(self):
        r'''Gets string representation of tempo.

        ..  container:: example

            **Example 1.** Fifty-two eighth notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 8), 52)
                >>> str(tempo)
                '8=52'

        ..  container:: example

            **Example 2.** Ninety quarter notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> str(tempo)
                '4=90'

        Returns string.
        '''
        return self._equation or self.textual_indication

    def __sub__(self, expr):
        r'''Subtracts `expr` from tempo.

        ..  container:: example

            **Example 1.** Same reference reference durations:
            ::

                >>> tempo_1 = Tempo(Duration(1, 4), 90)
                >>> tempo_2 = Tempo(Duration(1, 4), 60)
                >>> tempo_1 - tempo_2
                Tempo(reference_duration=Duration(1, 4), units_per_minute=30)

        ..  container:: example

            **Example 2.** Different reference durations:
            ::

                >>> tempo_1 = Tempo(Duration(1, 4), 90)
                >>> tempo_2 = Tempo(Duration(1, 2), 90)
                >>> tempo_1 - tempo_2
                Tempo(reference_duration=Duration(1, 4), units_per_minute=45)

        Returns new tempo.
        '''
        if not isinstance(expr, type(self)):
            message = 'must be tempo: {!r}.'
            message = message.format(expr)
            raise Exception(message)
        if self.is_imprecise or expr.is_imprecise:
            raise ImpreciseTempoError
        new_quarters_per_minute = self.quarters_per_minute - \
            expr.quarters_per_minute
        minimum_denominator = min((
            self.reference_duration.denominator,
            expr.reference_duration.denominator,
            ))
        nonreduced_fraction = mathtools.NonreducedFraction(
            new_quarters_per_minute / 4)
        nonreduced_fraction = nonreduced_fraction.with_denominator(
            minimum_denominator)
        new_units_per_minute, new_reference_duration_denominator = \
            nonreduced_fraction.pair
        new_reference_duration = durationtools.Duration(
            1, new_reference_duration_denominator)
        new_tempo = type(self)(
            reference_duration=new_reference_duration, 
            units_per_minute=new_units_per_minute,
            )
        return new_tempo

    def __truediv__(self, expr):
        r'''Divides tempo by `expr`. Operator required by Python 3.

        ..  container:: example

            **Example 1.** Divides tempo by number:

            ::

                >>> Tempo(Duration(1, 4), 60).__truediv__(2)
                Tempo(reference_duration=Duration(1, 4), units_per_minute=30)

        ..  container:: example

            **Example 2.** Divides tempo by other tempo:

            ::

                >>> Tempo(Duration(1, 4), 60).__truediv__(
                ...     Tempo(Duration(1, 4), 40)
                ...     )
                Multiplier(3, 2)

        Returns new tempo.
        '''
        return self.__div__(expr)

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from ide import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='reference_duration',
                command='d',
                editor=idetools.getters.get_duration,
                is_keyword=False,
                ),
            systemtools.AttributeDetail(
                name='units_per_minute',
                command='pm',
                editor=idetools.getters.get_integer,
                is_keyword=False,
                ),
            systemtools.AttributeDetail(
                name='textual_indication',
                command='ti',
                editor=idetools.getters.get_integer,
                is_keyword=True,
                ),
            systemtools.AttributeDetail(
                name='markup',
                command='m',
                editor=idetools.getters.get_markup,
                is_keyword=True,
                ),
            )

    @property
    def _dotted(self):
        return self.reference_duration.lilypond_duration_string

    @property
    def _equation(self):
        if self.reference_duration is None:
            return
        if isinstance(self.units_per_minute, tuple):
            string = '{}={}-{}'
            string = string.format(
                self._dotted,
                self.units_per_minute[0],
                self.units_per_minute[1],
                )
            return string
        elif isinstance(self.units_per_minute, float):
            markup = Tempo.make_tempo_equation_markup(
                self.reference_duration,
                self.units_per_minute,
                )
            string = str(markup)
            return string
        string = '{}={}'
        string = string.format(self._dotted, self.units_per_minute)
        return string

    @property
    def _lilypond_format(self):
        text, equation = None, None
        if self.textual_indication is not None:
            text = self.textual_indication
            text = schemetools.Scheme.format_scheme_value(text)
        if (self.reference_duration is not None and 
            self.units_per_minute is not None):
            equation = self._equation
        if self.markup is not None:
            return r'\tempo {}'.format(self.markup)
        elif text and equation:
            return r'\tempo {} {}'.format(text, equation)
        elif equation:
            return r'\tempo {}'.format(equation)
        elif text:
            return r'\tempo {}'.format(text)
        else:
            return r'\tempo \default'

    @property
    def _one_line_menu_summary(self):
        result = self._lilypond_format
        if result.startswith(r'\tempo '):
            result = result[7:]
        elif result.startswith(r'\markup '):
            result = result[8:]
        else:
            raise ValueError(result)
        return result

    @property
    def _repr_specification(self):
        return new(
            self._storage_format_specification,
            is_indented=False,
            )

    ### PRIVATE METHODS ###

    def _make_lhs_score_markup(self, reference_duration=None):
        from abjad.tools import scoretools
        reference_duration = reference_duration or self.reference_duration
        selection = scoretools.make_notes([0], [reference_duration])
        markup = durationtools.Duration._to_score_markup(selection)
        return markup

    def _to_markup(self):
        from abjad.tools import markuptools
        if self.markup is not None:
            return self.markup
        duration_log = int(math.log(self.reference_duration.denominator, 2))
        lhs = markuptools.Markup.note_by_number(
            duration_log, 
            self.reference_duration.dot_count,
            1,
            )
        lhs = lhs.general_align('Y', Down).fontsize(-6)
        left_space = markuptools.Markup.hspace(0.5)
        equals = markuptools.Markup('=')
        #right_space = markuptools.Markup.hspace(0.1)
        units = markuptools.Markup(self.units_per_minute)
        #rhs = left_space + equals + right_space + units
        rhs = equals + units
        #rhs = rhs.fontsize(3).upright()
        rhs = rhs.upright()
        markup = lhs + rhs
        return markup

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of tempo.

        ..  container:: example

            **Example 1.** Fifty-two eighth notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 8), 52)
                >>> tempo.default_scope
                <class 'abjad.tools.scoretools.Score.Score'>

        ..  container:: example

            **Example 2.** Ninety quarter notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> tempo.default_scope
                <class 'abjad.tools.scoretools.Score.Score'>

        Returns score.
        '''
        return self._default_scope

    @property
    def is_imprecise(self):
        r'''Is true if tempo is entirely textual or if tempo's
        units_per_minute is a range. Otherwise false.

        ..  container:: example

            **Example 1.** Imprecise tempos:

            ::

                >>> Tempo(Duration(1, 4), 60).is_imprecise
                False
                >>> Tempo(4, 60, 'Langsam').is_imprecise
                False
                >>> Tempo(textual_indication='Langsam').is_imprecise
                True
                >>> Tempo(4, (35, 50), 'Langsam').is_imprecise
                True
                >>> Tempo(Duration(1, 4), (35, 50)).is_imprecise
                True

        ..  container:: example

            **Example 2.** Precise tempo:

            ::

                >>> Tempo(Duration(1, 4), 60).is_imprecise
                False

        Returns boolean.
        '''
        if self.reference_duration is not None:
            if self.units_per_minute is not None:
                if not isinstance(self.units_per_minute, tuple):
                    return False
        return True

    @property
    def markup(self):
        r'''Gets optional tempo markup.

        ..  container:: example

            **Example 1.** With custom markup:

            ::

                >>> markup = Markup(r'\smaller \general-align #Y #DOWN \note-by-number #2 #0 #1 " = 67.5"')
                >>> tempo = Tempo(Duration(1, 4), 67.5, markup=markup)
                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> score = Score([staff])
                >>> attach(tempo, staff)
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        \tempo \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        " = 67.5"
                        }
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                >>

        Set to markup or none.

        Defaults to none.

        Ignores all other tempo attributes at format time when markup is set.

        Returns markup or none.
        '''
        return self._markup

    @property
    def quarters_per_minute(self):
        r'''Gets quarters per minute of tempo.

        ..  container:: example

            **Example 1.** Fifty-two eighth notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 8), 52)
                >>> tempo.quarters_per_minute
                Fraction(104, 1)

        ..  container:: example

            **Example 2.** Ninety quarter notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> tempo.quarters_per_minute
                Fraction(90, 1)

        Returns tuple when tempo `units_per_minute` is a range.

        Returns none when tempo is imprecise.

        Returns fraction otherwise.
        '''
        if self.is_imprecise:
            return None
        if isinstance(self.units_per_minute, tuple):
            low = durationtools.Duration(1, 4) / self.reference_duration * \
                self.units_per_minute[0]
            high = durationtools.Duration(1, 4) / self.reference_duration * \
                self.units_per_minute[1]
            return (low, high)
        result = durationtools.Duration(1, 4) / self.reference_duration * \
            self.units_per_minute
        return fractions.Fraction(result)

    @property
    def reference_duration(self):
        r'''Gets reference duration of tempo.

        ..  container:: example

            **Example 1.** Fifty-two eighth notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 8), 52)
                >>> tempo.reference_duration
                Duration(1, 8)

        ..  container:: example

            **Example 2.** Ninety quarter notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> tempo.reference_duration
                Duration(1, 4)

        Returns duration.
        '''
        return self._reference_duration

    @property
    def textual_indication(self):
        r'''Gets optional textual indication of tempo.

        ..  container:: example

            **Example 1.** Fifty-two eighth notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 8), 52)
                >>> tempo.textual_indication is None
                True

        ..  container:: example

            **Example 2.** Ninety quarter notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> tempo.textual_indication is None
                True

        Returns string or none.
        '''
        return self._textual_indication

    @property
    def units_per_minute(self):
        r'''Gets units per minute of tempo.

        ..  container:: example

            **Example 1.** Fifty-two eighth notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 8), 52)
                >>> tempo.units_per_minute
                52

        ..  container:: example

            **Example 2.** Ninety quarter notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> tempo.units_per_minute
                90

        ..  container:: example

            **Example 3.** Abjad allows float-valued tempi:

            ::

                >>> tempo = Tempo(Duration(1, 4), 90.1)
                >>> tempo.units_per_minute
                90.1

            ::

                >>> score = Score([])
                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> score.append(staff)
                >>> attach(tempo, staff[0])
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> print(format(score))
                \new Score <<
                    \new Staff {
                        \tempo \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            =
                            \general-align
                                #Y
                                #-0.5
                                90.1
                            }
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                >>

        ..  container:: example

            **Example 4.** Abjad allows rational-valued tempi:

            ::

                >>> tempo = Tempo(Duration(1, 4), Fraction(121, 2))
                >>> tempo.units_per_minute
                Fraction(121, 2)

            ::

                >>> score = Score([])
                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> score.append(staff)
                >>> attach(tempo, staff[0])
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> print(format(score))
                \new Score <<
                    \new Staff {
                        \tempo 4=121/2
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                >>

            But note that LilyPond rejects rational-valued tempi.

            ..  todo:: Implement something to allow rational-valued tempi
                in LilyPond output.

        Set to number or none.

        Defaults to none

        Returns number or none.
        '''
        return self._units_per_minute

    ### PUBLIC METHODS ###

    def duration_to_milliseconds(self, duration):
        r'''Gets millisecond value of `duration` under a given tempo.

        ..  container:: example

            **Example 1.** One quarter lasts 1000 msec at quarter equals 60 MM:

            ::

                >>> tempo = Tempo((1, 4), 60)
                >>> tempo.duration_to_milliseconds(Duration(1, 4))
                Duration(1000, 1)

        ..  container:: example

            **Example 1.** Dotted sixteenth lasts 1500 msec at quarter equals
            60 MM:

            ::

                >>> tempo = Tempo((1, 4), 60)
                >>> tempo.duration_to_milliseconds(Duration(3, 8))
                Duration(1500, 1)

        Returns duration.
        '''
        duration = durationtools.Duration(duration)
        # TODO: rewrite formula without line breaks;
        #       use two or three temporary variables instead. 
        whole_note_duration = 1000 \
            * durationtools.Multiplier(
                self.reference_duration.denominator,
                self.reference_duration.numerator,
                ) \
            * durationtools.Multiplier(
                60,
                self.units_per_minute,
                )
        return durationtools.Duration(duration * whole_note_duration)

    def list_related_tempos(
        self,
        maximum_numerator=None,
        maximum_denominator=None,
        ):
        r'''Lists related tempos.

        ..  container:: example

            **Example 1.** Rewrites tempo ``58`` MM by ratios of the form
            ``n:d`` such that ``1 <= n <= 8`` and ``1 <= d <= 8``. As follows:

            ::

                >>> tempo = Tempo(Duration(1, 4), 58)
                >>> pairs = tempo.list_related_tempos(
                ...     maximum_numerator=8,
                ...     maximum_denominator=8,
                ...     )

            ::

                >>> for tempo, ratio in pairs:
                ...     string = '{!s}\t{!s}'.format(tempo, ratio)
                ...     print(string)
                4=29    1:2
                4=58    1:1
                4=87    3:2
                4=116   2:1

        ..  container:: example

            **Example 2.** Rewrites tempo ``58`` MM by ratios of the form
            ``n:d`` such that ``1 <= n <= 30`` and ``1 <= d <= 30``. As
            follows:

            ::

                >>> tempo = Tempo(Duration(1, 4), 58)
                >>> pairs = tempo.list_related_tempos(
                ...     maximum_numerator=30,
                ...     maximum_denominator=30,
                ...     )

            ::

                >>> for tempo, ratio in pairs:
                ...     string = '{!s}\t{!s}'.format(tempo, ratio)
                ...     print(string)
                ... 
                4=30    15:29
                4=32    16:29
                4=34    17:29
                4=36    18:29
                4=38    19:29
                4=40    20:29
                4=42    21:29
                4=44    22:29
                4=46    23:29
                4=48    24:29
                4=50    25:29
                4=52    26:29
                4=54    27:29
                4=56    28:29
                4=58    1:1
                4=60    30:29

        Returns list of tempo / ratio pairs.

        Each new tempo equals not less than half of this tempo
        and not more than twice this tempo.

        Returns list.
        '''
        # assert integer tempo
        assert isinstance(self.units_per_minute, int), repr(self)
        # find divisors
        divisors = mathtools.divisors(self.units_per_minute)
        if maximum_denominator is not None:
            divisors = [x for x in divisors if x <= maximum_denominator]
        # make pairs
        pairs = []
        for divisor in divisors:
            start = int(math.ceil(divisor / 2.0))
            stop = 2 * divisor
            numerators = range(start, stop + 1)
            if maximum_numerator is not None:
                    numerators = [
                        x for x in numerators
                        if x <= maximum_numerator
                        ]
        for numerator in numerators:
                ratio = mathtools.Ratio((numerator, divisor))
                multiplier = durationtools.Multiplier(ratio.numbers)
                new_units_per_minute = multiplier * self.units_per_minute
                assert mathtools.is_integer_equivalent_expr(
                    new_units_per_minute)
                new_units_per_minute = int(new_units_per_minute)
                new_tempo = type(self)(
                    reference_duration=self.reference_duration, 
                    units_per_minute=new_units_per_minute,
                    )
                pair = (new_tempo, ratio)
                if pair not in pairs:
                    pairs.append(pair)
        # sort pairs
        pairs.sort()
        # return pairs
        return pairs

    @staticmethod
    def make_tempo_equation_markup(reference_duration, units_per_minute):
        r'''Makes tempo equation markup.

        ..  container:: example

            **Example 1.** Integer-valued tempo:

            ::

                >>> markup = Tempo.make_tempo_equation_markup(Duration(1, 4), 90)
                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score \with {
                                    \override SpacingSpanner #'spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                } <<
                                    \new RhythmicStaff \with {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem #'direction = #up
                                        \override Stem #'length = #5
                                        \override TupletBracket #'bracket-visibility = ##t
                                        \override TupletBracket #'direction = #up
                                        \override TupletBracket #'padding = #1.25
                                        \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                        \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    } {
                                        c'4
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \general-align
                        #Y
                        #-0.5
                        90
                    }

        ..  container:: example

            **Example 2.** Float-valued tempo:

            ::

                >>> markup = Tempo.make_tempo_equation_markup(Duration(1, 4), 90.1)
                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score \with {
                                    \override SpacingSpanner #'spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                } <<
                                    \new RhythmicStaff \with {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem #'direction = #up
                                        \override Stem #'length = #5
                                        \override TupletBracket #'bracket-visibility = ##t
                                        \override TupletBracket #'direction = #up
                                        \override TupletBracket #'padding = #1.25
                                        \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                        \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    } {
                                        c'4
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \general-align
                        #Y
                        #-0.5
                        90.1
                    }

        ..  container:: example

            **Example 3.** Reference duration expressed with ties:

            ::

                >>> markup = Tempo.make_tempo_equation_markup(Duration(5, 16), 90.1)
                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score \with {
                                    \override SpacingSpanner #'spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                } <<
                                    \new RhythmicStaff \with {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem #'direction = #up
                                        \override Stem #'length = #5
                                        \override TupletBracket #'bracket-visibility = ##t
                                        \override TupletBracket #'direction = #up
                                        \override TupletBracket #'padding = #1.25
                                        \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                        \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    } {
                                        c'4 ~
                                        c'16
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \general-align
                        #Y
                        #-0.5
                        90.1
                    }

        ..  container:: example

            **Example 4.** Reference duration expressed as a tuplet:

            ::

                >>> markup = Tempo.make_tempo_equation_markup(Duration(1, 6), 90.1)
                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score \with {
                                    \override SpacingSpanner #'spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                } <<
                                    \new RhythmicStaff \with {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem #'direction = #up
                                        \override Stem #'length = #5
                                        \override TupletBracket #'bracket-visibility = ##t
                                        \override TupletBracket #'direction = #up
                                        \override TupletBracket #'padding = #1.25
                                        \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                        \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    } {
                                        \tweak #'edge-height #'(0.7 . 0)
                                        \times 2/3 {
                                            c'4
                                        }
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \general-align
                        #Y
                        #-0.5
                        90.1
                    }

        ..  container:: example

            **Example 5.** Reference duration passed in as explicit rhythm:

            ::

                >>> durations = [Duration(1, 16), Duration(3, 16), Duration(1, 16)]
                >>> selection = scoretools.make_notes([0], durations)
                >>> attach(Tie(), selection)
                >>> attach(Beam(), selection)
                >>> markup = Tempo.make_tempo_equation_markup(selection, 90.1)
                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score \with {
                                    \override SpacingSpanner #'spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                } <<
                                    \new RhythmicStaff \with {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem #'direction = #up
                                        \override Stem #'length = #5
                                        \override TupletBracket #'bracket-visibility = ##t
                                        \override TupletBracket #'direction = #up
                                        \override TupletBracket #'padding = #1.25
                                        \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                        \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    } {
                                        c'16 ~ [
                                        c'8. ~
                                        c'16 ]
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \general-align
                        #Y
                        #-0.5
                        90.1
                    }

            Pass rhythms like this as Abjad selections.

        Returns markup.
        '''
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        if isinstance(reference_duration, selectiontools.Selection):
            selection = reference_duration
        else:
            selection = scoretools.make_notes([0], [reference_duration])
        lhs_score_markup = durationtools.Duration._to_score_markup(selection)
        lhs_score_markup = lhs_score_markup.scale((0.75, 0.75))
        equal_markup = markuptools.Markup('=')
        rhs_markup = markuptools.Markup(units_per_minute)
        rhs_markup = rhs_markup.general_align('Y', -0.5)
        markup = lhs_score_markup + equal_markup + rhs_markup
        return markup

    def rewrite_duration(self, duration, new_tempo):
        r'''Rewrites `duration` under `new_tempo`.

        ..  container:: example

            **Example 1.** Consider the two tempo indicators below.

            ::

                >>> tempo = Tempo(Duration(1, 4), 60)
                >>> new_tempo = Tempo(Duration(1, 4), 90)

            `tempo` specifies quarter equal to ``60 MM``.

            `new_tempo` indication specifies quarter equal to ``90 MM``.

            `new_tempo` is ``3/2`` times as fast as `tempo`:

            ::

                >>> new_tempo / tempo
                Multiplier(3, 2)

            Note that a triplet eighth note under `tempo` equals a regular
            eighth note under `new_tempo`:

            ::

                >>> tempo.rewrite_duration(Duration(1, 12), new_tempo)
                Duration(1, 8)

            And note that a regular eighth note under `tempo` equals a dotted
            sixteenth under `new_tempo`:

            ::

                >>> tempo.rewrite_duration(Duration(1, 8), new_tempo)
                Duration(3, 16)

        Given `duration` governed by this tempo returns new duration governed
        by `new_tempo`.

        Ensures that `duration` and new duration consume the same amount of
        time in seconds.

        Returns duration.
        '''
        tempo_ratio = new_tempo / self
        new_duration = tempo_ratio * duration
        return new_duration