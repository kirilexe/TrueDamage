import json


class BaseChampion:
    def __init__(self, name, level, data_dict):
        self.name = name
        self.level = level
        self.data = data_dict[name]
        self.inventory = []

        stats = self.data["stats"]
        self.base_ad = stats["base_ad"] + (stats.get("ad_per_level", 0) * (level - 1))
        self.base_ap = stats.get("base_ap", 0) + (stats.get("ap_per_level", 0) * (level - 1))
        self.base_as = stats["as"]

        if level > 1:
            as_per_level = stats.get("as_per_level", [])
            self.growth_as_pct = as_per_level[level - 2] / 100 if as_per_level else 0
        else:
            self.growth_as_pct = 0

        self.current_stacks = 0
        self._manual_bonus_ad = 0
        self._manual_bonus_ap = 0
        self._manual_bonus_as = 0

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
    def bonus_as(self):
        item_as = sum(item.get("stats", {}).get("attack_speed", 0) for item in self.inventory)
        return item_as + self._manual_bonus_as

    @bonus_as.setter
    def bonus_as(self, value):
        self._manual_bonus_as = value

    @property
    def total_ad(self):
        return self.base_ad + self.bonus_ad

    @property
    def total_ap(self):
        return self.base_ap + self.bonus_ap

    def get_on_hit_damage(self):
        total_on_hit = 0
        for item in self.inventory:
            if "on_hit" in item:
                oh = item["on_hit"]
                total_on_hit += oh["base_damage"] + (self.total_ap * oh["ap_ratio"])
        return total_on_hit