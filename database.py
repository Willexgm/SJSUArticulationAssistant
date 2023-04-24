import sqlite3

connection = sqlite3.connect('database_0.db')


def set_connection(conn):
    global connection
    connection = conn


# Decorator to skip the function call if we are trying to insert an entity that already exists.
def unique_skip(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" not in str(e):
                raise e
    return wrapper


def init_database():
    c = connection.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS CC (
          CCID INTEGER PRIMARY KEY,
          Name TEXT,
          URL TEXT,
          UNIQUE (Name, URL)
        );
        
        CREATE TABLE IF NOT EXISTS CCCourses (
          CCCourseID INTEGER PRIMARY KEY,
          CCID INTEGER REFERENCES CC(CCID),
          Prefix TEXT,
          Number Text,
          Title Text,
          UNIQUE (CCID, Prefix, Number, Title)
        );
        
        CREATE TABLE IF NOT EXISTS SJSUCourses (
          SJSUCourseID INTEGER PRIMARY KEY,
          Prefix TEXT,
          Number Text,
          Title Text,
          UNIQUE (Prefix, Number, Title)
        );
        
        CREATE TABLE IF NOT EXISTS SJSUGenEd (
          Code TEXT PRIMARY KEY,
          Name TEXT
        );
        
        CREATE TABLE IF NOT EXISTS CToCEq (
          SJSUCourseID INTEGER REFERENCES SJSUCourses(SJSUCourseID),
          CCCourseID INTEGER REFERENCES CCCourses(CCCourseID),
          SetID INTEGER,
          PRIMARY KEY (SJSUCourseID, CCCourseID, SetID)
        );
        
        CREATE TABLE IF NOT EXISTS GEEq (
          Code TEXT REFERENCES SJSUGenEd(Code),
          CCCourseID INTEGER REFERENCES CCCourses(CCCourseID),
          SetID INTEGER,
          PRIMARY KEY (Code, CCCourseID, SetID)
        );
    ''')
    connection.commit()
    c.close()


@unique_skip
def insert_into_CC(Name, URL):
    c = connection.cursor()
    c.execute("INSERT INTO CC (Name, URL) VALUES (?, ?)", (Name, URL))
    connection.commit()
    c.close()


def select_id_from_cc(name, URL):
    c = connection.cursor()
    c.execute("SELECT CCID FROM CC WHERE name=? AND URL=?", (name,URL))
    row = c.fetchone()
    c.close()
    return row[0]


def select_all_from_CC():
    c = connection.cursor()
    c.execute("SELECT * FROM CC")
    rows = c.fetchall()
    c.close()
    return rows


@unique_skip
def insert_into_CCCourses(CCID, Prefix, Number, Title):
    c = connection.cursor()
    c.execute("INSERT INTO CCCourses (CCID, Prefix, Number, Title) VALUES (?, ?, ?, ?)", (CCID, Prefix, Number, Title))
    connection.commit()
    c.close()
    return c.lastrowid


def select_all_from_CCCourses():
    c = connection.cursor()
    c.execute("SELECT * FROM CCCourses")
    rows = c.fetchall()
    c.close()
    return rows


def select_id_from_cccourse(CCID, Prefix, Number, Title):
    c = connection.cursor()
    if Title is None:
        c.execute("SELECT CCCourseID FROM CCCourses WHERE CCID=? AND Prefix=? AND Number=?", (CCID, Prefix, Number))
    else:
        c.execute("SELECT CCCourseID FROM CCCourses WHERE CCID=? AND Prefix=? AND Number=? AND Title=?", (CCID, Prefix, Number, Title))
    row = c.fetchone()
    c.close()
    return row[0]


@unique_skip
def insert_into_SJSUCourses(Prefix, Number, Title):
    c = connection.cursor()
    c.execute("INSERT INTO SJSUCourses (Prefix, Number, Title) VALUES (?, ?, ?)", (Prefix, Number, Title))
    connection.commit()
    c.close()
    return c.lastrowid


def select_all_from_SJSUCourses():
    c = connection.cursor()
    c.execute("SELECT * FROM SJSUCourses")
    rows = c.fetchall()
    c.close()
    return rows


@unique_skip
def select_id_from_sjsucourse(Prefix, Number, Title):
    c = connection.cursor()
    c.execute("SELECT SJSUCourseID FROM SJSUCourses WHERE Prefix=? AND Number=? AND Title=?", (Prefix, Number, Title))
    row = c.fetchone()
    c.close()
    return row[0]


@unique_skip
def insert_into_SJSUGenEd(Code, Name):
    c = connection.cursor()
    c.execute("INSERT INTO SJSUGenEd (Code, Name) VALUES (?, ?)", (Code, Name))
    connection.commit()
    c.close()


def select_all_from_SJSUGenEd():
    c = connection.cursor()
    c.execute("SELECT * FROM SJSUGenEd")
    rows = c.fetchall()
    c.close()
    return rows


@unique_skip
def insert_into_CToCEq(SJSUCourseID, CCCourseID, SetID):
    c = connection.cursor()
    c.execute("INSERT INTO CToCEq (SJSUCourseID, CCCourseID, SetID) VALUES (?, ?, ?)", (SJSUCourseID, CCCourseID, SetID))
    connection.commit()
    c.close()


def select_all_from_CToCEq():
    c = connection.cursor()
    c.execute("SELECT * FROM CToCEq")
    rows = c.fetchall()
    c.close()
    return rows


@unique_skip
def insert_into_GEEq(Code, CCCourseID, SetID):
    c = connection.cursor()
    c.execute("INSERT INTO GEEq (Code, CCCourseID, SetID) VALUES (?, ?, ?)", (Code, CCCourseID, SetID))
    connection.commit()
    c.close()


def select_all_from_GEEq():
    c = connection.cursor()
    c.execute("SELECT * FROM GEEq")
    rows = c.fetchall()
    c.close()
    return rows


def join_from_CToCEq(sjsu_course_id):
    c = connection.cursor()
    c.execute("SELECT CToCEq.SetID, CCCourses.Prefix, CCCourses.Number, CCCourses.Title, CC.Name FROM CToCEq "
              "JOIN SJSUCourses ON CToCEq.SJSUCourseID = SJSUCourses.SJSUCourseID "
              "JOIN CCCourses ON CToCEq.CCCourseID = CCCourses.CCCourseID "
              "JOIN CC ON CCCourses.CCID = CC.CCID "
              "WHERE CToCEq.SJSUCourseID = ?", (sjsu_course_id,))
    rows = c.fetchall()
    c.close()
    return rows


def join_from_GEEq(code):
    c = connection.cursor()
    c.execute("SELECT CCCourses.Prefix, CCCourses.Number, CCCourses.Title, CC.Name FROM GEEq "
              "JOIN CCCourses ON GEEq.CCCourseID = CCCourses.CCCourseID "
              "JOIN CC ON CCCourses.CCID = CC.CCID "
              "WHERE GEEq.Code = ?", (code,))
    rows = c.fetchall()
    c.close()
    return rows
