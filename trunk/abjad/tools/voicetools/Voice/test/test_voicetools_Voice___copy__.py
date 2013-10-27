# -*- encoding: utf-8 -*-
from abjad import *
import copy


def test_voicetools_Voice___copy___01():
    r'''Voices copy name, engraver removals, engraver consists,
    grob overrides and context settings. Voices do not copy musical
    content.
    '''

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_1.name = 'SopranoVoice'
    voice_1.engraver_removals.append('Forbid_line_break_engraver')
    voice_1.engraver_consists.append('Time_signature_engraver')
    voice_1.override.note_head.color = 'red'
    voice_1.set.tuplet_full_length = True

    r'''
    \context Voice = "SopranoVoice" \with {
        \remove Forbid_line_break_engraver
        \consists Time_signature_engraver
        \override NoteHead #'color = #red
        tupletFullLength = ##t
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    voice_2 = copy.copy(voice_1)

    r'''
    \context Voice = "SopranoVoice" \with {
        \remove Forbid_line_break_engraver
        \consists Time_signature_engraver
        \override NoteHead #'color = #red
        tupletFullLength = ##t
    } {
    }
    '''

    assert testtools.compare(
        voice_2,
        r'''
        \context Voice = "SopranoVoice" \with {
            \remove Forbid_line_break_engraver
            \consists Time_signature_engraver
            \override NoteHead #'color = #red
            tupletFullLength = ##t
        } {
        }
        '''
        )


def test_voicetools_Voice___copy___02():
    r'''Voice copies semanticity indicator.
    '''

    voice_1 = Voice("s8 s8 s8 s8")
    voice_1.name = 'SkipVoice'
    voice_1.is_nonsemantic = True

    r'''
    \context Voice = "SkipVoice" {
        s8
        s8
        s8
        s8
    }
    '''

    voice_2 = copy.copy(voice_1)

    r'''
    \context Voice = "SkipVoice" {
    }
    '''

    assert voice_2.is_nonsemantic
    assert testtools.compare(
        voice_2,
        r'''
        \context Voice = "SkipVoice" {
        }
        '''
        )
