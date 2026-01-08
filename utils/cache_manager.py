# services/cache_manager.py
import os
import json

class CacheManager:
    def __init__(self, cache_file="data/cache.json"):
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        """Charge le cache depuis le fichier JSON"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Warning: cache.json corrompu, un nouveau sera créé")
                return {}
        return {}

    def save_cache(self):
        """Sauvegarde le cache dans le fichier JSON"""
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f, indent=4)

    def set_default_cache(self, profile):
        riot_id = profile["Riot_id"]
        self.cache[riot_id] = {
            "image_url": None,
            "opgg_data": {
                "tier": "unknown",
                "division": "unknown",
                "lp": "unknown"
            }
        }
        self.save_cache()

    def get(self, key):
        """Récupère une entrée du cache"""
        return self.cache.get(key)

    def set(self, key, value):
        """Ajoute ou met à jour une entrée du cache"""
        self.cache[key] = value
        self.save_cache()

    def clear(self):
        """Vide le cache"""
        self.cache = {}
        self.save_cache()
