import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.models.champion import BaseChampion

class Katarina(BaseChampion):
    def __init__(self, level, data_file="data/champions.json"):
        with open(data_file, "r") as f:
            all_data = json.load(f)
        
        super().__init__("Katarina", level, all_data)
        self.inventory = []
        self._manual_bonus_ap = 0
        self._manual_bonus_ad = 0

    @property
    def bonus_ap(self):
        item_ap = sum(item.get("stats", {}).get("ap", 0) for item in self.inventory)
        return item_ap + self._manual_bonus_ap

    @bonus_ap.setter
    def bonus_ap(self, value):
        self._manual_bonus_ap = value

    @property
    def bonus_ad(self):
        item_ad = sum(item.get("stats", {}).get("ad", 0) for item in self.inventory)
        return item_ad + self._manual_bonus_ad

    @bonus_ad.setter
    def bonus_ad(self, value):
        self._manual_bonus_ad = value

    @property
    def total_ap(self):
        return self.bonus_ap

    @property
    def total_ad(self):
        return self.base_ad + self.bonus_ad

    def get_on_hit_damage(self):
        total_on_hit = 0
        for item in self.inventory:
            if "on_hit" in item:
                oh = item["on_hit"]
                total_on_hit += oh["base_damage"] + (self.total_ap * oh["ap_ratio"])
        return total_on_hit

    # -- ABILITIES --

    def get_p_damage(self):
        idx = 0 if self.level < 6 else 1 
        ability = self.data["abilities"]["P"]
        return ability["base"][idx] + (self.total_ap * ability["ap_ratio"]) + (self.bonus_ad * ability["bonus_ad_ratio"])

    def get_q_damage(self, rank):
        ability = self.data["abilities"]["Q"]
        return ability["base"][rank-1] + (self.total_ap * ability["ap_ratio"])

    def get_e_damage(self, rank):
        ability = self.data["abilities"]["E"]
        raw_e = ability["base"][rank-1] + (self.total_ad * ability["ad_ratio"]) + (self.total_ap * ability["ap_ratio"])

        return raw_e + self.get_on_hit_damage()

    def get_r_damage(self, rank, daggers=15):
        ability = self.data["abilities"]["R"]
        base = ability["base_per_dagger"][rank-1]
        scaling = self.bonus_ad * ability["bonus_ad_ratio"]
        return (base + scaling) * daggers
    
    # -- COMBOS -- 
    def get_each_ability(self, q_rank, e_rank, r_rank):
        q = self.get_q_damage(q_rank)
        e = self.get_e_damage(e_rank)

        r_base = self.get_r_damage(r_rank)
        r_on_hit = self.get_on_hit_damage() * 15 * 0.30 # katarina's R applies onhit only on 30% effectiveness

        total = q + e + r_base + r_on_hit
        return total
    
    def get_qewr_damage(self, q_rank, e_rank, r_rank):
        q = self.get_q_damage(q_rank)
        e = self.get_e_damage(e_rank)
        p = self.get_p_damage()

        r_base = self.get_r_damage(r_rank)
        r_on_hit = self.get_on_hit_damage() * 15 * 0.30 # katarina's R applies onhit only on 30% effectiveness

        total = q + e + p + r_base + r_on_hit + p # assuming 2 procs of passive in a full combo
        return total

# TESTING
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