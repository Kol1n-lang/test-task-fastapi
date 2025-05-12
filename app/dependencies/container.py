from dishka import make_async_container

from app.dependencies.providers import (
    ConfigsProvider,
    DatabaseConnectionProvider,
    RepoProvider,
    ServiceProvider,
)

container = make_async_container(
    ConfigsProvider(),
    DatabaseConnectionProvider(),
    RepoProvider(),
    ServiceProvider(),
)
