from src.champions.katarina import Katarina
from src.champions.irelia import Irelia
import json


# -- INITIAL TEST --
if __name__ == "__main__":
    with open("data/items.json", "r") as f:
        item_data = json.load(f)

    # Get Nashors from the data and add it to Kat
    nashors = item_data["Nashors Tooth"]
    
    kat = Katarina(level=1)
    kat.inventory.append(nashors)
    kat.bonus_ap = 62
    kat.bonus_ad = 0

    print(f"Katarina Q dmg: {kat.get_q_damage(rank=3)}") # Q test works in game
    print(f"Katarina E dmg: {kat.get_e_damage(rank=1)}") # E test is slightly off in game, but close enough for now
    # a test of kata's basic combo - Q + E on dagger + W + R with full channel, 2 passive procs on one target
    print(f"Katarina Q-E-W-R dmg: {kat.get_qewr_damage(q_rank=3, e_rank=1, r_rank=3)}")


    # irelia test
    bork = item_data["Blade of the ruined king"]

    irelia = Irelia(level=1)
    irelia.inventory.append(bork)

    print(f"Irelia no R combo damage: {irelia.no_ult_combo(q_rank=5, w_rank=3, e_rank=1, r_rank=1)}")
    print(f"Irelia R combo damage: {irelia.ult_combo(q_rank=5, w_rank=3, e_rank=1, r_rank=1)}")