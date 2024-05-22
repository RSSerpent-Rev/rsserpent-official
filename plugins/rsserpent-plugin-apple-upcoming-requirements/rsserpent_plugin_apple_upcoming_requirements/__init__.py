from rsserpent.models import Persona, Plugin

from . import route


plugin = Plugin(
    name="rsserpent-plugin-apple-upcoming-requirements",
    author=Persona(
        name="RSSerpent-Rev",
        link="https://github.com/RSSerpent-Rev",
        email="beijiu572@gmail.com",
    ),
    prefix="/apple-upcoming-requirements",
    repository="https://github.com/RSSerpent-Rev/rsserpent-plugin-apple-upcoming-requirements",
    routers={route.path: route.provider},
)
