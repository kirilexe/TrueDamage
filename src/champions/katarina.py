import json

class Katarina:
    def __init__(self, level, data_file="data/champions.json"):
        with open(data_file, "r") as f:
            all_data = json.load(f)
        
        self.data = all_data["Katarina"]
        self.level = level
        
        self.base_ad = self.data["stats"]["base_ad"] + (self.data["stats"]["ad_per_level"] * (level - 1))
        self.bonus_ad = 0
        self.bonus_ap = 0

    @property
    def total_ad(self):
        return self.base_ad + self.bonus_ad

    @property
    def total_ap(self):
        return self.bonus_ap

    def get_p_damage(self):
        idx = 0 if self.level < 6 else 1 
        base = self.data["abilities"]["P"]["base"][idx]
        return base + (self.total_ap * self.data["abilities"]["P"]["ap_ratio"]) + (self.bonus_ad * self.data["abilities"]["P"]["bonus_ad_ratio"])

    def get_q_damage(self, rank):
        base = self.data["abilities"]["Q"]["base"][rank-1]
        return base + (self.total_ap * self.data["abilities"]["Q"]["ap_ratio"])

    def get_e_damage(self, rank):
        base = self.data["abilities"]["E"]["base"][rank-1]
        return base + (self.total_ad * self.data["abilities"]["E"]["ad_ratio"]) + (self.total_ap * self.data["abilities"]["E"]["ap_ratio"])

    def get_r_damage(self, rank, daggers=15):
        base = self.data["abilities"]["R"]["base_per_dagger"][rank-1]
        scaling = self.bonus_ad * self.data["abilities"]["R"]["bonus_ad_ratio"]
        return (base + scaling) * daggers

# TESTING
kat = Katarina(level=1)
kat.bonus_ap = 62
kat.bonus_ad = 0

print(f"Katarina Q dmg: {kat.get_q_damage(rank=3)}") # Q test works in game
print(f"Katarina E dmg: {kat.get_e_damage(rank=1)}") # E test is slightly off in game, but close enough for now
print(f"Katarina R dmg (full channel): {kat.get_r_damage(rank=1)}") # R test is off because of scaling issues