from abjad.core.abjadcore import _Abjad
from abjad.parentage.containment import _ContextContainmentSignature
from abjad.rational.rational import Rational
from abjad.receipt.parentage import _ParentageReceipt
import types


class _Parentage(_Abjad):

   def __init__(self, client):
      self._client = client
      self._parent = None

   ## PRIVATE ATTRIBUTES ##
   
   @property
   def _containment(self):
      '''Return _ContextContainmentSignature giving the root and
         first voice, staff and score in parentage of component.'''
      from abjad.score.score import Score
      from abjad.staff.staff import Staff
      from abjad.voice.voice import Voice
      containment = _ContextContainmentSignature( )
      found_voice, found_staff, found_score = False, False, False
      for component in self.parentage:
         '''Voices can be named the same to compare equally.'''
         if isinstance(component, Voice) and not found_voice:
            containment.voice = component._ID
            found_voice = True
         '''Staves must be manifestly equal to compare True.'''
         if isinstance(component, Staff) and not found_staff:
            containment.staff = id(component)
            found_staff = True
         '''Scores must be manifestly equal to compare True.'''
         if isinstance(component, Score) and not found_score:
            containment.score = id(component)
            found_score = True
      else:
         '''Root components must be manifestly equal to compare True.'''
         containment.root = id(component)
      return containment

   @property
   def _governor(self):
      '''Return reference to first sequential container Q 
         in the parentage of client such that 
         the parent of Q is either a parallel container or None.
         In the case that no such sequential container exists
         in the parentage of client, return None.'''
      from abjad.container.container import Container
      for component in self.parentage:
         if isinstance(component, Container) and not component.parallel:
            parent = component.parentage.parent
            if parent is None:
               return component
            if isinstance(parent, Container) and parent.parallel:
               return component
            
   @property
   def _threadParentage(self):
      '''Return thread-pertinent parentage structure.
         Same as parentage but with _Tuplets, redundant Sequentials, 
         Parallels and tautologies (unlikely) removed.'''
      from abjad.container.parallel import Parallel
      from abjad.container.sequential import Sequential
      from abjad.context.context import _Context
      from abjad.tuplet.tuplet import _Tuplet
      parentage = self.parentage[1:]
      if len(parentage) > 0:
      ## remove sequentials
         for p in parentage[:]:
            if isinstance(p, (Sequential, _Tuplet)):
               parentage.remove(p)
            else:
               break
      # remove tautological nesting
         for i, p in enumerate(parentage[:-1]):
            if type(p) == type(parentage[i+1]):
               if isinstance(p, Parallel):
                  parentage.remove(p)
               elif isinstance(p, _Context):
                  if p.invocation == parentage[i+1].invocation:
                     parentage.remove(p)
      return parentage

   ## PRIVATE METHODS ##

   def _cutOutgoingReferenceToParent(self):
      '''Keep incoming reference from parent to client in tact.
         Sever ougoing reference from parent to client.
         Parent will continue to reference client.
         Client will no longer reference parent.
         Return parent.'''
      parent = self.parent
      if parent is not None:
         self.parent = None
         return parent

   def _detach(self):
      '''Sever incoming reference from parent to client.
         Sever outgoing reference from client to parent.'''
      client = self._client
      client._update._markForUpdateToRoot( )
      parent, index = self._removeFromParent( )
      self._cutOutgoingReferenceToParent( )
      receipt = _ParentageReceipt(client, parent, index)
      return receipt

   def _first(self, klass):
      '''Return first instance of klass in score tree above client.'''
      for component in self.parentage[1:]:
         if isinstance(component, klass):
            return component

   def _reattach(self, receipt):
      '''Reattach client to parent described in receipt.
         Empty receipt and return client.'''
      client = self._client
      assert client is receipt._component
      parent = receipt._parent
      index = receipt._index
      parent._music.insert(index, client)
      self.parent = parent
      receipt._empty( )
      return client

   def _removeFromParent(self):
      '''Sever incoming reference from parent to client.
         Leave outgoing reference from client to parent in tact.
         Parent will no longer reference client.
         Client will continue to reference parent.'''
      client = self._client
      parent = self.parent
      if parent is not None:
         index = parent.index(client)
         parent._music.remove(client)
         return parent, index
      return None, None

   def _splice(self, components):
      '''Insert components immediately after self in parent.
         Do not handle spanners.'''
      if self.parent is not None:
         client = self._client
         index = self.parent.index(client) + 1
         self.parent[index:index] = components
         return [client] + components

   def _switchParentTo(self, new_parent):
      '''Remove client from parent and give client to new_parent.'''
      client = self._client
      cur_parent = self.parent
      if cur_parent is not None:
         cur_parent._music.remove(client)
      self.parent = new_parent

   ## PUBLIC ATTRIBUTES ##

   @property
   def depth(self):
      '''Absolute depth of component in Abjad expression.'''
      return len(self.parentage) - 1

   @property
   def layer(self):
      '''Layer of leaf in nested tuplet.'''
      from abjad.tuplet.tuplet import _Tuplet
      result = 0
      for parent in self.parentage[1:]:
         if isinstance(parent, _Tuplet):
            result += 1
      return result

   @property
   def orphan(self):
      '''True when component has no parent, otherwise False.'''
      return len(self.parentage) == 1

   @apply
   def parent( ):
      '''Return reference to parent of client, else None.'''
      def fget(self):
         return self._parent
      def fset(self, arg):
         ## TODO: Include asserts
         self._parent = arg
      
   @property
   def parentage(self):
      '''Return a list of all of elements in the
         parentage of client, including client.'''
      result = [ ]
      cur = self._client
      while cur is not None:
         result.append(cur)
         cur = cur.parentage.parent
      return result

   @property
   def root(self):
      '''Return reference to component at depth 0 of Abjad expression.'''
      return self.parentage[-1]
