# -*- encoding: utf-8 -*-
import os
import subprocess
from experimental.tools.scoremanagertools.core.ScoreManagerObject import ScoreManagerObject


class ScoreManager(ScoreManagerObject):

    ### INITIALIZER ###

    def __init__(self, session=None):
        from experimental.tools import scoremanagertools
        ScoreManagerObject.__init__(self, session=session)
        self._segment_package_wrangler = scoremanagertools.wranglers.SegmentPackageWrangler(
            session=self._session)
        self._material_package_maker_wrangler = scoremanagertools.wranglers.MaterialPackageMakerWrangler(
            session=self._session)
        self._material_package_wrangler = scoremanagertools.wranglers.MaterialPackageWrangler(
            session=self._session)
        self._music_specifier_module_wrangler = scoremanagertools.wranglers.MusicSpecifierModuleWrangler(
            session=self._session)
        self._score_package_wrangler = scoremanagertools.wranglers.ScorePackageWrangler(
            session=self._session)
        self._stylesheet_file_wrangler = scoremanagertools.wranglers.StylesheetFileWrangler(
            session=self._session)

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if not isinstance(result, str):
            raise TypeError('result must be string.')
        if result == 'active':
            self._session.show_active_scores()
        elif result == 'all':
            self._session.show_all_scores()
        elif result == 'f':
            self.music_specifier_module_wrangler._run(
                rollback=True, head=self.configuration.built_in_specifiers_package_path)
        elif result == 'fix':
            self.score_package_wrangler.fix_visible_assets()
        elif result == 'k':
            self._io.print_not_yet_implemented()
        elif result == 'm':
            self.material_package_wrangler._run(
                rollback=True, head=self.configuration.built_in_materials_package_path)
        elif result == 'mb':
            self._session.show_mothballed_scores()
        elif result == 'new':
            self.score_package_wrangler.make_asset_interactively(rollback=True)
        elif result == 'profile':
            self.score_package_wrangler.profile_visible_assets()
        elif result == 'py.test':
            self.run_py_test_on_all_user_scores()
        elif result == 'svn':
            self.manage_svn()
        elif result in self.score_package_wrangler.list_visible_asset_packagesystem_paths():
            self.edit_score_interactively(result)

    def _make_main_menu(self):
        menu = self.make_score_selection_menu()
        section = menu.make_section()
        section.append(('m', 'materials'))
        section.append(('f', 'specifiers'))
        section.append(('k', 'sketches'))
        section.append(('new', 'new score'))
        hidden_section = menu.make_section(is_hidden=True)
        hidden_section.append(('active', 'show active scores only'))
        hidden_section.append(('all', 'show all scores'))
        hidden_section.append(('fix', 'fix all score package structures'))
        hidden_section.append(('mb', 'show mothballed scores only'))
        hidden_section.append(('profile', 'profile packages'))
        hidden_section.append(('py.test', 'run py.test on all scores'))
        hidden_section.append(('svn', 'work with repository'))
        return menu

    def _run(self, user_input=None, clear=True, cache=False):
        type(self).__init__(self)
        self._io.assign_user_input(user_input=user_input)
        self._session.cache_breadcrumbs(cache=cache)
        self._session.push_breadcrumb(self._breadcrumb)
        run_main_menu = True
        while True:
            self._session.push_breadcrumb(self.score_status_string)
            if run_main_menu:
                menu = self._make_main_menu()
                result = menu._run(clear=clear)
            else:
                run_main_menu = True
            if self._session.backtrack(source='home'):
                self._session.pop_breadcrumb()
                self._session.clean_up()
                break
            elif self._session.is_navigating_to_next_score:
                self._session.is_navigating_to_next_score = False
                self._session.is_backtracking_to_score_manager = False
                result = self.get_next_score_package_name()
            elif self._session.is_navigating_to_prev_score:
                self._session.is_navigating_to_prev_score = False
                self._session.is_backtracking_to_score_manager = False
                result = self.get_prev_score_package_name()
            elif not result:
                self._session.pop_breadcrumb()
                continue
            self._handle_main_menu_result(result)
            if self._session.backtrack(source='home'):
                self._session.pop_breadcrumb()
                self._session.clean_up()
                break
            elif self._session.is_navigating_to_sibling_score:
                run_main_menu = False
            self._session.pop_breadcrumb()
        self._session.pop_breadcrumb()
        self._session.restore_breadcrumbs(cache=cache)

    def _write_cache(self):
        cache_file_path = os.path.join(self.configuration.configuration_directory_path, 'cache.py')
        cache_file_pointer = file(cache_file_path, 'w')
        cache_file_pointer.write('start_menu_tokens = [\n')
        tokens = self.score_package_wrangler._make_menu_tokens()
        for token in tokens:
            cache_file_pointer.write('{},\n'.format(token))
        cache_file_pointer.write(']\n')
        cache_file_pointer.close()

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'scores'

    @property
    def material_package_maker_wrangler(self):
        return self._material_package_maker_wrangler

    @property
    def material_package_wrangler(self):
        return self._material_package_wrangler

    @property
    def music_specifier_module_wrangler(self):
        return self._music_specifier_module_wrangler

    @property
    def score_package_wrangler(self):
        return self._score_package_wrangler

    @property
    def score_status_string(self):
        return '{} scores'.format(self._session.scores_to_show)

    @property
    def segment_package_wrangler(self):
        return self._segment_package_wrangler

    @property
    def stylesheet_file_wrangler(self):
        return self._stylesheet_file_wrangler

    ### PUBLIC METHODS ###

    def edit_score_interactively(self, score_package_path):
        score_package_proxy = self.score_package_wrangler._initialize_asset_proxy(score_package_path)
        score_package_proxy._session.underscore_delimited_current_score_name = score_package_path
        score_package_proxy._run(cache=True)
        self._session.underscore_delimited_current_score_name = None

    def get_next_score_package_name(self):
        score_package_names = self.score_package_wrangler.list_asset_names()
        if self._session.underscore_delimited_current_score_name is None:
            return score_package_names[0]
        index = score_package_names.index(self._session.underscore_delimited_current_score_name)
        next_index = (index + 1) % len(score_package_names)
        return score_package_names[next_index]

    def get_prev_score_package_name(self):
        score_package_names = self.score_package_wrangler.list_asset_names()
        if self._session.underscore_delimited_current_score_name is None:
            return score_package_names[-1]
        index = score_package_names.index(self._session.underscore_delimited_current_score_name)
        prev_index = (index - 1) % len(score_package_names)
        return score_package_names[prev_index]

    def handle_svn_menu_result(self, result):
        '''Return true to exit the svn menu.
        '''
        this_result = False
        if result == 'add':
            self.score_package_wrangler.svn_add_assets()
        elif result == 'ci':
            self.score_package_wrangler.svn_ci_assets()
        elif result == 'st':
            self.score_package_wrangler.svn_st_assets()
        elif result == 'up':
            self.score_package_wrangler.svn_up_assets()
            return True
        return this_result

    def make_score_selection_menu(self):
        menu, section = self._io.make_menu(where=self._where, is_numbered=True, is_keyed=False)
        #section.tokens = self.score_package_wrangler._make_menu_tokens()
        if self._session.is_first_run:
            section.tokens = self.start_menu_tokens
            self._session.is_first_run = False
        else:
            section.tokens = self.score_package_wrangler._make_menu_tokens()
        return menu

    def make_svn_menu(self):
        menu, section = self._io.make_menu(where=self._where)
        section.append(('add', 'svn add scores'))
        section.append(('ci', 'svn commit scores'))
        section.append(('st', 'svn status scores'))
        section.append(('up', 'svn update scores'))
        return menu

    def manage_svn(self, clear=True):
        while True:
            self._session.push_breadcrumb('repository commands')
            menu = self.make_svn_menu()
            result = menu._run(clear=clear)
            if self._session.is_backtracking_to_score:
                self._session.is_backtracking_to_score = False
                self._session.pop_breadcrumb()
                continue
            elif self._session.backtrack():
                break
            self.handle_svn_menu_result(result)
            if self._session.backtrack():
                break
            self._session.pop_breadcrumb()
        self._session.pop_breadcrumb()

    def run_py_test_on_all_user_scores(self, prompt=True):
        command = 'py.test {}'.format(self.configuration.user_scores_directory_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        if lines:
            self._io.display(lines, capitalize_first_character=False)
        line = 'tests complete.'
        self._io.proceed(line, is_interactive=prompt)
