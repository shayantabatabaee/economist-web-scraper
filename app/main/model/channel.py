from typing import Set, List, Union
from app.main.model.item import Item
from pydantic_xml import BaseXmlModel, element
from pydantic.class_validators import validator
from app.main.util.validators import parse_date


class Channel(BaseXmlModel, tag='channel'):
    title: str = element()
    link: str = element()
    description: Union[str, None] = element()
    publish_date: str = element(tag='pubDate')
    items: Set[Item] = element(tag='item')
    _parse_date = validator('publish_date', allow_reuse=True)(parse_date)
