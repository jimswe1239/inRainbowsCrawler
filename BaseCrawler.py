import requests
import random
from bs4 import BeautifulSoup
# from writeToCSV import writeheader
import time
from Therapist import Therapist
from Name import Name
from Address import Address

# user agent headers for requests
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

# write headers for csv file
# writeheader()

# verify if we have already seen record
setOfNames = {}


def crawl(url):
    therapistsRemaining = True
    pnum = 1
    goal = 3
    while(therapistsRemaining and pnum <= goal):
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
            if name not in setOfNames:
                print("    scraping new data")
                url = extractUrl(div)
                time.sleep(3 + random.random())
                r = requests.get(url, headers=headers)
                pageSoup = BeautifulSoup(r.text, 'html.parser')

                therapist = extractData(pageSoup)
            else:
                print("    name already found")

        btnNexts = searchSoup.findAll("a", {"class": "btn-next"})
        if(len(btnNexts) == 0):
            therapistsRemaining = False
        else:
            url = btnNexts[0]['href']
            pnum = 2

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

    print(therapist)
    return therapist


# make calls to crawl(urlString)
crawl("https://www.psychologytoday.com/us/therapists/lesbian/ma/boston?sid=5e763cc7a0a78")
