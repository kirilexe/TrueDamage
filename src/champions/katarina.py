import json

class Katarina:
    def __init__(self, level, data_file="data/champions.json"):
        with open(data_file, "r") as f:
            all_data = json.load(f)
        self.data = all_data["Katarina"]
        self.level = level
        self.base_ad = self.data["stats"]["base_ad"]
        self.ad_per_level = self.data["stats"]["ad_per_level"]
        self.ap = self.data["stats"].get("base_ap", 0)

    def get_q_damage(self, ap, rank):
        base = self.data["abilities"]["Q"]["base"][rank-1]
        scaling = ap * self.data["abilities"]["Q"]["ap_ratio"]
        return base + scaling
    

# TESTING

kat = Katarina(level=1)
q_dmg = kat.get_q_damage(ap=30, rank=1)

print(f"Katarina Q dmg: {q_dmg}")