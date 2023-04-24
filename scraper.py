import requests
from bs4 import BeautifulSoup
import bs4
from typing import List, Dict
from helper_classes import CCCourse, SJSUCourse, GE, CommunityCollege


def get_community_colleges():
    ccs = []
    soup = BeautifulSoup(requests.get(f"http://transfer.sjsu.edu/web-dbgen/artic/all-course-to-course.html").content,
                         "html.parser")
    tds = soup.find_all("table", attrs={"class": "info-table"})[1].find_all("a")
    for td in tds:
        ccs.append(
            CommunityCollege(td.text,
                             td["href"].replace("/web-dbgen/artic/", "").replace("/course-to-course.html", "")))

    return ccs


def _get_relevant_tr(cc: CommunityCollege) -> List[bs4.element.Tag]:
    soup = BeautifulSoup(requests.get(cc.c_to_c_url()).content, "html.parser")

    table = soup.find_all("table", attrs={"class": "info-table"})[1]
    rows = []
    for tr in table.find_all("tr"):
        if tr.has_attr("style"):
            continue
        bad_tr = False
        for td in tr.find_all("td"):
            bad_tr = False
            if not td.has_attr("valign"):
                bad_tr = True
                continue
        if bad_tr:
            continue
        rows.append(tr)

    return rows


def get_course_equivalencies(cc: CommunityCollege) -> Dict:
    course_eqs = {}
    for tr in _get_relevant_tr(cc):
        tds = tr.find_all("td")
        key = _str_to_sjsu_course(tds[0].text)
        for td in tds[2:]:
            if td.text == "No Current Equivalent":
                course_eqs[key] = None
            else:
                course_eqs[key] = [list(map(_str_to_cc_course, x.split("\xa0\xa0\xa0AND"))) for x in
                                   td.text.split("\xa0\xa0\xa0OR")]
    return course_eqs


def _str_to_cc_course(s: str) -> CCCourse:
    spl = s.split(" ")
    return CCCourse(spl[0], spl[1], " ".join(spl[2:]))


def _str_to_sjsu_course(s: str) -> SJSUCourse:
    spl = s.split(" ")
    return SJSUCourse(spl[0], spl[1], " ".join(spl[2:]))


def get_ges() -> List[GE]:
    return [
        GE("A1", "Oral Communication"),
        GE("A2", "Written Communication"),
        GE("A3", "Critical Thinking"),
        GE("B1", "Physical Science"),
        GE("B2", "Life Science"),
        GE("B3", "Laboratory Activity"),
        GE("B4", "Mathematics/Quantitative Reasoning"),
        GE("C1", "Arts (Art, Cinema, Dance, Music, Theatre)"),
        GE("C2", "Humanities (Literature, Philosophy, Languages Other than English)"),
        GE("D-1", "Sociology"),
        GE("D1", "Anthropology and Archaeology"),
        GE("D2", "Economics"),
        GE("D3", "Ethnic Studies"),
        GE("D4", "Gender Studies"),
        GE("D5", "Geography"),
        GE("D6", "History"),
        GE("D7", "Interdisciplinary Social or Behavioral Science"),
        GE("D8", "Political Science, Government and Legal Institutions"),
        GE("D9", "Psychology"),
        GE("D0", "Sociology and Criminology"),
        GE("E", "Lifelong Understanding and Self-Development"),
        GE("F", "Ethnic Studies"),
        GE("US1", "U.S. History"),
        GE("US2", "U.S. Constitution"),
        GE("US3", "California Government")
    ]


