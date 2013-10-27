# -*- encoding: utf-8 -*-
import py
from abjad import *


def test_mutationtools_ScoreMutationAgent_split_01():
    r'''Cyclically split note in score. Don't fracture spanners.
    '''

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    notes = staff[0][1:2]
    result = mutate(notes).split(
        [Duration(3, 64)],
        cyclic=True,
        fracture_spanners=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'32. ~
                d'32. ~
                d'32 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 3


def test_mutationtools_ScoreMutationAgent_split_02():
    r'''Cyclically split consecutive notes in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    leaves = staff.select_leaves()
    result = mutate(leaves).split(
        [Duration(3, 32)], 
        cyclic=True,
        fracture_spanners=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'16. [ ( ~
                c'32
                d'16 ~
                d'16 ]
            }
            {
                e'32 [ ~
                e'16.
                f'16. ~
                f'32 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 6


def test_mutationtools_ScoreMutationAgent_split_03():
    r'''Cyclically split measure in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=False, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ (
            }
            {
                c'32
                d'16
            }
            {
                \time 2/32
                d'16 ]
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 3


def test_mutationtools_ScoreMutationAgent_split_04():
    r'''Cyclically split consecutive measures in score. 
    Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    measures = staff[:]
    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=False, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ (
            }
            {
                c'32
                d'16
            }
            {
                \time 2/32
                d'16 ]
            }
            {
                \time 1/32
                e'32 [
            }
            {
                \time 3/32
                e'16.
            }
            {
                f'16.
            }
            {
                \time 1/32
                f'32 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 6


def test_mutationtools_ScoreMutationAgent_split_05():
    r'''Cyclically split orphan measures. Don't fracture spanners.
    '''

    measures = [Measure((2, 8), "c'8 d'8"), Measure((2, 8), "e'8 f'8")]
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([measures[0]])
    beam_2.attach([measures[1]])

    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=False, 
        tie_split_notes=False,
        )

    music = sequencetools.flatten_sequence(result)
    staff = Staff(music)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [
            }
            {
                c'32
                d'16
            }
            {
                \time 2/32
                d'16 ]
            }
            {
                \time 1/32
                e'32 [
            }
            {
                \time 3/32
                e'16.
            }
            {
                f'16.
            }
            {
                \time 1/32
                f'32 ]
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 6


def test_mutationtools_ScoreMutationAgent_split_06():
    r'''Cyclically split note in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    notes = staff[0][1:]
    result = mutate(notes).split(
        [Duration(1, 32)],
        cyclic=True, 
        fracture_spanners=False, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'32 ~
                d'32 ~
                d'32 ~
                d'32 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 4


def test_mutationtools_ScoreMutationAgent_split_07():
    r'''Cyclically split consecutive notes in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    leaves = staff.select_leaves()
    result = mutate(leaves).split(
        [Duration(1, 16)],
        cyclic=True, 
        fracture_spanners=False, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'16 [ ( ~
                c'16
                d'16 ~
                d'16 ]
            }
            {
                e'16 [ ~
                e'16
                f'16 ~
                f'16 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 8


def test_mutationtools_ScoreMutationAgent_split_08():
    r'''Cyclically split measure in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(1, 16)],
        cyclic=True, 
        fracture_spanners=False, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/16
                c'16 [ ( ~
            }
            {
                c'16
            }
            {
                d'16 ~
            }
            {
                d'16 ]
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 4


def test_mutationtools_ScoreMutationAgent_split_09():
    r'''Cyclically split consecutive measures in score. 
    Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    measures = staff[:]
    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=False, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ ( ~
            }
            {
                c'32
                d'16 ~
            }
            {
                \time 2/32
                d'16 ]
            }
            {
                \time 1/32
                e'32 [ ~
            }
            {
                \time 3/32
                e'16.
            }
            {
                f'16. ~
            }
            {
                \time 1/32
                f'32 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 6


def test_mutationtools_ScoreMutationAgent_split_10():
    r'''Cyclically split note in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    notes = staff[0][1:2]
    result = mutate(notes).split(
        [Duration(3, 64)], 
        cyclic=True,
        fracture_spanners=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'32. ) ~
                d'32. ( ) ~
                d'32 ] (
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 3


def test_mutationtools_ScoreMutationAgent_split_11():
    r'''Cyclically split consecutive notes in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    leaves = staff.select_leaves()
    result = mutate(leaves).split(
        [Duration(3, 32)], 
        cyclic=True, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'16. [ ( ) ~
                c'32 (
                d'16 ) ~
                d'16 ] (
            }
            {
                e'32 [ ) ~
                e'16. (
                f'16. ) ~
                f'32 ] ( )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 6


def test_mutationtools_ScoreMutationAgent_split_12():
    r'''Cyclically split measure in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=True, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ ] ( )
            }
            {
                c'32 [ (
                d'16 ] )
            }
            {
                \time 2/32
                d'16 [ ] (
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 3


def test_mutationtools_ScoreMutationAgent_split_13():
    r'''Cyclically split consecutive measures in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    measures = staff[:]
    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=True, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ ] ( )
            }
            {
                c'32 [ (
                d'16 ] )
            }
            {
                \time 2/32
                d'16 [ ] (
            }
            {
                \time 1/32
                e'32 [ ] )
            }
            {
                \time 3/32
                e'16. [ ] ( )
            }
            {
                f'16. [ ] ( )
            }
            {
                \time 1/32
                f'32 [ ] ( )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 6


def test_mutationtools_ScoreMutationAgent_split_14():
    r'''Cyclically split orphan notes.
    '''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]

    result = mutate(notes).split(
        [Duration(3, 32)], 
        cyclic=True, 
        fracture_spanners=True,
        )

    music = sequencetools.flatten_sequence(result)
    staff = Staff(music)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'16. ~
            c'32
            d'16 ~
            d'16
            e'32 ~
            e'16.
            f'16. ~
            f'32
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 6


def test_mutationtools_ScoreMutationAgent_split_15():
    r'''Cyclically split orphan measures. Fracture spanners.
    '''

    measures = [Measure((2, 8), "c'8 d'8"), Measure((2, 8), "e'8 f'8")]
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([measures[0]])
    beam_2.attach([measures[1]])

    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=True, 
        tie_split_notes=False,
        )

    music = sequencetools.flatten_sequence(result)
    staff = Staff(music)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ ]
            }
            {
                c'32 [
                d'16 ]
            }
            {
                \time 2/32
                d'16 [ ]
            }
            {
                \time 1/32
                e'32 [ ]
            }
            {
                \time 3/32
                e'16. [ ]
            }
            {
                f'16. [ ]
            }
            {
                \time 1/32
                f'32 [ ]
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 6


def test_mutationtools_ScoreMutationAgent_split_16():
    r'''Cyclically split note in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    notes = staff[0][1:]
    result = mutate(notes).split(
        [Duration(1, 32)],
        cyclic=True, 
        fracture_spanners=True, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'32 ) ~
                d'32 ( ) ~
                d'32 ( ) ~
                d'32 ] (
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 4


def test_mutationtools_ScoreMutationAgent_split_17():
    r'''Cyclically split consecutive notes in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    leaves = staff.select_leaves()
    result = mutate(leaves).split(
        [Duration(1, 16)],
        cyclic=True, 
        fracture_spanners=True, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'16 [ ( ) ~
                c'16 (
                d'16 ) ~
                d'16 ] (
            }
            {
                e'16 [ ) ~
                e'16 (
                f'16 ) ~
                f'16 ] ( )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 8


def test_mutationtools_ScoreMutationAgent_split_18():
    r'''Cyclically split measure in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(1, 16)],
        cyclic=True, 
        fracture_spanners=True, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/16
                c'16 [ ] ( ) ~
            }
            {
                c'16 [ ] ( )
            }
            {
                d'16 [ ] ( ) ~
            }
            {
                d'16 [ ] (
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 4


def test_mutationtools_ScoreMutationAgent_split_19():
    r'''Cyclically split consecutive measures in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    measures = staff[:]
    result = mutate(measures).split(
        [Duration(3, 32)],
        cyclic=True, 
        fracture_spanners=True, 
        tie_split_notes=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/32
                c'16. [ ] ( ) ~
            }
            {
                c'32 [ (
                d'16 ] ) ~
            }
            {
                \time 2/32
                d'16 [ ] (
            }
            {
                \time 1/32
                e'32 [ ] ) ~
            }
            {
                \time 3/32
                e'16. [ ] ( )
            }
            {
                f'16. [ ] ( ) ~
            }
            {
                \time 1/32
                f'32 [ ] ( )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 6


def test_mutationtools_ScoreMutationAgent_split_20():
    r'''Force split measure in score. Do not fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(1, 32), Duration(3, 32), Duration(5, 32)],
        cyclic=False, 
        fracture_spanners=False, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/32
                c'32 [ (
            }
            {
                \time 3/32
                c'16.
            }
            {
                \time 4/32
                d'8 ]
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 3


def test_mutationtools_ScoreMutationAgent_split_21():
    r'''Force split consecutive measures in score. Do not fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    measures = staff[:]
    result = mutate(measures).split(
        [Duration(1, 32), Duration(3, 32), Duration(5, 32)],
        cyclic=False, 
        fracture_spanners=False, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/32
                c'32 [ (
            }
            {
                \time 3/32
                c'16.
            }
            {
                \time 4/32
                d'8 ]
            }
            {
                \time 1/32
                e'32 [
            }
            {
                \time 7/32
                e'16.
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 4


def test_mutationtools_ScoreMutationAgent_split_22():
    r'''Force split measure in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(1, 32), Duration(3, 32), Duration(5, 32)],
        cyclic=False, 
        fracture_spanners=True, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/32
                c'32 [ ] ( )
            }
            {
                \time 3/32
                c'16. [ ] ( )
            }
            {
                \time 4/32
                d'8 [ ] (
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 3


def test_mutationtools_ScoreMutationAgent_split_23():
    r'''Force split consecutive measures in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam_1 = spannertools.BeamSpanner()
    beam_2 = spannertools.BeamSpanner()
    beam_1.attach([staff[0]])
    beam_2.attach([staff[1]])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    measures = staff[:]
    result = mutate(measures).split(
        [Duration(1, 32), Duration(3, 32), Duration(5, 32)],
        cyclic=False, 
        fracture_spanners=True, 
        tie_split_notes=False)

    assert inspect(staff).is_well_formed()
    assert len(result) == 4
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/32
                c'32 [ ] ( )
            }
            {
                \time 3/32
                c'16. [ ] ( )
            }
            {
                \time 4/32
                d'8 [ ] (
            }
            {
                \time 1/32
                e'32 [ ] )
            }
            {
                \time 7/32
                e'16. [ (
                f'8 ] )
            }
        }
        '''
        )


