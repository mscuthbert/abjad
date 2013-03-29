from scf import selectors
from scf.wizards.HandlerCreationWizard import HandlerCreationWizard


class ArticulationHandlerCreationWizard(HandlerCreationWizard):

    ### CLASS ATTRIBUTES ###

    handler_class_name_selector = selectors.ArticulationHandlerClassNameSelector
    handler_editor_class_name_suffix = 'Editor'

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'articulation handler creation wizard'
