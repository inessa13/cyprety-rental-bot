import calendar
import datetime
import logging
from typing import List

from . import client, entities, parsers, settings

logger = logging.getLogger(__name__)


class Provider:

    def __init__(self, url: str, parser: parsers.Parser, webclient: client.Client):
        self.client = webclient
        self.url = url
        self.parser = parser
        self.latest_created_at: float = calendar.timegm((datetime.datetime.utcnow() - datetime.timedelta(days=1)).utctimetuple())
        self.recently_seen: List[str] = []

    async def get_updates(self) -> List[entities.Property]:
        logger.info('get_updates...')
        content = await self.client.get(self.url)
        properties = self.parser.parse(content)
        _total = len(properties)

        properties = list(sorted(properties, key=lambda x: x.created_at))[:settings.SHOW_MAX]
        for property in properties:
            print(property.title, property.created_at > self.latest_created_at, property.price, property.url)

        properties = [p for p in properties if p.created_at > self.latest_created_at]
        properties = [p for p in properties if p.url not in self.recently_seen]
        logger.info('found %d total and %d filtered', _total, len(properties))
        if properties:
            self.latest_created_at = max(p.created_at for p in properties)
            self.recently_seen = ([p.url for p in properties] + self.recently_seen)[:settings.SHOW_MAX]

        return properties
