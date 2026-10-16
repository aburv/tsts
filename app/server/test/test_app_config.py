from unittest import mock

from flask import Flask

from src.app import App


def get_app() -> Flask:
    app = App()
    with mock.patch.object(App, '_set_up'):
        app.create()

    return app.get_app()
