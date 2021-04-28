# CREATING_COLLECTIONS_TABLE = """
#     CREATE TABLE IF NOT EXISTS collections(
#         collection_id INTEGER PRIMARY KEY,
#         name TEXT NOT NULL,
#     );
# """

_CREATING_TABLE_SKILLS = """
    CREATE TABLE IF NOT EXISTS skills(
        skill_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        stats INTEGER DEFAULT 0,
        steps INTEGER DEFAULT 0);
"""

INSERT_INTO_SKILLS = """
    INSERT
        INTO skills(name)
        VALUES(?)
"""

SELECT_ALL_SKILLS = """
    SELECT name, stats
    FROM skills
"""

SELECT_FROM_SKILLS = """
    SELECT stats, steps
        FROM skills
    WHERE name=?
"""

UPDATE_STATS_SKILLS = """
    UPDATE skills
        SET stats=?
    WHERE name=?
"""

UPDATE_RENAME_SKILLS = """
    UPDATE skills
        SET name=?
    WHERE name=?
"""

UPDATE_STEPS_SKILLS = """
    UPDATE skills
        SET steps=?
    WHERE name=?
"""

DELETE_FROM_SKILLS = """
    DELETE FROM skills
    WHERE name=?
"""

_CREATING_TABLE_STEPS = """
    CREATE TABLE IF NOT EXISTS steps(
        step_id INTEGER PRIMARY KEY,
        skill_id INTEGER NOT NULL,
        step_order INTEGER NOT NULL,
        objective TEXT NOT NULL,
        FOREIGN KEY (skill_id)
            REFERENCES skills (skill_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION);
"""

INSERT_INTO_STEPS = """
    INSERT
        INTO steps(skill_id, step_order, objective)
        VALUES(
            (SELECT skill_id
                FROM skills
                WHERE name=?),?,?)
"""

# SELECT_FROM_STEPS = """
#     SELECT name, step_order, objective, url
#         FROM steps
#         JOIN skills
#         USING(SELECT skill_id
#                 FROM skills
#             WHERE name=?)
#         JOIN urls
#         USING(step_id,
#             (SELECT skill_id
#                 FROM skills
#             WHERE name=?))
#     WHERE skill_id=(
#         SELECT skill_id
#             FROM skills
#         WHERE name=?)
# """

SELECT_FROM_STEPS = """
    SELECT name, step_order, objective, url
    FROM skills
    JOIN steps
        USING(skill_id)
    JOIN urls
        USING(skill_id)
    WHERE name=?
"""

_CREATING_TABLE_NOTES = """
    CREATE TABLE IF NOT EXISTS notes(
        note_id INTEGER PRIMARY KEY,
        skill_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        FOREIGN KEY (skill_id)
            REFERENCES skills (skill_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION);
"""

INSERT_INTO_NOTES = """
    INSERT
        INTO notes(skill_id, text)
        VALUES(
            (SELECT skill_id
                FROM skills
                WHERE name=?),?)
"""

SELECT_FROM_NOTES = """
    SELECT note_id, text
        FROM notes
    WHERE skill_id=((SELECT skill_id
                FROM skills
                WHERE name=?))
"""

DELETE_FROM_NOTES = """
    DELETE FROM notes
    WHERE note_id=?
"""

_CREATING_TABLE_URLS = """
    CREATE TABLE IF NOT EXISTS urls(
        url_id INTEGER PRIMARY KEY,
        skill_id INTEGER NOT NULL,
        step_id INTEGER,
        url TEXT NOT NULL,
        FOREIGN KEY (skill_id)
            REFERENCES skills (skill_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION,
        FOREIGN KEY (step_id)
            REFERENCES steps (step_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION);
"""

INSERT_INTO_URLS = """
    INSERT
        INTO urls(skill_id, step_id, url)
        VALUES(
            (SELECT skill_id
                FROM skills
                WHERE name=?),
            (SELECT step_id FROM steps
                WHERE
                    skill_id=(SELECT skill_id FROM skills WHERE name=?)
                    AND step_order=?),?)
"""

SELECT_SKILL_URLS = """
    SELECT url
        FROM urls
    WHERE skill_id=(
        SELECT skill_id
            FROM skills
        WHERE name=?)
        AND step_id is NULL
"""

CREATING_TABLE_QUERIES = [
    # CREATING_COLLECTIONS_TABLE,
    _CREATING_TABLE_SKILLS,
    _CREATING_TABLE_NOTES,
    _CREATING_TABLE_STEPS,
    _CREATING_TABLE_URLS,
]