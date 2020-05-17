from houdini.plugins import IPlugin
from houdini import commands

from houdini import permissions
from houdini.data.room import Room

import difflib


class Essentials(IPlugin):
    author = "Solero"
    description = "Essentials plugin"
    version = "1.0.0"

    def __init__(self, server):
        super().__init__(server)

        self.items_by_name = None

    async def ready(self):
        await self.server.permissions.register('essentials.jr')
        await self.server.permissions.register('essentials.ai')
        await self.server.permissions.register('essentials.ac')

        self.items_by_name = {item.name: item for item in self.server.items.values()}

    @commands.command('room', alias=['jr'])
    @permissions.has_or_moderator('essentials.jr')
    async def join_room(self, p, room: Room):
        if room is not None:
            await p.join_room(room)
        else:
            await p.send_xt('mm', 'Room does not exist', p.id)

    @commands.command('ai')
    @permissions.has_or_moderator('essentials.ai')
    async def add_item(self, p, *item_query: str):
        item_query = ' '.join(item_query)

        try:
            if item_query.isdigit():
                item = self.server.items[int(item_query)]
            else:
                item_name = difflib.get_close_matches(item_query, self.items_by_name.keys(), n=1)
                item = self.items_by_name[item_name[0]]

            await p.add_inventory(item, cost=0)
        except (IndexError, KeyError):
            await p.send_xt('mm', 'Item does not exist', p.id)

    @commands.command('ac')
    @permissions.has_or_moderator('essentials.ac')
    async def add_coins(self, p, amount: int = 100):
        await p.add_coins(amount, stay=True)