def get_ge_equivalencies(cc: CommunityCollege) -> Dict:
    soup = BeautifulSoup(requests.get(cc.ge_url()).content, "html.parser")

    if soup.find("td", string="American Institutions (US-1-2-3)") is None:
        return

    if soup.find("td", string="D--1: Sociology") is None:
        return

    eqs = {
        GE("A1", "Oral Communication"): _string_to_course_list(soup.find("td", string="A-1: Oral Communication").find_next("td").text),
        GE("A2", "Written Communication"): _string_to_course_list(soup.find("td", string="A-2: Written Communication").find_next("td").text),
        GE("A3", "Critical Thinking"): _string_to_course_list(soup.find("td", string="A-3: Critical Thinking").find_next("td").text),
        GE("B1", "Physical Science"): _string_to_course_list(soup.find("td", string="B-1: Physical Science").find_next("td").text),
        GE("B2", "Life Science"): _string_to_course_list(soup.find("td", string="B-2: Life Science").find_next("td").text),
        GE("B3", "Laboratory Activity"): _string_to_course_list(soup.find("td", string="B-3: Laboratory Activity").find_next("td").text),
        GE("B4", "Mathematics/Quantitative Reasoning"): _string_to_course_list(soup.find("td", string="B-4: Mathematics/Quantitative Reasoning").find_next("td").text),
        GE("C1", "Arts (Art, Cinema, Dance, Music, Theatre)"): _string_to_course_list(soup.find("td", string="C-1: Arts (Art, Cinema, Dance, Music, Theatre)").find_next("td").text),
        GE("C2", "Humanities (Literature, Philosophy, Languages Other than English)"): _string_to_course_list(soup.find("td", string="C-2: Humanities (Literature, Philosophy, Languages Other than English)").find_next("td").text),
        GE("D-1", "Sociology"): _string_to_course_list(soup.find("td", string="D--1: Sociology").find_next("td").text),
        GE("D1", "Anthropology and Archaeology"): _string_to_course_list(soup.find("td", string="D-1: Anthropology and Archaeology").find_next("td").text),
        GE("D2", "Economics"): _string_to_course_list(soup.find("td", string="D-2: Economics").find_next("td").text),
        GE("D3", "Ethnic Studies"): _string_to_course_list(soup.find("td", string="D-3: Ethnic Studies").find_next("td").text),
        GE("D4", "Gender Studies"): _string_to_course_list(soup.find("td", string="D-4: Gender Studies").find_next("td").text),
        GE("D5", "Geography"): _string_to_course_list(soup.find("td", string="D-5: Geography").find_next("td").text),
        GE("D6", "History"): _string_to_course_list(soup.find("td", string="D-6: History").find_next("td").text),
        GE("D7", "Interdisciplinary Social or Behavioral Science"): _string_to_course_list(soup.find("td", string="D-7: Interdisciplinary Social or Behavioral Science").find_next("td").text),
        GE("D8", "Political Science, Government and Legal Institutions"): _string_to_course_list(soup.find("td", string="D-8: Political Science, Government and Legal Institutions").find_next("td").text),
        GE("D9", "Psychology"): _string_to_course_list(soup.find("td", string="D-9: Psychology").find_next("td").text),
        GE("D0", "Sociology and Criminology"): _string_to_course_list(soup.find("td", string="D-0: Sociology and Criminology").find_next("td").text),
        GE("E", "Lifelong Understanding and Self-Development"): _string_to_course_list(soup.find("td", string="Area E: Lifelong Understanding and Self-Development").find_all_next("td")[2].text),
        GE("F", "Ethnic Studies"): _string_to_course_list(soup.find("td", string="Area F: Ethnic Studies").find_all_next("td")[2].text),
    }

    us1 = []
    us2 = []
    us3 = []
    t = soup.find("td", string="American Institutions (US-1-2-3)").find_next("td")
    while t is not None:
        try:
            t = t.find_next("td")
            if t is None or "California Challenge Exam" in t.text:
                break
            spl = t.text.split("-")
            if len(spl[0].split(" ")) < 2:
                continue
            pre = spl[0].split(" ")[0].strip(" ")
            num = spl[0].split(" ")[1].strip(" ")

            if "US 1" in spl[1]:
                us1.append(CCCourse(pre, num, None))
            if "US 2" in spl[1]:
                us2.append(CCCourse(pre, num, None))
            if "US 3" in spl[1]:
                us3.append(CCCourse(pre, num, None))
        except:
            pass

    eqs[GE("US1", "U.S. History")] = us1
    eqs[GE("US2", "U.S. Constitution")] = us2
    eqs[GE("US3", "California Government")] = us3

    return eqs


def _string_to_course_list(s: str):
    spl = s.split(";")
    for i in range(len(spl)):
        spl[i] = spl[i].strip(". ")

    if len(spl) == 1 and len(spl[0]) >= 20:
        return None

    n = []
    for x in spl:
        prefix = x.split(" ")[0]
        if len(prefix) >= 9:
            return None
        x = x[len(prefix)+1:]

        for y in x.split(" "):
            y = y.replace(",","")
            if len(y) == 0 or not y[0].isnumeric():
                continue
            n.append(CCCourse(prefix, y, None))
    return n

# get_community_colleges()

# get_ges()

