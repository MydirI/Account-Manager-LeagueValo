import json
import os


class ProfileManager:
    def __init__(self, file_path="data/profiles_data.json"):
        self.file_path = file_path
        self.profiles = self.load_profiles()

    def load_profiles(self):
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r") as f:
            data = json.load(f)
            return data.get("Profiles", [])

    def save_profiles(self):
        with open(self.file_path, "w") as f:
            json.dump({"Profiles": self.profiles}, f, indent=4)

    def get_all(self):
        return self.profiles

    def add(self, profile):
        self.profiles.append(profile)
        self.save_profiles()

    def delete(self, riot_id):
        self.profiles = [
            p for p in self.profiles if p["Riot_id"] != riot_id
        ]
        self.save_profiles()

    def update(self, old_riot_id, new_profile):
        for i, profile in enumerate(self.profiles):
            if profile["Riot_id"] == old_riot_id:
                self.profiles[i] = new_profile
                break
        self.save_profiles()
