import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.models.champion import BaseChampion


class Irelia(BaseChampion):
    def __init__(self, level, data_file="data/champions.json"):
        with open(data_file, "r") as f:
            all_data = json.load(f)

        super().__init__("Irelia", level, all_data)

    def get_passive_as_per_stack(self):
        ability = self.data["abilities"]["P"]
        breakpoints = ability["attack_speed_per_stack"]
        if self.level >= 13:
            return breakpoints["level_13"]
        elif self.level >= 7:
            return breakpoints["level_7"]
        return breakpoints["level_1"]

    def get_passive_onhit(self, stacks):
        ability = self.data["abilities"]["P"]
        base_magic_dmg = 0
        if stacks == ability.get("max_stacks", 4):
            base_magic_dmg = 10 + (3 * (self.level - 1))
        scaling_dmg = self.bonus_ad * ability["on_hit_magic_damage"]["bonus_ad_ratio"]
        return base_magic_dmg + scaling_dmg

    def get_on_hit_damage(self, stacks=0, target_health=0):
        item_on_hit = super().get_on_hit_damage()
        passive_on_hit = self.get_passive_onhit(stacks)
        return item_on_hit + passive_on_hit

    def get_q_damage(self, rank):
        ability = self.data["abilities"]["Q"]
        return ability["base"][rank - 1] + (self.total_ad * ability["ad_ratio"])

    def get_w_damage(self, rank):
        ability = self.data["abilities"]["W"]
        return ability["base"][rank - 1] + (self.total_ad * ability["ad_ratio"]) + (self.total_ap * ability["ap_ratio"])
    
    def get_e_damage(self, rank):
        ability = self.data["abilities"]["E"]
        return ability["base"][rank - 1] + (self.total_ap * ability["ap_ratio"])

    def get_r_damage(self, rank, hits=2):
        ability = self.data["abilities"]["R"]
        per_hit = ability["base_per_hit"][rank - 1] + (self.total_ap * ability["ap_ratio"])
        return per_hit * hits
    
    def no_ult_combo(self, q_rank=1, w_rank=1, e_rank=1, r_rank=1, target_health=0):
        # SETUP
        q = self.get_q_damage(q_rank)
        w = self.get_w_damage(w_rank)
        e = self.get_e_damage(e_rank)
        r = self.get_r_damage(r_rank)
        onhit = self.get_on_hit_damage(4, target_health) # assuming she has 4 stacks todo fix this later
        auto =  onhit + self.base_ad + self.bonus_ad

        # COMBO
        total = e + q + auto + q + w + auto * 2
        return total
    
    def ult_combo(self, q_rank=1, w_rank=1, e_rank=1, r_rank=1, target_health=0):
        # SETUP
        q = self.get_q_damage(q_rank)
        w = self.get_w_damage(w_rank)
        e = self.get_e_damage(e_rank)
        r = self.get_r_damage(r_rank)
        onhit = self.get_on_hit_damage(4, target_health) # assuming she has 4 stacks todo fix this later
        auto =  onhit + self.base_ad + self.bonus_ad

        # COMBO
        total = r + q + auto + e + auto + q + auto + w
        return total