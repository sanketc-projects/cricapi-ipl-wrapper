class Team:
    def __init__(self, team_name):
        self.name = team_name
        # short name is the acronym of the team name
        self.short_name  = "".join([word[0].upper() for word in team_name.split() if word])

        if (self.short_name == "PK"):
            self.short_name = "PBKS"
        elif (self.short_name == "SH"):
            self.short_name = "SRH"

    def __str__(self):
        return f"{self.short_name:<4} - {self.name}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Team):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)