def test_mutationtools_ScoreMutationAgent_split_24():
    r'''Force split orphan note. Offsets sum to less than note duration.
    '''

    note = Note("c'4")
    note = select(note)

    result = mutate(note).split(
        [(1, 32), (5, 32)],
        cyclic=False, 
        fracture_spanners=True, 
        tie_split_notes=False,
        )

    notes = sequencetools.flatten_sequence(result)
    staff = Staff(notes)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'32
            c'8 ~
            c'32
            c'16
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 3


def test_mutationtools_ScoreMutationAgent_split_25():
    r'''Force split note in score. Fracture spanners.
    '''

    staff = Staff("c'8 [ ]")

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [ ]
        }
        '''
        )

    notes = staff[:]
    result = mutate(notes).split(
        [Duration(1, 64), Duration(5, 64)],
        cyclic=False, 
        fracture_spanners=True, 
        tie_split_notes=False,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'64 [ ]
            c'16 [ ~
            c'64 ]
            c'32 [ ]
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_mutationtools_ScoreMutationAgent_split_26():
    r'''Split tuplet in score and do not fracture spanners.
    '''

    voice = Voice()
    voice.append(Tuplet((2, 3), "c'8 d'8 e'8"))
    voice.append(Tuplet((2, 3), "f'8 g'8 a'8"))
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])

    tuplets = voice[1:2]
    result = mutate(tuplets).split(
        [Duration(1, 12)],
        fracture_spanners=False,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                f'8
            }
            \times 2/3 {
                g'8
                a'8 ]
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_split_27():
    r'''Split in-score measure with power-of-two denominator and 
    do not fracture spanners.
    '''

    voice = Voice()
    voice.append(Measure((3, 8), "c'8 d'8 e'8"))
    voice.append(Measure((3, 8), "f'8 g'8 a'8"))
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])

    measures = voice[1:2]
    result = mutate(measures).split(
        [Duration(1, 8)], 
        fracture_spanners=False,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 3/8
                c'8 [
                d'8
                e'8
            }
            {
                \time 1/8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8 ]
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_split_28():
    r'''Split in-score measure without power-of-two denominator 
    and do not frature spanners.
    '''

    voice = Voice()
    voice.append(Measure((3, 9), "c'8 d'8 e'8"))
    voice.append(Measure((3, 9), "f'8 g'8 a'8"))
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])

    measures = voice[1:2]
    result = mutate(measures).split(
        [Duration(1, 9)], 
        fracture_spanners=False,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 3/9
                \scaleDurations #'(8 . 9) {
                    c'8 [
                    d'8
                    e'8
                }
            }
            {
                \time 1/9
                \scaleDurations #'(8 . 9) {
                    f'8
                }
            }
            {
                \time 2/9
                \scaleDurations #'(8 . 9) {
                    g'8
                    a'8 ]
                }
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_split_29():
    r'''A single container can be split in the middle.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")

    result = mutate([voice]).split(
        [Duration(1, 4)], 
        fracture_spanners=False,
        )

    assert inspect(voice).is_well_formed()

    voice_1 = result[0][0]
    voice_2 = result[1][0]

    assert testtools.compare(
        voice_1,
        r'''
        \new Voice {
            c'8
            d'8
        }
        '''
        )

    assert inspect(voice_1).is_well_formed()

    assert testtools.compare(
        voice_2,
        r'''
        \new Voice {
            e'8
            f'8
        }
        '''
        )

    assert inspect(voice_2).is_well_formed()


