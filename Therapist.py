class Therapist:

    def __init__(self):
        self.generatedID = None
        self.name = None
        self.phone = None
        self.email = None
        self.website = None
        self.titles = []
        self.blurb = None
        self.address = None
        self.specialties = []
        self.issues = []
        self.mentalHealth = []
        self.sexuality = []
        self.ages = []
        self.communities = []
        self.types = []
        self.modality = []
        self.video = []
        self.qualifications = dict()
        self.finances = dict()


    def setID(self):
        self.generatedID = hash(self.name+self.phone)

    def __str__(self):  # for testing
        ret = ""
        ret = ret + "Name: " + str(self.name) + "\n"
        ret = ret + "Phone: " + str(self.phone) + "\n"
        # ret = ret + "Email: " + str(self.email) + "\n"
        # ret = ret + "Website: " + str(self.website) + "\n"
        for x in self.titles:
            ret = ret + "  Title: " + str(x) + "\n"
        for x in self.blurb.split("\n"):
            ret = ret + "  Blurb paragraph: " + str(x[0:20]) + "...\n"
        ret = ret + "Address: " + str(self.address) + "\n"
        for x in self.specialties:
            ret = ret + "  Specialty: " + str(x) + "\n"
        for x in self.issues:
            ret = ret + "  Issue: " + str(x) + "\n"
        for x in self.mentalHealth:
            ret = ret + "  Mental Health: " + str(x) + "\n"
        for x in self.sexuality:
            ret = ret + "  Sexuality: " + str(x) + "\n"
        for x in self.ages:
            ret = ret + "  Age: " + str(x) + "\n"
        for x in self.communities:
            ret = ret + "  Community: " + str(x) + "\n"
        for x in self.types:
            ret = ret + "  Type: " + str(x) + "\n"
        for x in self.modality:
            ret = ret + "  Modality: " + str(x) + "\n"
        for x in self.video:
            ret = ret + "  Video: " + str(x) + "\n"
        ret = ret + "Qualifications: " + str(self.qualifications) + "\n"
        ret = ret + "Finances: " + str(self.finances) + "\n"

        return ret

