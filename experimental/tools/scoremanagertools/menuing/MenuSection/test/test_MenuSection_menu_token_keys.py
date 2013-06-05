from experimental import *


def test_MenuSection_menu_token_keys_01():
    '''Menu entry keys equal none when menu entry menu_tokens are strings.
    True whether section is numbered or not.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = ['apple', 'banana', 'cherry']
    section = menu.make_section(menu_tokens=menu_tokens, is_keyed=False)
    section.title = 'section'
    assert not section.is_numbered
    assert section.menu_token_keys == [None, None, None]

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = ['apple', 'banana', 'cherry']
    section = menu.make_section(is_numbered=True, menu_tokens=menu_tokens, is_keyed=False)
    section.title = 'section'
    assert section.is_numbered
    assert section.menu_token_keys == [None, None, None]


def test_MenuSection_menu_token_keys_02():
    '''Menu entry keys equal index 0 of menu entry menu_tokens when menu entry menu_tokens are tuples.
    True whether section is numbered or not.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = [
        ('add', 'add something'),
        ('rm', 'delete something'),
        ('mod', 'modify something'),
        ]
    section = menu.make_section(menu_tokens=menu_tokens)
    section.title = 'section title'
    assert not section.is_numbered
    assert section.menu_token_keys == ['add', 'rm', 'mod']
    assert section.menu_token_keys == [x[0] for x in section.menu_tokens]

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = [
        ('add', 'add something'),
        ('rm', 'delete something'),
        ('mod', 'modify something'),
        ]
    section = menu.make_section(is_numbered=True, menu_tokens=menu_tokens)
    section.title = 'section title'
    assert section.is_numbered
    assert section.menu_token_keys == ['add', 'rm', 'mod']
    assert section.menu_token_keys == [x[0] for x in section.menu_tokens]
