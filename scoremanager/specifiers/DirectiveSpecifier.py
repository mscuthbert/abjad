# -*- encoding: utf-8 -*-
from scoremanager.specifiers.ParameterSpecifier \
    import ParameterSpecifier


class DirectiveSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(
        self,
        description=None,
        directive_handler_name=None,
        custom_identifier=None,
        source=None,
        ):
        ParameterSpecifier.__init__(
            self,
            description=description,
            custom_identifier=custom_identifier,
            source=source,
            )
        self.directive_handler_name = directive_handler_name

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        return self.custom_identifier or self.directive_handler_name