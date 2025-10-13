from logging import Logger, getLogger
from dishka import Provider, Scope, provide, from_context


class LoggingProvider(Provider):
    component_name = from_context(provides=str, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def get_logger(self, component_name: str) -> Logger:
        return getLogger(component_name)
