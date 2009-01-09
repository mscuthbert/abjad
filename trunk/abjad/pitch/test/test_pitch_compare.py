from abjad import *
from py.test import raises


def test_pitch_compare_01( ):
   '''Referentially equal pitches compare equally.'''
   p1 = Pitch('fs', 4)
   assert     p1 == p1
   assert not p1 != p1
   assert not p1 >  p1
   assert     p1 >= p1
   assert not p1 <  p1
   assert     p1 <= p1


def test_pitch_compare_02( ):
   '''Pitches equal by name, accidental and octave compare equally.'''
   p1, p2 = Pitch('fs', 4), Pitch('fs', 4)
   assert     p1 == p2
   assert not p1 != p2
   assert not p1 >  p1
   assert     p1 >= p1
   assert not p1 <  p1
   assert     p1 <= p1


def test_pitch_compare_03( ):
   '''Pitches enharmonically equal compare unequally.'''
   p1, p2 = Pitch('fs', 4), Pitch('gf', 4)
   assert not p1 == p2
   assert     p1 != p2
   assert not p1 >  p2
   assert not p1 >= p2
   assert     p1 <  p2
   assert     p1 <= p2


def test_pitch_compare_04( ):
   '''Pitches manifestly different compare unequally.'''
   p1, p2 = Pitch('f', 4), Pitch('g', 4)
   assert not p1 == p2
   assert     p1 != p2
   assert not p1 >  p2
   assert not p1 >= p2
   assert     p1 <  p2
   assert     p1 <= p2


def test_pitch_compare_05( ):
   '''Pitches typographically crossed compare unequally.'''
   p1, p2 = Pitch('fss', 4), Pitch('gff', 4)
   assert not p1 == p2
   assert     p1 != p2
   assert not p1 >  p2
   assert not p1 >= p2
   assert     p1 <  p2
   assert     p1 <= p2
