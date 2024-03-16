from typing import Dict, TypedDict, List
from BaseClasses import LocationProgressType


class RPGLocationDict(TypedDict, total=False): 
    name: str
    description: str
    progressType: LocationProgressType


location_table: Dict[str, List[RPGLocationDict]] = {
    "Game Room": [
        {"name": "Iron Chest",
         "description": "Acquired by opening the iron chest with the Iron Key",
         "progressType": LocationProgressType.DEFAULT},
    ],
    "Underground": [
        {"name": "Underground Iron Chest Left",
         "description": "Acquired by opening the iron chest with the Iron Key",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Underground Iron Chest Right",
         "description": "Acquired by opening the iron chest with the Iron Key",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Underground Locker",
         "description": "Item inside the locker in the underground",
         "progressType": LocationProgressType.DEFAULT},
    ],
    "Maze Game": [
        {"name": "Maze Game Easy",
         "description": "Prize for completing Maze Game Lv 1",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Maze Game Medium",
         "description": "Prize for completing Maze Game Lv 2",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Maze Game Hard",
         "description": "Prize for completing Maze Game Lv 3",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Maze Game Very Hard",
         "description": "Prize for completing Maze Game Lv 4",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Maze Game Trophy",
         "description": "Prize for completing all Maze Game levels",
         "progressType": LocationProgressType.EXCLUDED},
    ],
    "Clown": [
        {"name": "Clown Gift Tiny",
         "description": "Gift bought from the clown (500 tokens)",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Clown Gift Small",
         "description": "Gift bought from the clown (1000 tokens)",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Clown Gift Large",
         "description": "Gift bought from the clown (2500 tokens)",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Clown Gift Huge",
         "description": "Gift bought from the clown (5000 tokens)",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Clown Gift Super Duper",
         "description": "Gift given by clown after purchasing all other gifts",
         "progressType": LocationProgressType.DEFAULT},
    ],
    "Walking Dog": [
        {"name": "Dog Walk 1",
         "description": "Walk 100 steps then talk to the dog",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Dog Walk 2",
         "description": "Walk 200 steps then talk to the dog",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Dog Walk 3",
         "description": "Walk 300 steps then talk to the dog",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Dog Walk 4",
         "description": "Walk 500 steps then talk to the dog",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Dog Walk 5",
         "description": "Walk 800 steps then talk to the dog",
         "progressType": LocationProgressType.DEFAULT},
    ],
    "Devil Shop": [
        {"name": "Devil Shop Rare Coin",
         "description": "Purchased with G from the Devil in the underground",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Devil Shop Lucky Clover",
         "description": "Purchased with G from the Devil in the underground",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Devil Shop Guesser Booster",
         "description": "Purchased with G from the Devil in the underground",
         "progressType": LocationProgressType.DEFAULT},
        {"name": "Devil Shop Extra Item",
         "description": "Purchased with G from the Devil in the underground",
         "progressType": LocationProgressType.DEFAULT},
    ],
    "Mystery Chests": [
        {"name": f"Mystery Chest {i+1}",
         "description": f"Acquired by opening Mystery Chest (Item #{i+1})",
         "progressType": LocationProgressType.DEFAULT} for i in range(18)
    ],
    "Gacha Machine": [
        {"name": f"Gacha {i+1}",
         "description": f"Acquired as Gacha prize (Item #{i+1})",
         "progressType": LocationProgressType.DEFAULT} for i in range(16)
    ],
}
