from opgg.opgg import OPGG
from opgg.params import Region
import time 

class DataManager:
    def __init__(self):
        self.opgg = OPGG()

    def fetch_data(self,riot_id):
        opgg_data= self.opgg.search(riot_id, Region.EUW)
        summoner_data = opgg_data[0].summoner
        solo_rank = next((league for league in summoner_data.league_stats if league.game_type == "SOLORANKED"), None)
        image_url = summoner_data.profile_image_url
        last_request_time = time.time()

        summoner_data_dic = {
            "image_url": str(image_url),
            "last_request_time":last_request_time,
            "opgg_data": {
                "tier": solo_rank.tier_info.tier,
                "division": solo_rank.tier_info.division,
                "lp": solo_rank.tier_info.lp,
            }
         }
        
        return summoner_data_dic
