from rsserpent.models import Persona, Plugin

from . import route


plugin = Plugin(
    name="rsserpent-plugin-applovin-sdk",
    author=Persona(
        name="Ekko",
        link="https://github.com/EkkoG",
        email="beijiu572@gmail.com",
    ),
    prefix="/applovin/sdk",
    repository="https://github.com/EkkoG/rsserpent-plugin-applovin-sdk",
    routers={
        route.path: route.provider,
    },
)
