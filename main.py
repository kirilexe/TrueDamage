from src.champions.katarina import Katarina
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