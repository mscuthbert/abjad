# -*- encoding: utf-8 -*-
from abjad import *
import copy


def test_chordtools_Chord___copy___01():

    chord_1 = Chord("<ef' cs'' f''>4")
    chord_2 = copy.copy(chord_1)

    assert isinstance(chord_1, Chord)
    assert isinstance(chord_2, Chord)
    assert chord_1.lilypond_format == chord_2.lilypond_format
    assert chord_1 is not chord_2


def test_chordtools_Chord___copy___02():
    r'''Chord copies LilyPond duration multiplier.
    '''

    chord_1 = Chord("<ef' cs'' f''>4 * 1/2")
    chord_2 = copy.copy(chord_1)

    assert isinstance(chord_1, Chord)
    assert isinstance(chord_2, Chord)
    assert chord_1.lilypond_format == chord_2.lilypond_format
    assert chord_1 is not chord_2


def test_chordtools_Chord___copy___03():
    r'''Chord copies LilyPond grob overrides and LilyPond context settings.
    '''

    chord_1 = Chord("<ef' cs'' f''>4")
    chord_1.override.staff.note_head.color = 'red'
    chord_1.override.accidental.color = 'red'
    chord_1.set.tuplet_full_length = True
    chord_2 = copy.copy(chord_1)

    assert isinstance(chord_1, Chord)
    assert isinstance(chord_2, Chord)
    assert chord_1.lilypond_format == chord_2.lilypond_format
    assert chord_1 is not chord_2


def test_chordtools_Chord___copy___04():
    r'''Chord copies tweaked note heads.
    '''

    chord_1 = Chord("<c' e' g'>4")
    chord_1[0].tweak.color = 'red'
    chord_2 = copy.copy(chord_1)

    assert testtools.compare(
        chord_1,
        r'''
        <
            \tweak #'color #red
            c'
            e'
            g'
        >4
        '''
        )

    assert testtools.compare(
        chord_2,
        r'''
        <
            \tweak #'color #red
            c'
            e'
            g'
        >4
        '''
        )

    assert chord_2[0]._client is chord_2
    assert chord_2[1]._client is chord_2
    assert chord_2[2]._client is chord_2

    assert chord_1.lilypond_format == chord_2.lilypond_format
    assert chord_1 is not chord_2

    assert chord_1[0] == chord_2[0]
    assert chord_1[1] == chord_2[1]
    assert chord_1[2] == chord_2[2]

    assert chord_1[0] is not chord_2[0]
    assert chord_1[1] is not chord_2[1]
    assert chord_1[2] is not chord_2[2]


def test_chordtools_Chord___copy___05():
    r'''Chord coipes articulations and markup.
    '''

    chord_1 = Chord("<ef' cs'' f''>4")
    articulation_1 = marktools.Articulation('staccato')(chord_1)
    markup_1 = markuptools.Markup('foo', Up)(chord_1)

    chord_2 = copy.copy(chord_1)

    assert chord_1.lilypond_format == chord_2.lilypond_format
    assert chord_1 is not chord_2

    articulation_2 = inspect(chord_2).get_marks(marktools.Articulation)[0]
    assert articulation_1 == articulation_2
    assert articulation_1 is not articulation_2

    markup_2 = inspect(chord_2).get_markup()[0]
    assert markup_1 == markup_2
    assert markup_1 is not markup_2
