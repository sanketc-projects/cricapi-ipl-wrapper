class Venue:
    def __init__(self, venue_name_full):
        # venue name is of the format "Satdium Name, City"
        venue_name_split = venue_name_full.split(",")
        self.name = venue_name_split[0].strip()
        self.city = venue_name_split[1].strip() if len(venue_name_split) > 1 else ""
        self.__full_name = venue_name_full

    def __str__(self):
        return self.__full_name

    def __repr__(self):
        return self.__full_name

    def __eq__(self, other):
        if isinstance(other, Venue):
            return self.name == other.name and self.city == other.city
        return False

    def __hash__(self):
        return hash((self.name, self.city))