from abc import ABC, abstractmethod

from pydantic import BaseModel, Extra

from database.config.orm.mixin import ORMConfig


class Config(BaseModel, ABC):
    orm: ORMConfig = ORMConfig()

    @abstractmethod
    def uri(self) -> str: ...

    class Config:
        extras = Extra.allow
