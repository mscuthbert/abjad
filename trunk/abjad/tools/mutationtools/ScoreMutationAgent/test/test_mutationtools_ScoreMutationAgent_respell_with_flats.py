# -*- encoding: utf-8 -*-
from abjad import *


def test_mutationtools_ScoreMutationAgent_respell_with_flats_01():

    note = Note(('cs', 4), 4)
    mutate(note).respell_with_flats()

    assert note.written_pitch == pitchtools.NamedPitch('df', 4)


def test_mutationtools_ScoreMutationAgent_respell_with_flats_02():

    chord = Chord([('cs', 4), ('f', 4), ('as', 4)], (1, 4))
    mutate(chord).respell_with_flats()

    assert chord.written_pitches == (
        pitchtools.NamedPitch('df', 4),
        pitchtools.NamedPitch('f', 4),
        pitchtools.NamedPitch('bf', 4),
        )


def test_mutationtools_ScoreMutationAgent_respell_with_flats_03():

    staff = Staff([Note(n, (1, 8)) for n in range(12, 0, -1)])
    mutate(staff).respell_with_flats()

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c''8
            b'8
            bf'8
            a'8
            af'8
            g'8
            gf'8
            f'8
            e'8
            ef'8
            d'8
            df'8
        }
        '''
        )