def test_mutationtools_ScoreMutationAgent_split_30():
    r'''Split voice at negative index.
    '''

    staff = Staff([Voice("c'8 d'8 e'8 f'8")])
    voice = staff[0]

    result = mutate([voice]).split(
        [Duration(1, 4)],
        fracture_spanners=False,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        left,
        r'''
        \new Voice {
            c'8
            d'8
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        \new Voice {
            e'8
            f'8
        }
        '''
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
        }
        '''
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \new Voice {
                c'8
                d'8
            }
            \new Voice {
                e'8
                f'8
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_mutationtools_ScoreMutationAgent_split_31():
    r'''Slpit container in score and do not fracture spanners.
    '''

    staff = Staff([Container("c'8 d'8 e'8 f'8")])
    voice = staff[0]
    beam = spannertools.BeamSpanner()
    beam.attach(voice)

    result = mutate([voice]).split(
        [Duration(1, 4)],
        fracture_spanners=False,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8 ]
            }
        }
        '''
        )

    assert testtools.compare(
        left,
        r'''
        {
            c'8 [
            d'8
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        {
            e'8
            f'8 ]
        }
        '''
        )

    assert testtools.compare(
        voice,
        r'''
        {
        }
        '''
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8 ]
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_mutationtools_ScoreMutationAgent_split_32():
    r'''Split tuplet in score and do not fracture spanners.
    '''

    tuplet = Tuplet((4, 5), "c'8 c'8 c'8 c'8 c'8")
    voice = Voice([tuplet])
    staff = Staff([voice])
    beam = spannertools.BeamSpanner()
    beam.attach(tuplet)

    result = mutate([tuplet]).split(
        [Duration(1, 5)],
        fracture_spanners=False,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \new Voice {
                \times 4/5 {
                    c'8 [
                    c'8
                }
                \times 4/5 {
                    c'8
                    c'8
                    c'8 ]
                }
            }
        }
        '''
        )

    assert testtools.compare(
        left,
        r'''
        \times 4/5 {
            c'8 [
            c'8
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        \times 4/5 {
            c'8
            c'8
            c'8 ]
        }
        '''
        )

    assert testtools.compare(
        tuplet,
        r'''
        \times 4/5 {
        }
        '''
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 4/5 {
                c'8 [
                c'8
            }
            \times 4/5 {
                c'8
                c'8
                c'8 ]
            }
        }
        '''
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \new Voice {
                \times 4/5 {
                    c'8 [
                    c'8
                }
                \times 4/5 {
                    c'8
                    c'8
                    c'8 ]
                }
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_mutationtools_ScoreMutationAgent_split_33():
    r'''Split triplet, and fracture spanners.
    '''

    voice = Voice()
    voice.append(Tuplet((2, 3), "c'8 d'8 e'8"))
    voice.append(Tuplet((2, 3), "f'8 g'8 a'8"))
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])
    tuplet = voice[1]

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                g'8
                a'8 ]
            }
        }
        '''
        )

    result = mutate([tuplet]).split(
        [Duration(1, 12)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        left,
        r'''
        \times 2/3 {
            f'8 ]
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        \times 2/3 {
            g'8 [
            a'8 ]
        }
        '''
        )

    assert tuplet.lilypond_format == '\\times 2/3 {\n}'

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                f'8 ]
            }
            \times 2/3 {
                g'8 [
                a'8 ]
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_split_34():
    r'''Split measure with power-of-two time signature denominator.
    Fracture spanners.
    '''

    voice = Voice()
    voice.append(Measure((3, 8), "c'8 d'8 e'8"))
    voice.append(Measure((3, 8), "f'8 g'8 a'8"))
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])
    measure = voice[1]

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 3/8
                c'8 [
                d'8
                e'8
            }
            {
                f'8
                g'8
                a'8 ]
            }
        }
        '''
        )

    result = mutate([measure]).split(
        [Duration(1, 8)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        left,
        r'''
        {
            \time 1/8
            f'8 ]
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        {
            \time 2/8
            g'8 [
            a'8 ]
        }
        '''
        )

    assert py.test.raises(UnderfullContainerError, 'measure.lilypond_format')

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 3/8
                c'8 [
                d'8
                e'8
            }
            {
                \time 1/8
                f'8 ]
            }
            {
                \time 2/8
                g'8 [
                a'8 ]
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_split_35():
    r'''Split measure without power-of-two time signature denominator.
    Fracture spanners.
    '''

    voice = Voice()
    voice.append(Measure((3, 9), "c'8 d'8 e'8"))
    voice.append(Measure((3, 9), "f'8 g'8 a'8"))
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])
    measure = voice[1]

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 3/9
                \scaleDurations #'(8 . 9) {
                    c'8 [
                    d'8
                    e'8
                }
            }
            {
                \scaleDurations #'(8 . 9) {
                    f'8
                    g'8
                    a'8 ]
                }
            }
        }
        '''
        )

    result = mutate([measure]).split(
        [Duration(1, 9)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        left,
        r'''
        {
            \time 1/9
            \scaleDurations #'(8 . 9) {
                f'8 ]
            }
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        {
            \time 2/9
            \scaleDurations #'(8 . 9) {
                g'8 [
                a'8 ]
            }
        }
        '''
        )

    assert py.test.raises(UnderfullContainerError, 'measure.lilypond_format')

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 3/9
                \scaleDurations #'(8 . 9) {
                    c'8 [
                    d'8
                    e'8
                }
            }
            {
                \time 1/9
                \scaleDurations #'(8 . 9) {
                    f'8 ]
                }
            }
            {
                \time 2/9
                \scaleDurations #'(8 . 9) {
                    g'8 [
                    a'8 ]
                }
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_split_36():
    r'''Split voice outside of score.
    Fracture spanners.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )

    result = mutate([voice]).split(
        [Duration(1, 4)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        left,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        \new Voice {
            e'8 [
            f'8 ]
        }
        '''
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
        }
        '''
        )


def test_mutationtools_ScoreMutationAgent_split_37():
    r'''Split measure in score and fracture spanners.
    '''

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    beam = spannertools.BeamSpanner()
    beam.attach(staff[0])
    beam = spannertools.BeamSpanner()
    beam.attach(staff[1])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(1, 8)],
        fracture_spanners=True,
        )

    left = result[0][0]
    right = result[1][0]

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/8
                c'8 [ ] ( )
            }
            {
                d'8 [ ] (
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_mutationtools_ScoreMutationAgent_split_38():
    r'''Split in-score measure with power-of-two time signature denominator.
    Fractured spanners but do not tie over split locus.
    Measure contents necessitate denominator change.
    '''

    staff = Staff([Measure((3, 8), "c'8. d'8.")])
    beam = spannertools.BeamSpanner()
    beam.attach(staff[0])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/8
                c'8. [ (
                d'8. ] )
            }
        }
        '''
        )

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(3, 16)],
        fracture_spanners=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/16
                c'8. [ ] ( )
            }
            {
                d'8. [ ] ( )
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 2


def test_mutationtools_ScoreMutationAgent_split_39():
    r'''Split cyclic.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    beam = spannertools.BeamSpanner()
    beam.attach(voice[0])
    slur = spannertools.SlurSpanner()
    slur.attach(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    note = voice[0]
    result = mutate(note).split(
        [Duration(1, 8), Duration(3, 8)],
        cyclic=True, 
        fracture_spanners=False,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
            }
            {
                d'8
                e'8
                f'8
            }
            {
                g'8
            }
            {
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_split_40():
    r'''Cyclic 1 splits all elements in container.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    beam = spannertools.BeamSpanner()
    beam.attach(voice[0])
    slur = spannertools.SlurSpanner()
    slur.attach(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    container = voice[0]
    result = mutate(container).split(
        [Duration(1, 8)],
        cyclic=True, 
        fracture_spanners=False,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
            }
            {
                d'8
            }
            {
                e'8
            }
            {
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_split_41():
    r'''Split cyclic.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    beam = spannertools.BeamSpanner()
    beam.attach(voice[0])
    slur = spannertools.SlurSpanner()
    slur.attach(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    container = voice[0]
    result = mutate(container).split(
        [Duration(1, 8), Duration(3, 8)],
        cyclic=True, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ ] ( )
            }
            {
                d'8 [ (
                e'8
                f'8 ] )
            }
            {
                g'8 [ ] ( )
            }
            {
                a'8 [ (
                b'8
                c''8 ] )
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()
    assert len(result) == 4


def test_mutationtools_ScoreMutationAgent_split_42():
    r'''Cyclic by 1 splits all elements in container.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    beam = spannertools.BeamSpanner()
    beam.attach(voice[0])
    slur = spannertools.SlurSpanner()
    slur.attach(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    container = voice[0]
    result = mutate(container).split(
        [Duration(1, 8)],
        cyclic=True, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ ] ( )
            }
            {
                d'8 [ ] ( )
            }
            {
                e'8 [ ] ( )
            }
            {
                f'8 [ ] ( )
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()
    assert len(result) == 4


def test_mutationtools_ScoreMutationAgent_split_43():
    r'''Extra durations are ignored.
    Result contains no empty shards.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    beam = spannertools.BeamSpanner()
    beam.attach(voice[0])
    slur = spannertools.SlurSpanner()
    slur.attach(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    container = voice[0]
    result = mutate(container).split(
        5 * [Duration(2, 8)],
        cyclic=True, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8 ] )
            }
            {
                e'8 [ (
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()
    assert len(result) == 2


def test_mutationtools_ScoreMutationAgent_split_44():
    r'''Empty durations list.
    Expression remains unaltered.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    beam = spannertools.BeamSpanner()
    beam.attach(voice[0])
    slur = spannertools.SlurSpanner()
    slur.attach(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    container = voice[0]
    result = mutate(container).split(
        [], 
        cyclic=True, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()
    assert len(result) == 1


def test_mutationtools_ScoreMutationAgent_split_45():
    r'''Split one time.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    beam = spannertools.BeamSpanner()
    beam.attach(voice[0])
    slur = spannertools.SlurSpanner()
    slur.attach(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    container = voice[0]
    result = mutate(container).split(
        [Duration(1, 8), Duration(3, 8)],
        cyclic=False, 
        fracture_spanners=False,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
            }
            {
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()
    assert len(result) == 3


def test_mutationtools_ScoreMutationAgent_split_46():
    r'''Split one time.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    beam = spannertools.BeamSpanner()
    beam.attach(voice[0])
    slur = spannertools.SlurSpanner()
    slur.attach(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    container = voice[0]
    result = mutate(container).split(
        [Duration(1, 8), Duration(3, 8)],
        cyclic=False, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ ] ( )
            }
            {
                d'8 [ (
                e'8
                f'8 ] )
            }
            {
                g'8 [ (
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()
    assert len(result) == 3


def test_mutationtools_ScoreMutationAgent_split_47():
    r'''Extra durations are ignored.
    Result contains no empty shards.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    beam = spannertools.BeamSpanner()
    beam.attach(voice[0])
    slur = spannertools.SlurSpanner()
    slur.attach(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    container = voice[0]
    result = mutate(container).split(
        5 * [Duration(2, 8)],
        cyclic=False, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8 ] )
            }
            {
                e'8 [ (
                f'8 ] )
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()
    assert len(result) == 2


def test_mutationtools_ScoreMutationAgent_split_48():
    r'''Split leaf at relative offset that is both non-assignable
    and non-power-of-two.
    '''

    staff = Staff("c'4")

    notes = staff[:1]
    result = mutate(notes).split(
        [Duration(5, 24)],
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \times 2/3 {
                c'4 ~
                c'16 ~
            }
            \times 2/3 {
                c'16
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()


# container._split_at_index() works here;
# componenttools.split() doesn't work here.
# eventually make componenttools.split() work here.
def test_mutationtools_ScoreMutationAgent_split_49():
    r'''Split in-score measure without power-of-two time 
    signature denominator. Fractured spanners but do not tie 
    over split locus. Measure contents necessitate denominator change.
    '''
    py.test.skip('TODO: make this work.')

    staff = Staff([Measure((3, 12), "c'8. d'8.")])
    beam = spannertools.BeamSpanner()
    beam.attach(staff[0])
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/12
                \scaleDurations #'(2 . 3) {
                    c'8. [ (
                    d'8. ] )
                }
            }
        }
        '''
        )

    measures = staff[:1]
    result = mutate(measures).split(
        [Duration(3, 24)],
        fracture_spanners=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/24
                \scaleDurations #'(2 . 3) {
                    c'8. [ ] (
                }
            }
            {
                \scaleDurations #'(2 . 3) {
                    d'8. [ ] )
                }
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 2
