import requests
import random
from bs4 import BeautifulSoup
# from writeToCSV import writeheader
import time
from Therapist import Therapist
from Name import Name
from Address import Address
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

# get this file from the firebase site project settings
cred = credentials.Certificate("creds/inrainbows-171a7-firebase-adminsdk-9htrh-c0a0a9f490.json")

firebase_admin.initialize_app(cred, {
  'projectId': "inrainbows-171a7",
})

db = firestore.client()


# user agent headers for requests
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}



def crawl(url, setOfNames):
    therapistsRemaining = True
    pnum = 1

    while(therapistsRemaining):
        print("PAGE", pnum)
        time.sleep(3 + random.random())
        r = requests.get(url, headers=headers)
        searchResults = r.text
        # begin parsing html with beautiful soup
        searchSoup = BeautifulSoup(searchResults, 'html.parser')
        listOfDivs = searchSoup.findAll("div", {"class": "result-row"})

        for div in listOfDivs:
            # time.sleep(5)
            name = extractName(div)
            print("  Name:", name)
            if str(name) not in setOfNames:

                doc_ref = db.collection('therapists').document(str(name))
                doc = doc_ref.get()

                if not doc.exists:
                    print("    scraping new data")
                    url = extractUrl(div)
                    time.sleep(3 + random.random())
                    r = requests.get(url, headers=headers)
                    pageSoup = BeautifulSoup(r.text, 'html.parser')

                    therapist = extractData(pageSoup)
                    writeToDB(therapist, doc_ref)
                else:
                    print("    name already found")

                fNames = open('names.txt', 'a')
                fNames.write(str(name)+"\n")
                fNames.close()
                setOfNames.add(str(name))
            else:
                print("name in SET")

        btnNexts = searchSoup.findAll("a", {"class": "btn-next"})
        if(len(btnNexts) == 0):
            therapistsRemaining = False
        else:
            url = btnNexts[0]['href']
            pnum += 1


    print("ending crawl")


def extractName(div):
    aName = div.find("a", {"class": "result-name"})
    spanName = aName.find("span")
    stringName = spanName.text
    name = Name(stringName)
    return name


def extractUrl(div):
    aName = div.find("a", {"class": "result-name"})
    url = aName["href"]
    return url


