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

    def get_p_damage(self):
        idx = 0 if self.level < 6 else 1
        ability = self.data["abilities"]["P"]
        return ability["base"][idx] + (self.total_ap * ability["ap_ratio"]) + (self.bonus_ad * ability["bonus_ad_ratio"])

    def get_q_damage(self, rank):
        ability = self.data["abilities"]["Q"]
        return ability["base"][rank - 1] + (self.total_ap * ability["ap_ratio"])

    def get_e_damage(self, rank):
        ability = self.data["abilities"]["E"]
        raw_e = ability["base"][rank - 1] + (self.total_ad * ability["ad_ratio"]) + (self.total_ap * ability["ap_ratio"])
        return raw_e + self.get_on_hit_damage()

    def get_r_damage(self, rank, daggers=15):
        ability = self.data["abilities"]["R"]
        base = ability["base_per_dagger"][rank - 1]
        scaling = self.bonus_ad * ability["bonus_ad_ratio"]
        return (base + scaling) * daggers

    def get_each_ability(self, q_rank, e_rank, r_rank):
        q = self.get_q_damage(q_rank)
        e = self.get_e_damage(e_rank)
        r_base = self.get_r_damage(r_rank)
        r_on_hit = self.get_on_hit_damage() * 15 * 0.30
        return q + e + r_base + r_on_hit

    def get_qewr_damage(self, q_rank, e_rank, r_rank):
        q = self.get_q_damage(q_rank)
        e = self.get_e_damage(e_rank)
        p = self.get_p_damage()
        r_base = self.get_r_damage(r_rank)
        r_on_hit = self.get_on_hit_damage() * 15 * 0.30
        total = q + e + p + r_base + r_on_hit + p
        return total