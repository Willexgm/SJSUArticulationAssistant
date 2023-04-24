from helper_classes import CCCourse, SJSUCourse, GE, CommunityCollege
from scraper import get_community_colleges, get_ges, get_course_equivalencies, get_ge_equivalencies
import database


def scrape_cc_into_db():
    for cc in get_community_colleges():
        database.insert_into_CC(cc.full_name, cc.url_name)


def scrape_ge_into_db():
    for ge in get_ges():
        database.insert_into_SJSUGenEd(ge.code, ge.name)


def scrape_course_eq_into_db(cc: CommunityCollege):
    eqs = get_course_equivalencies(cc)
    ccid = database.select_id_from_cc(cc.full_name, cc.url_name)

    for eq in eqs:
        database.insert_into_SJSUCourses(eq.prefix, eq.number, eq.title)
        sjsucourseid = database.select_id_from_sjsucourse(eq.prefix, eq.number, eq.title)
        if eqs[eq] is None:
            continue

        for set_id, val in enumerate(eqs[eq]):
            for x in val:
                database.insert_into_CCCourses(ccid, x.prefix, x.number, x.title)
                cccourseid = database.select_id_from_cccourse(ccid, x.prefix, x.number, x.title)
                database.insert_into_CToCEq(sjsucourseid, cccourseid, set_id)


def scrape_ge_eq_into_db(cc: CommunityCollege):
    eqs = get_ge_equivalencies(cc)
    if eqs is None:
        return
    ccid = database.select_id_from_cc(cc.full_name, cc.url_name)

    for eq in eqs:
        if eqs[eq] is None: continue
        for ccc in eqs[eq]:
            database.insert_into_CCCourses(ccid, ccc.prefix, ccc.number, "")
            cccid = database.select_id_from_cccourse(ccid, ccc.prefix, ccc.number, ccc.title)
            database.insert_into_GEEq(eq.code, cccid, 0)


if __name__ == '__main__':
    database.init_database()
    scrape_ge_into_db()
    print("Scraped GEs.")
    scrape_cc_into_db()
    print("Scraped CCs.")
    print("\nScraping Equivalencies...\n")
    for cc in get_community_colleges():
        scrape_course_eq_into_db(cc)
        scrape_ge_eq_into_db(cc)
        print(f"Scraped {cc.full_name}.")
    print("\nScraped Equivalencies.\n")
