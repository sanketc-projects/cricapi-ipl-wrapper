class HitInfo:
    def __init__(self):
        self.hits_today = 0
        self.hits_used = 0
        self.hits_limit = 100

    def __str__(self):
        return f"Hits Today: {self.hits_today} Hits Used: {self.hits_used} Hits Limit: {self.hits_limit}"

    def __repr__(self):
        return self.__str__()

hits = HitInfo()

def get_hits_info():
    return hits

def update_hits_info(info):
    global hits
    hits.hits_today = info.get("hitsToday", 0)
    hits.hits_used = info.get("hitsUsed", 0)
    hits.hits_limit = info.get("hitsLimit", 100)