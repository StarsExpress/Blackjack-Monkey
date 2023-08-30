from pywebio.output import put_html, use_scope, put_text, clear


def set_title(title):  # Set page title.
    put_html(title)


def write_text(message, scope, use=False):  # Performs put_text in given scope.
    if use:  # Apply use_scope syntax if use is True.
        with use_scope(scope):
            put_text(message)
        return

    put_text(message, scope=scope)


def clear_contents(scope):  # Clear contents inside given scope.
    clear(scope)
