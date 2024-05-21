from rsserpent.models import Persona, Plugin

from . import update


plugin = Plugin(
    name="rsserpent-plugin-admob-sdk",
    author=Persona(
        name="Ekko",
        link="https://github.com/EkkoG",
        email="beijiu572@gmail.com",
    ),
    prefix="/admob/sdk",
    repository="https://github.com/EkkoG/rsserpent-plugin-applovin-sdk",
    routers={
        update.path: update.provider,
    },
)
