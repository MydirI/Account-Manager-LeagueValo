import os
import json

class CacheManager:
    def __init__(self, cache_file="data/cache.json"):
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Warning: No cache.json, creating a new one...")
                return {}
        return {}

    def save_cache(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f, indent=4)

    def set_default_cache(self, profile):
        riot_id = profile["Riot_id"]
        self.cache[riot_id] = {
            "image_url": None,
            "last_request_time":None,
            "opgg_data": {
                "tier": "unknown",
                "division": "unknown",
                "lp": "unknown"
            }
        }
        self.save_cache()

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value
        self.save_cache()

    def clear(self):
        self.cache = {}
        self.save_cache()
