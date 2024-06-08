from configs.app_config import PAGE_NAME, PAGE_THEME, PAGE_TITLE
from configs.output_config import TITLE_SCOPE, PLAYER_HEADER, PLAYER_SCOPE, DEALER_HEADER, DEALER_SCOPE
from configs.output_config import INTRO_SUB_SCOPES, RULES_SUB_SCOPES, INCOME_SUB_SCOPES, SHARED_HEIGHT, RELATIVE_WIDTH
from pywebio.platform import config
from pywebio.session import set_env
from pywebio.output import put_html, put_collapse, put_scrollable, put_scope
from pywebio.output import put_row, put_text, put_tabs, clear, use_scope


def set_name_and_theme():
    config(title=PAGE_NAME, theme=PAGE_THEME)


def set_top_layouts():  # Set page title and scopes for rules and income statement.
    put_scope(name=TITLE_SCOPE,
              content=put_html(f"""<h1 align='center'><strong>{PAGE_TITLE}</strong></h1>""", scope=TITLE_SCOPE))
    put_row(content=[put_scope(INTRO_SUB_SCOPES['intro']),
                     put_scope(RULES_SUB_SCOPES['rules']),
                     put_scope(INCOME_SUB_SCOPES['income'])], scope=TITLE_SCOPE)


def set_core_layouts_width():  # Set core layouts' width as 90% of page width.
    set_env(output_max_width='90%')


def set_core_layouts():  # Set game page layouts: two parallel contents.
    # Left side content: scope for cards of each player's hand.
    player_content = put_collapse(PLAYER_HEADER, put_scrollable(
        put_scope(PLAYER_SCOPE), height=SHARED_HEIGHT, keep_bottom=True), open=True)

    # Right side content: scope for dealer's cards.
    dealer_content = put_collapse(DEALER_HEADER, put_scrollable(
        put_scope(DEALER_SCOPE), height=SHARED_HEIGHT, keep_bottom=True), open=True)

    put_row([player_content, None, dealer_content], size=RELATIVE_WIDTH)  # None: middle blank between scopes.


def set_cards_tabs(head_hands: int):  # Set tabs to store scopes for each head hand and its branches.
    tabs_list = []

    for i in range(1, head_hands + 1):
        head_scope = f'{PLAYER_SCOPE}_{str(i)}'
        content = put_scope(name=head_scope, content=put_text(f"Hand {str(i)}'s Branches", scope=head_scope))
        tabs_list.append({'title': f'Hand {str(i)}', 'content': content})

    put_tabs(tabs_list, PLAYER_SCOPE)  # Put all tabs in player scope.


def clear_contents(scopes: list[str] | str):  # Clear contents inside given scope(s).
    if isinstance(scopes, list):  # If input is a list of scopes.
        for scope in scopes:
            clear(scope)

    else:
        clear(scopes)


def write_text(message: str, scope: str, clear_scope: bool = True):  # Performs put_text in given scope.
    with use_scope(scope, clear=clear_scope) as s:
        put_text(message, scope=s)
