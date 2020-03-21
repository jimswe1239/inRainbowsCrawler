class Name:

    def __init__(self, first, middle, last):
        self.title = ""
        self.first = first.upper()
        self.middle = middle.upper()
        self.last = last.upper()
        self.suffix = ""

    def __init__(self, full):
        if(full[0:3].lower()) == "dr.":
            self.title = "Dr."
            full = full[3:]
        comma = full.split(",")
        segments = comma[0].split()
        self.first = segments[0]
        self.middle = " ".join(segments[1:-1])
        self.last = segments[-1]
        if(len(comma) > 1):
            self.suffix = comma[1]

    def __eq__(self, obj):
        return self.first == obj.first and self.middle == obj.middle and self.last == obj.last

    def __hash__(self):
        return hash(self.first+" "+self.middle+" "+self.last)

    def __str__(self):
        return self.first + (" " if len(self.middle) > 0 else "") + self.middle + " " + self.last