def extractData(soup):
    therapist = Therapist()

    name = soup.find("div", {"class": "name-title-column"})
    name = name.find("h1")
    name = Name(name.text.strip())
    therapist.name = name

    try:
        phone = soup.find("div", {"class": "profile-phone"})
        phone = phone.find("span")
        phone = phone.find("a")
        phone = phone.text.strip()
        therapist.phone = phone
    except(AttributeError):
        pass

    therapist.email = None  # Psychology Today does not make this data public
    therapist.website = None  # TODO, as Psychology Today only serves this data via a dynamic web crawler

    titles = []
    titleBlock = soup.find("div", {"class": "profile-title"})
    titleBlock = titleBlock.find("h2").findAll("span", {"data-ui-type": "glossary"})
    for title in titleBlock:
        txt = title.text.strip()
        titles += [txt]
    therapist.titles = titles

    blurb = ""
    paras = soup.findAll("div", {"class": "statementPara"})
    for p in paras:
        blurb += p.text.strip() + "\n"
    therapist.blurb = blurb

    try:
        div = soup.find("div", {"class": "location-address-phone"})
        lst = div.findAll("span")
        street = ""
        city = ""
        state = ""
        zipcode = ""
        for part in lst:
            try:
                if(part["itemprop"] == "streetAddress"):
                    street = part.text.strip()
                if(part["itemprop"] == "addressLocality"):
                    city = part.text.strip()[0:-1]
                if(part["itemprop"] == "addressRegion"):
                    state = part.text.strip()
                if(part["itemprop"] == "postalcode"):
                    zipcode = part.text.strip()
            except(KeyError):
                pass
        unitBlock = div.text
        try:
            unit = unitBlock.split(street)[1].split(city)[0].strip()
        except(ValueError):
            unit = ""

        therapist.address = Address(street, unit, city, state, zipcode)
    except(AttributeError):
        pass

    try:
        specialties = []
        lst = soup.find("ul", {"class": "specialties-list"})
        lst = lst.findAll("li")
        for spec in lst:
            txt = spec.text.strip()
            specialties += [txt]
        therapist.specialties = specialties
    except(AttributeError):
        pass

    try:
        issues = []
        lst = soup.find("div", {"class": "attributes-issues"})
        lst = lst.findAll("li")
        for issue in lst:
            txt = issue.text.strip()
            issues += [txt]
        therapist.issues = issues
    except(AttributeError):
        pass

    try:
        mentalHealth = []
        lst = soup.find("div", {"class": "attributes-mental-health"})
        lst = lst.findAll("li")
        for mh in lst:
            txt = mh.text.strip()
            mentalHealth += [txt]
        therapist.mentalHealth = mentalHealth
    except(AttributeError):
        pass

    try:
        sexuality = []
        lst = soup.find("div", {"class": "attributes-sexuality"})
        lst = lst.findAll("li")
        for x in lst:
            txt = x.text.strip()
            sexuality += [txt]
        therapist.sexuality = sexuality
    except(AttributeError):
        pass

    try:
        ages = []
        lst = soup.find("div", {"class": "attributes-age-focus"})
        lst = lst.findAll("li")
        for x in lst:
            txt = x.text.strip()
            ages += [txt]
        therapist.ages = ages
    except(AttributeError):
        pass

    try:
        communities = []
        lst = soup.find("div", {"class": "attributes-categories"})
        lst = lst.findAll("li")
        for x in lst:
            txt = x.text.strip()
            communities += [txt]
        therapist.communities = communities
    except(AttributeError):
        pass

    try:
        types = []
        lst = soup.find("div", {"class": "attributes-treatment-orientation"})
        lst = lst.findAll("li")
        for x in lst:
            txt = x.text.strip()
            types += [txt]
        therapist.types = types
    except(AttributeError):
        pass

    try:
        modality = []
        lst = soup.find("div", {"class": "attributes-modality"})
        lst = lst.findAll("li")
        for x in lst:
            txt = x.text.strip()
            modality += [txt]
        therapist.modality = modality
    except(AttributeError):
        pass

    try:
        video = []
        lst = soup.find("div", {"class": "attributes-online-therapy"})
        lst = lst.findAll("li")
        for x in lst:
            txt = x.text.strip()
            video += [txt]
        therapist.video = video
    except(AttributeError):
        pass

    try:
        lst = soup.find("div", {"class": "profile-qualifications"})
        lst = lst.findAll("li")
        for x in lst:
            key = x.text.split(":")[0].strip()
            val = x.text.split(":")[-1].strip()
            therapist.qualifications[key] = val
    except(AttributeError):
        pass

    try:
        lst = soup.find("div", {"class": "profile-finances"})
        lst = lst.find("ul").findAll("li")
        for x in lst:
            key = x.text.split(":")[0].strip()
            val = x.text.split(":")[-1].strip()
            therapist.finances[key] = val
    except(AttributeError):
        pass

    try:
        insurance = []
        lst = soup.find("div", {"class": "attributes-insurance"})
        lst = lst.findAll("li")
        for x in lst:
            txt = x.text.strip()
            insurance += [txt]
        therapist.insurance = insurance
    except(AttributeError):
        pass

    try:
        payBy = []
        lst = soup.find("div", {"class": "attributes-payment-method"})
        lst = lst.findAll("span")
        for x in lst:
            txt = x.text.strip()
            if txt[0] == ",":
                txt = txt[2:]
            if txt != "Pay By:":
                payBy += [txt]
        therapist.payBy = payBy
    except(AttributeError):
        pass

    return therapist


def writeToDB(therapist, doc_ref):
    doc_ref.set({
        'name': therapist.name.toDict(),
        'phone': therapist.phone,
        'email': therapist.email,
        'website': therapist.website,
        'titles': therapist.titles,
        'blurb': therapist.blurb,
        'address': therapist.address.toDict(),
        'specialties': therapist.specialties,
        'issues': therapist.issues,
        'mentalHealth': therapist.mentalHealth,
        'sexuality': therapist.sexuality,
        'ages': therapist.ages,
        'communities': therapist.communities,
        'types': therapist.types,
        'modality': therapist.modality,
        'video': therapist.video,
        'qualifications': therapist.qualifications,
        'finances': therapist.finances,
        'payBy': therapist.payBy,
        'insurance': therapist.insurance
    })

# make calls to crawl(urlString)

listOfUrls = [

]

for x in listOfUrls:
    setOfNames = set()

    with open('names.txt') as f:
        read_data = f.read()
        for row in read_data.split("\n"):
            setOfNames.add(row)
    crawl(x, setOfNames)
