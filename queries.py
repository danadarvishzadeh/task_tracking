# CREATING_COLLECTIONS_TABLE = """
#     CREATE TABLE IF NOT EXISTS collections(
#         collection_id INTEGER PRIMARY KEY,
#         name TEXT NOT NULL,
#     );
# """

_CREATING_SKILLS_TABLE = """
    CREATE TABLE IF NOT EXISTS skills(
        skill_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        stats INTEGER DEFAULT 0,
        url TEXT,
        collection_id INTEGER,
        FOREIGN KEY (collection_id)
            REFERENCES collections (collection_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION);
"""

_CREATING_NOTES_TABLE = """
    CREATE TABLE IF NOT EXISTS notes(
        note_id INTEGER PRIMARY KEY,
        text TEXT NOT NULL,
        skill_id INTEGER NOT NULL,
        FOREIGN KEY (skill_id)
            REFERENCES skills (skill_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION);
"""


CREATING_TABLE_QUERIES = [
    # CREATING_COLLECTIONS_TABLE,
    _CREATING_SKILLS_TABLE,
    _CREATING_NOTES_TABLE
]


SKILL_LOAD_QUERY = """
    SELECT
        skill_id,
        stats,
        url
    FROM
        skills
    WHERE
        name=?
"""

SKILL_INSERT_QUERY = """
    INSERT
        INTO skills (name)
    VALUES (?)
"""

GET_ALL_SKILLS = """
    SELECT
        name,
        stats
    FROM
        skills
"""

ADD_STATS = """
    UPDATE
        skills
    SET
        stats=?
    WHERE
        name=?
"""

SET_URL = """
    UPDATE
        skills
    SET
        url=?
    WHERE
        name=?
"""

NOTE_INSERT_QUERY = """
    INSERT
        INTO notes (text, skill_id)
    VALUES (?, ?)
"""

GET_SKILL_NOTES = """
    SELECT
        note_id,
        text
    FROM
        notes
    WHERE
        skill_id=?
"""

SKILL_DELETE_QUERY = """
    DELETE
        FROM skills
    WHERE 
        name=?
"""


NOTE_DELETE_QUERY = """
    DELETE
        FROM notes
    WHERE
        note_id=?
"""

SKILL_RENAME_QUERY = """
    UPDATE
        skills
    SET
        name=?
    WHERE
        name=?
"""