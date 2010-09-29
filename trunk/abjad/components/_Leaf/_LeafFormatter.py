from abjad.components._Component._ComponentFormatter import _ComponentFormatter
from abjad.components._Leaf._LeafFormatterNumberInterface import _LeafFormatterNumberInterface
from abjad.components._Leaf._LeafFormatterSlotsInterface import _LeafFormatterSlotsInterface
from abjad.tools.formattools._get_comment_contribution_for_slot import \
   _get_comment_contribution_for_slot
from abjad.tools.formattools._get_markup_format_contribution import \
   _get_markup_format_contribution


class _LeafFormatter(_ComponentFormatter):

   __slots__ = ('_number',)

   def __init__(self, client):
      _ComponentFormatter.__init__(self, client)
      self._number = _LeafFormatterNumberInterface(self)
      self._slots = _LeafFormatterSlotsInterface(self)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _agrace_body(self):
      result = [ ]
      #agrace = self._client.grace.after
      if hasattr(self._client, '_after_grace'):
         after_grace = self._client.after_grace
         if len(after_grace):
            result.append(after_grace.format)
      return result

   @property
   def _agrace_opening(self):
      result = [ ]
      if hasattr(self._client, '_after_grace'):
         #if len(self._client.grace.after):
         if len(self._client.after_grace):
            result.append(r'\afterGrace')
      return result

   @property
   def _grace_body(self):
      result = [ ]
      #grace = self._client.grace.before
      if hasattr(self._client, '_grace'):
         grace = self._client.grace
         if len(grace):
            result.append(grace.format)
      return result

   @property
   def _leaf_body(self):
      from abjad.tools.formattools._get_context_mark_format_contributions_for_slot import \
         _get_context_mark_format_contributions_for_slot
      from abjad.tools.formattools._get_left_slot_format_contributions import \
         _get_left_slot_format_contributions
      from abjad.tools.formattools._get_context_mark_format_contributions_for_slot import \
         _get_context_mark_format_contributions_for_slot
      from abjad.tools.formattools._get_right_slot_format_contributions import \
         _get_right_slot_format_contributions
      from abjad.tools.leaftools._get_left_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf import \
      _get_left_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf
      from abjad.tools.leaftools._get_right_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf import \
      _get_right_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf
      result = [ ]
      client = self._client
      spanners = client.spanners
      result.extend(
      _get_left_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf(
      self._client))
      result.extend(_get_left_slot_format_contributions(self._client))
      result.extend(self._nucleus)
      result.extend(self._tremolo_subdivision_contribution)
      result.extend(_get_right_slot_format_contributions(self._client))
      result.extend(_get_context_mark_format_contributions_for_slot(self._client, 'right'))
      result.extend(_get_markup_format_contribution(client))
      result.extend(
      _get_right_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf(
      self._client))
      result.extend(self._number_contribution)
      result.extend(_get_comment_contribution_for_slot(client, 'right'))
      return [' '.join(result)]

   @property
   def _nucleus(self):
      return self._client._body

   @property
   def _number_contribution(self):
      result = [ ]
      leaf = self._client
## FIXME ##
#      contribution = self.number._leaf_contribution
#      if contribution == 'markup':
#         result.append(r'^ \markup { %s }' % leaf.number)
#      elif contribution == 'comment':
#         result.append(r'%% leaf %s' % leaf.number)
      return result

   @property
   def _tremolo_subdivision_contribution(self):
      result = [ ]
      #subdivision = self._client.tremolo_subdivision
      subdivision = getattr(self._client, 'tremolo_subdivision', None)
      if subdivision:
         result.append(':%s' % subdivision) 
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def leaf(self):
      return self._client

   @property
   def number(self):
      return self._number

   @property
   def slots(self):
      return self._slots
