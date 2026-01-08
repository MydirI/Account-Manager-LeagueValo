import customtkinter as tk
from opgg.opgg import OPGG
import requests
import PIL
from PIL import Image
import io
from script import script_launch
from CTkToolTip import *
import tkinter as ttk
import threading
from io import BytesIO
import pywinstyles
from tkinter import Frame
from opgg.params import Region
from utils.image_utils import download_image
from utils.cache_manager import CacheManager
from utils.profile_manager import ProfileManager
import time


class main_window:
    def __init__(self) -> None:
        self.root = tk.CTk()
        image = PIL.Image.open("assets\\background.png")
        self.root.configure(fg_color='#010A13')
        background_image = tk.CTkImage(image, size=(800, 500))
        bg_lbl = tk.CTkLabel(self.root, text="", image=background_image)
        bg_lbl.place(x=0, y=0)
        pywinstyles.set_opacity(bg_lbl, value=0.65, color="#010A13")
        self.root.focus_force()
        self.root.title("Riot account manager")
        tk.set_appearance_mode("Dark")

        self.root.geometry('800x500')
        self.root.resizable(0, 0)

        image_riot = PIL.Image.open("assets\\Riot_Manager_white.png")
        riot_logo = tk.CTkImage(image_riot, size=(220, 100))
        riot_lbl = tk.CTkLabel(self.root, text="", image=riot_logo, bg_color="#000001")
        riot_lbl.place(x=50, y=50)
        pywinstyles.set_opacity(riot_lbl, value=0.75, color="#000001")

        self.frame_profile = tk.CTkFrame(self.root, width=700, height=101, fg_color="#000001", corner_radius=0)
        self.frame_profile.pack(expand=True)
        self.frame_profile.place(x=182, y=215)
        pywinstyles.set_opacity(self.frame_profile, value=0.75, color="#000001")

        self.prev_button = tk.CTkButton(self.root, text="", width=50, height=101, fg_color="#311662", command=self.show_previous_profiles, corner_radius=5)
        self.prev_button.place(x=140, y=215)
        pywinstyles.set_opacity(self.prev_button, value=0.2, color="#000001")

        self.next_button = tk.CTkButton(self.root, text='', width=50, height=101, fg_color="#311662", command=self.show_next_profiles, corner_radius=5)
        self.next_button.place(x=620, y=215)
        pywinstyles.set_opacity(self.next_button, value=0.2, color="#000001")

        games_list = ["League of legends", "Valorant"]
        self.choose_game_button = tk.CTkComboBox(self.root, values=games_list, border_color="#000001", corner_radius=5)
        self.choose_game_button.place(x=650, y=450)
        pywinstyles.set_opacity(self.choose_game_button, value=0.5, color="#000001")

        self.current_page = 0
        self.profiles_per_page = 4
        self.cache_manager = CacheManager()
        self.cache = self.cache_manager.load_cache()
        self.profile_manager = ProfileManager()
        self.profiles = self.profile_manager.get_all()

        self.load_all()


    def load_all(self):

        self.button_add = tk.CTkButton(self.root, font=tk.CTkFont(weight="bold", size=65), corner_radius=0, text="+", fg_color="#000001", hover_color="#091428", height=100, width=100, command=self.add_new_account)
        self.button_add.place(x=350, y=350)
        pywinstyles.set_opacity(self.button_add, color="#000001")
        
        self.profiles = self.profile_manager.get_all()
        self.display_profiles()

    def display_profiles(self):
        for widget in self.frame_profile.winfo_children():
            widget.destroy()

        start_index = self.current_page * self.profiles_per_page
        end_index = start_index + self.profiles_per_page

        for i in range(start_index, min(end_index, len(self.profiles))):
            profile = self.profiles[i]
            riot_id = profile["Riot_id"]
            
            if riot_id in self.cache:
                cache_data = self.cache[riot_id]
                
                if cache_data["image_url"]:
                    try:
                        response = requests.get(cache_data["image_url"], timeout=10)
                        response.raise_for_status()
                        image_data = BytesIO(response.content)
                        my_image = tk.CTkImage(dark_image=Image.open(image_data), size=(75, 75))
                        self.update_ui(profile, my_image, cache_data["opgg_data"])
                    except Exception as e:
                        print(f"Cache image load error: {e}")
                        self.load_default_image(profile)
                else:
                    self.load_default_image(profile)
            else:
                self.load_default_image(profile)
            
            threading.Thread(target=self.update_profile_image, args=(profile,)).start()
            

    def load_default_image(self, profile):
        try:
            default_image = PIL.Image.open("assets\\Default.jpg")
            summoner_image = tk.CTkImage(default_image, size=(75, 75))
            self.update_ui(profile, summoner_image)
        except Exception as e:
            print(f"Default image error: {e}")
       

    def update_profile_image(self, profile):
        try:
            riot_id = profile["Riot_id"]
            
            opgg = OPGG()
            opgg_data = opgg.search(riot_id, region = Region.EUW)
            summoner_data = opgg_data[0].summoner
                
            image_url = summoner_data.profile_image_url
            summoner_image = None

            solo_rank = next((league for league in summoner_data.league_stats if league.game_type == "SOLORANKED"), None)

            if image_url:
                summoner_image = download_image(image_url)

            if summoner_image:
                if solo_rank and solo_rank.tier_info.tier:
                    cache_data = {
                        "image_url": str(image_url),
                        "opgg_data": {
                            "tier": solo_rank.tier_info.tier,
                            "division": solo_rank.tier_info.division,
                            "lp": solo_rank.tier_info.lp
                        }
                    }
                else:
                    cache_data = {
                        "image_url": str(image_url),
                        "opgg_data": {
                            "tier": "unranked",
                            "division": "",
                            "lp": "0"
                        }
                    }
                
                self.cache_manager.set(riot_id, cache_data)

            else:
                self.cache_manager.set_default_cache(profile= profile)
                
        except Exception as e:
            print(f"Profile update error {profile['Riot_id']}: {e}")
            self.cache_manager.set_default_cache(profile= profile)
        

    def update_ui(self, profile, summoner_image, opgg_data=None):
        self.profile_button = tk.CTkButton(
            self.frame_profile,
            text="",
            hover_color="#091428",
            image=summoner_image,
            fg_color="transparent",
            height=100,
            width=100,
            command=lambda: script_launch(profile["Username"], profile["Password"], self.choose_game_button.get())
        )

        self.profile_button.image = summoner_image
        self.profile_button.bind("<Button-3>", lambda event: self.right_click(profile, event))
        self.profile_button.pack(side=tk.LEFT, padx=5)

        if opgg_data is not None:
            tooltip_message = (
                f"{profile['Riot_id']}\n"
                f"{opgg_data['tier']} {opgg_data['division']}\n"
                f"{opgg_data['lp']} LP"
            )
        else:
            tooltip_message = f"{profile['Riot_id']}"

        CTkToolTip(self.profile_button, message=tooltip_message)
    def show_previous_profiles(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_profiles()
        time.sleep(0.1)

    def show_next_profiles(self):
        if (self.current_page + 1) * self.profiles_per_page < len(self.profiles):
            self.current_page += 1
            self.display_profiles()
        time.sleep(0.1)

    def add_new_account(self):
        new_window = new_account_window(self.root, self.profile_manager)
        self.root.wait_window(new_window.newpage)
        self.root.deiconify()
        self.reload()

    def modify_account(self, data):
        new_window = new_account_window(
            self.root,
            self.profile_manager,
            data=data,
            modify=True
        )

        self.root.wait_window(new_window.newpage)
        self.root.deiconify()
        self.reload()

    def reload(self):
        self.current_page = 0
        self.cache = self.cache_manager.load_cache()
        self.load_all()

    def delete_account(self, profile):
        self.profile_manager.delete(profile["Riot_id"])
        self.reload()

    def right_click(self, profile, event):
        self.menu = ttk.Menu(self.root)
        self.menu.add_command(label='delete', command=lambda: self.delete_account(profile))
        self.menu.add_command(label="Modify", command=lambda: self.modify_account(profile))
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def quit_program(self):
        self.root.destroy()

    def move_app(self,e):
        self.root.geometry(f'+{e.x_root}+{e.y_root}')

class new_account_window:
    def __init__(self, root, profile_manager, data=None, modify=False):
        self.profile_manager = profile_manager
        self.root = root
        self.data = data

        self.newpage = tk.CTkToplevel(self.root)
        self.newpage.config(background='#010A13')
        self.root.withdraw()
        self.newpage.geometry("800x500")

        self.frame_entry = tk.CTkFrame(self.newpage, width=300, height=600, corner_radius=0, fg_color="#010A13")
        self.frame_entry.pack(anchor=tk.CENTER, expand=True)

        
        self.entry_riotID = tk.CTkEntry(self.frame_entry, width=300, height=50)
        self.entry_riotID.pack(pady=20)

        self.entry_username = tk.CTkEntry(self.frame_entry, width=300, height=50)
        self.entry_username.pack(pady=20)

        self.entry_password = tk.CTkEntry(self.frame_entry, width=300, height=50)
        self.entry_password.pack(pady=20)

        if data is not None:
            self.entry_riotID.insert(0, data["Riot_id"])
            self.entry_username.insert(0, data["Username"])
            self.entry_password.insert(0, data["Password"])
            self.old_riot_id = data["Riot_id"]


        if not modify:
            self.register_button = tk.CTkButton(self.newpage, text="🡢", font=tk.CTkFont(weight="bold", size=35), fg_color="#091428", bg_color="#010A13", hover_color="#0A1428", height=60, width=60, corner_radius=15, command=self.account_register)
            self.register_button.place(x=650, y=400)

        if data is not None:
            self.old_riot_id = data["Riot_id"]
            
        if modify:
            self.register_button = tk.CTkButton(
                self.newpage,
                text="🡢",
                font=tk.CTkFont(weight="bold", size=35),
                fg_color="#091428",
                bg_color="#010A13",
                hover_color="#0A1428",
                height=60,
                width=60,
                corner_radius=15,
                command=self.account_modify
            )
            self.register_button.place(x=650, y=400)


    def account_register(self):
        riot_id = self.entry_riotID.get()
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not riot_id or not username or not password:
            ttk.messagebox.showinfo("ERROR", "All fields must be filled")
            return

        riot_ids = [p["Riot_id"] for p in self.profile_manager.get_all()]
        if riot_id in riot_ids:
            ttk.messagebox.showinfo("ERROR", "Riot ID already registered")
            return

        self.profile_manager.add({
            "Riot_id": riot_id,
            "Username": username,
            "Password": password
        })

        self.newpage.destroy()


    def account_modify(self):
        riot_id = self.entry_riotID.get()
        username = self.entry_username.get()
        password = self.entry_password.get()

        self.profile_manager.update(
            self.old_riot_id,
            {
                "Riot_id": riot_id,
                "Username": username,
                "Password": password
            }
        )

        self.newpage.destroy()

if __name__ == "__main__":
    app = main_window()
    app.root.attributes('-topmost', True)
    app.root.attributes('-topmost', False)
    app.root.mainloop()