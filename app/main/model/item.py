from typing import Union, Any

from pydantic.class_validators import validator
from pydantic.networks import HttpUrl
from pydantic_xml import BaseXmlModel, element

from app.main.util.validators import parse_date


class Item(BaseXmlModel):
    title: str = element()
    link: HttpUrl = element()
    description: Union[str, None] = element()
    guid: str = element()
    publish_date: str = element(tag='pubDate')
    _parse_date = validator('publish_date', allow_reuse=True)(parse_date)

    def __hash__(self) -> int:
        return self.guid.__hash__()

    def __eq__(self, other: Any) -> bool:
        if other is None:
            return False
        if isinstance(other, Item):
            return other.guid.__eq__(self.guid)
        else:
            return False
