class BaseChampion:
    def __init__(self, name, level, data_dict):
        self.name = name
        self.level = level
        self.data = data_dict[name]
        self.inventory = [] # A list of all the item names
        
        self.base_ad = self.data["stats"]["base_ad"] + (self.data["stats"]["ad_per_level"] * (level - 1)) # Calculate the base AD at the given level
        
        self.bonus_ad = 0
        self.bonus_ap = 0

    @property
    def bonus_ap(self):
        return sum(item["stats"].get("ap", 0) for item in self.inventory)

    @property
    def bonus_ad(self):
        return sum(item["stats"].get("ad", 0) for item in self.inventory)

    @property
    def total_ad(self):
        return self.base_ad + self.bonus_ad

    @property
    def total_ap(self):
        return self.bonus_ap
    
    def get_on_hit_damage(self):
        total_on_hit = 0
        for item in self.inventory:
            if "on_hit" in item:
                oh = item["on_hit"]
                total_on_hit += oh["base_damage"] + (self.total_ap * oh["ap_ratio"])
        return total_on_hit