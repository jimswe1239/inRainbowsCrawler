class Address:

    def __init__(self):
        self.street = ""
        self.unit = ""
        self.city = ""
        self.state = ""
        self.zipcode = ""
        self.country = ""

    def __init__(self, street, unit, city, state, zipcode):  # USA only
        self.street = street
        self.unit = unit
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.country = "USA"

    def __eq__(self, obj):
        return self.street == obj.street and self.unit == obj.unit and self.city == obj.city and self.state == obj.state

    def __str__(self):
        return self.street+"\n" + self.unit + ("\n" if len(self.unit) > 0 else "") + self.city + ", " + self.state + " " + self.zipcode

    def toDict(self):
        return {"street": self.street, "unit": self.unit, "city": self.city, "state": self.state, "zipcode": self.zipcode}
