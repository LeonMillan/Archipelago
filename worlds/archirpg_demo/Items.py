import math
from typing import Dict, NamedTuple, List
from BaseClasses import Item, ItemClassification, MultiWorld

item_base_id = 774_000_000

item_id_offsets: Dict[str, int] = {
    "actor":    1000,
    "item":     2000,
    "weapon":   4000,
    "armor":    6000,
    "gold_add": 8000,
    "gold_sub": 8500,
}
gold_multiplier = 50
gold_id_max = 500

class ItemData(NamedTuple):
    category: str
    db_id: int
    name: str
    tags: List[str]


class RPGMakerItem(Item):
    game = "RPG Maker"
    groups: List[str] = []

    def __init__(self, player: int, item_id: int, item_data: ItemData) -> None:
        if "Key Item" in item_data.tags:
            item_class = ItemClassification.progression
        elif "Gold" in item_data.tags:
            item_class = ItemClassification.progression_skip_balancing
        elif "Useful" in item_data.tags:
            item_class = ItemClassification.useful
        elif "Trap" in item_data.tags:
            item_class = ItemClassification.trap
        else:
            item_class = ItemClassification.filler
        super().__init__(item_data.name, item_class, item_id, player)
        self.groups = item_data.tags

def gold_id(amount: int):
    gold_item_id = min(math.ceil(abs(amount) / gold_multiplier), gold_id_max)
    gold_start_id = item_id_offsets["gold_add"] if amount > 0 else item_id_offsets["gold_sub"]
    return gold_start_id + gold_item_id

items_table = [
    # ITEMS
    ItemData("item", 1, "Mystery Chest", ["Useful"]),
    ItemData("item", 2, "Mystery Key", ["Key Item", "Access"]),

    ItemData("item", 4, "Small Pouch", ["Tokens"]),
    ItemData("item", 5, "Medium Pouch", ["Tokens"]),
    ItemData("item", 6, "Large Pouch", ["Useful", "Tokens"]),

    ItemData("item", 8, "Slots x10 Access", ["Key Item", "Luck"]),
    ItemData("item", 9, "Slots x100 Access", ["Key Item", "Luck"]),
    ItemData("item", 10, "Rare Coin", ["Useful", "Luck"]),
    ItemData("item", 11, "Lucky Clover", ["Useful", "Luck"]),
    ItemData("item", 12, "Iron Key", ["Key Item", "Access"]),
    ItemData("item", 13, "Wrench", ["Key Item", "Access"]),
    ItemData("item", 14, "Dog Communicator", ["Key Item", "Access"]),
    ItemData("item", 15, "Guesser Booster", ["Useful", "Luck"]),
    
    ItemData("gold_add", gold_id(50), "50G", ["Useful", "Gold"]),
    ItemData("gold_add", gold_id(100), "100G", ["Useful", "Gold"]),
    ItemData("gold_add", gold_id(200), "200G", ["Useful", "Gold"]),
]

item_name_groups: Dict[str, List[str]] = {}
for item in items_table:
    for group in item.tags:
        item_name_groups[group] = item_name_groups.get(group, []) + [item.name]

filler_weights = {
    "Large Pouch": 20,
    "Medium Pouch": 40,
    "Small Pouch": 15,
    "50G": 15,
    "100G": 10,
    "200G": 5,
}

class ArchiRPGItemManager:
    item_name_to_data = None
    item_name_to_id = None
    
    def generate_item_dicts(self):
        self.item_name_to_data = { item.name: item for item in items_table }
        self.item_name_to_id = { item.name: self.convert_item_id(item.category, item.db_id) for item in items_table }
    
    def get_item_name_to_id(self):
        if self.item_name_to_id is None:
            self.generate_item_dicts()
        return self.item_name_to_id
    
    def get_item_name_to_data(self):
        if self.item_name_to_data is None:
            self.generate_item_dicts()
        return self.item_name_to_data

    def convert_item_id(self, category: str, db_id: int):
        return item_base_id + item_id_offsets[category] + db_id

    def create_item(self, player: int, name: str):
        item_id_dict = self.get_item_name_to_id()
        item_data_dict = self.get_item_name_to_data()
        return RPGMakerItem(player, item_id_dict[name], item_data_dict[name])

    def create_items(self, player: int, multiworld: MultiWorld):
        locations_count = len([location
                               for location in multiworld.get_locations(player)
                               if not location.event])
        
        excluded_items = [item for item in multiworld.precollected_items[player]]
        item_list = [
            self.create_item(player, "Mystery Key"),
            self.create_item(player, "Slots x10 Access"),
            self.create_item(player, "Slots x100 Access"),
            self.create_item(player, "Rare Coin"),
            self.create_item(player, "Rare Coin"),
            self.create_item(player, "Rare Coin"),
            self.create_item(player, "Rare Coin"),
            self.create_item(player, "Lucky Clover"),
            self.create_item(player, "Iron Key"),
            self.create_item(player, "Wrench"),
            self.create_item(player, "Dog Communicator"),
            self.create_item(player, "Guesser Booster"),

            self.create_item(player, "Mystery Chest"),
            self.create_item(player, "Mystery Chest"),
            self.create_item(player, "Mystery Chest"),

            self.create_item(player, "100G"),
            self.create_item(player, "200G"),
        ]
        for excluded_item in excluded_items:
            item_list.remove(excluded_item)
        
        multiworld.itempool += item_list

        # Add as many filler items as necessary to meet location count
        filler_slots = locations_count - len(item_list)
        for _ in range(filler_slots):
            filler_item = multiworld.random.choices( list(filler_weights.keys()), list(filler_weights.values()) )[0]
            multiworld.itempool += [self.create_item(player, filler_item)]