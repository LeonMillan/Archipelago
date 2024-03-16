import math
from typing import Dict, List
from itertools import chain

from BaseClasses import Item, Location, Region, Tutorial, MultiWorld
from Options import PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import set_rule, forbid_item

# from .Options import RPGMakerOptions
from .Items import item_name_groups, ArchiRPGItemManager
from .Locations import location_table


class ArchiRPGLocation(Location):
    game: str = "ArchiRPG Demo"


class ArchiRPGDemoWebWorld(WebWorld):
    theme = "grass"
    
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="How to play the ArchiRPG Demo",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["LeonMillan"]
    )

    tutorials = [setup_en]


class ArchiRPGDemoWorld(World):
    """Demo for ArchiRPG (Archipelago integration for RPG Maker MV/MZ)."""
    
    item_manager = ArchiRPGItemManager()

    game = "ArchiRPG Demo"
    base_id = 774_000_000
    data_version = 1
    web = ArchiRPGDemoWebWorld()
    options_dataclass = PerGameCommonOptions
    options: PerGameCommonOptions
    item_name_to_id = item_manager.get_item_name_to_id()
    location_name_to_id = { loc["name"]: 774_000_000 + i for i, loc in enumerate(chain.from_iterable(location_table.values())) }
    item_name_groups = item_name_groups

    def create_regions(self) -> None:
        start_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions += [start_region]

        game_room = Region("Game Room", self.player, self.multiworld)
        game_room.locations = [
            ArchiRPGLocation(self.player, loc["name"], self.location_name_to_id[loc["name"]], game_room)
            for loc in location_table["Game Room"]
        ]

        clown = Region("Clown", self.player, self.multiworld)
        clown.locations = [
            ArchiRPGLocation(self.player, loc["name"], self.location_name_to_id[loc["name"]], clown)
            for loc in location_table["Clown"]
        ]

        gacha_machine = Region("Gacha Machine", self.player, self.multiworld)
        gacha_machine.locations = [
            ArchiRPGLocation(self.player, loc["name"], self.location_name_to_id[loc["name"]], gacha_machine)
            for loc in location_table["Gacha Machine"]
        ]

        mystery_chests = Region("Mystery Chests", self.player, self.multiworld)
        mystery_chests.locations = [
            ArchiRPGLocation(self.player, loc["name"], self.location_name_to_id[loc["name"]], mystery_chests)
            for loc in location_table["Mystery Chests"]
        ]
        
        underground = Region("Underground", self.player, self.multiworld)
        underground.locations = [
            ArchiRPGLocation(self.player, loc["name"], self.location_name_to_id[loc["name"]], underground)
            for loc in location_table["Underground"]
        ]
        
        maze_game = Region("Maze Game", self.player, self.multiworld)
        maze_game.locations = [
            ArchiRPGLocation(self.player, loc["name"], self.location_name_to_id[loc["name"]], maze_game)
            for loc in location_table["Maze Game"]
        ]

        devil_shop = Region("Devil Shop", self.player, self.multiworld)
        devil_shop.locations = [
            ArchiRPGLocation(self.player, loc["name"], self.location_name_to_id[loc["name"]], devil_shop)
            for loc in location_table["Devil Shop"]
        ]

        walking_dog = Region("Walking Dog", self.player, self.multiworld)
        walking_dog.locations = [
            ArchiRPGLocation(self.player, loc["name"], self.location_name_to_id[loc["name"]], walking_dog)
            for loc in location_table["Walking Dog"]
        ]

        start_region.connect(game_room, "Start Game")
        game_room.connect(gacha_machine, "Play Gacha")
        game_room.connect(clown, "Talk to Clown")
        game_room.connect(mystery_chests, "Open Mystery Chest",
                          lambda state: state.has("Mystery Key", self.player))
        game_room.connect(underground, "Go Underground",
                          lambda state: state.has("Wrench", self.player))
        underground.connect(maze_game, "Play Maze Game")
        underground.connect(devil_shop, "Talk to Devil",
                          lambda state: state.count_group("Gold", self.player) >= 1)
        underground.connect(walking_dog, "Talk to Dog",
                          lambda state: state.has("Dog Communicator", self.player))
        
        gacha_machine.connect(game_room)
        clown.connect(game_room)
        mystery_chests.connect(game_room)
        underground.connect(game_room)
        maze_game.connect(underground)
        devil_shop.connect(underground)
        walking_dog.connect(underground)

        self.multiworld.regions += [
            start_region,
            game_room,
            clown,
            gacha_machine,
            mystery_chests,
            underground,
            maze_game,
            devil_shop,
            walking_dog,
        ]
    
    def set_rules(self) -> None:
        set_rule(self.multiworld.get_location("Iron Chest", self.player),
                 lambda state: state.has("Iron Key", self.player))
        
        set_rule(self.multiworld.get_location("Underground Iron Chest Left", self.player),
                 lambda state: state.has("Iron Key", self.player))
        
        set_rule(self.multiworld.get_location("Underground Iron Chest Right", self.player),
                 lambda state: state.has("Iron Key", self.player))
        
        # Try to prevent expensive gifts from having early items
        set_rule(self.multiworld.get_location("Clown Gift Small", self.player),
                 lambda state: state.count_group("Luck", self.player) >= 2)
        set_rule(self.multiworld.get_location("Clown Gift Large", self.player),
                 lambda state: state.count_group("Luck", self.player) >= 3)
        set_rule(self.multiworld.get_location("Clown Gift Huge", self.player),
                 lambda state: state.count_group("Luck", self.player) >= 4 and
                 state.has("Slots x100 Access", self.player))
        
        for i in range(18):
            location = self.multiworld.get_location(f"Mystery Chest {i+1}", self.player)
            forbid_item(location, "Mystery Chest", self.player)
        
        for i in range(16):
            min_luck = math.floor(i / 5)
            set_rule(self.multiworld.get_location(f"Gacha {i+1}", self.player),
                     lambda state: state.has_group("Luck", self.player, min_luck))

        from Utils import visualize_regions
        visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    def create_item(self, name: str) -> Item:
        return self.item_manager.create_item(self.player, name)
    
    def create_items(self) -> None:
        return self.item_manager.create_items(self.player, self.multiworld)

    def fill_slot_data(self) -> Dict[str, object]:
        included_option_names: List[str] = [option_name for option_name in self.options_dataclass.type_hints]
        return self.options.as_dict(*included_option_names, casing="camel")