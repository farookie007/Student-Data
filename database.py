import glob
import pandas as pd
import sqlalchemy as db
from typing import List, Dict


engine = db.create_engine('sqlite:///data.db')
meta = db.MetaData(engine)


students = db.Table('students', meta,
                    db.Column('id', db.String(10), primary_key=True),
                    db.Column('password', db.String(60), nullable=False),
                    db.Column('email', db.String, nullable=False, unique=True))

results = db.Table('results', meta,
                   db.Column('id', db.String(14), primary_key=True),
                   db.Column('level', db.String(3), nullable=False),
                   db.Column('student_id', db.String(10), db.ForeignKey('students.id')),
                   db.Column('html', db.Text, nullable=False))


def _get_result_files() -> List:
    """This private function gets the HTML files from the `results` folder
    in the root directory and returns a list of the filenames."""
    files = glob.glob('.\\results\\*.html')
    return files


# noinspection PyUnresolvedReferences
def upload(matric_no: str):
    """This function uploads only the data of the current user into database
    by filtering using the `matric_no`."""
    files = _get_result_files()
    values = (_get_values(file) for file in files)
    for value in values:
        id_, level, st_id, html = value.values()
        # noinspection PyUnresolvedReferences
        if st_id == matric_no:  # checks if the `matric_no` is the same as the student id
            with engine.begin() as conn:
                try:
                    ins = results.insert().\
                        values(id=id_, level=level, student_id=st_id, html=html)
                    conn.execute(ins)
                except db.exc.IntegrityError:
                    upd = results.update().where(results.c.id == id_). \
                        values(level=level, student_id=st_id, html=html)
                    conn.execute(upd)


def _get_values(filepath: str) -> Dict:
    st_id, _, _, _, level = pd.read_html(filepath)[0][1]
    with open(filepath) as f:
        content = f.read()
    return {'id': st_id+'-'+level, 'level': level, 'student_id': st_id, 'content': content}


def refresh():
    """This function refresh the database by updating the existing results or adding new results
    to the database using all the results HTML files in the `results` folder from root directory."""
    files = _get_result_files()
    values = (_get_values(file) for file in files)
    for value in values:
        id_, level, st_id, html = value.values()
        # noinspection PyUnresolvedReferences
        with engine.begin() as conn:
            # noinspection PyUnresolvedReferences
            try:
                ins = results.insert().\
                    values(id=id_, level=level, student_id=st_id, html=html)
                conn.execute(ins)
            except db.exc.IntegrityError:
                upd = results.update().where(results.c.id == id_). \
                    values(level=level, student_id=st_id, html=html)
                conn.execute(upd)


def __burn_database():  # I only use this when I want to clear out the database
    """This function deletes all the data in the database :class: MetaData and leaves an empty table
    in the database."""
    meta.drop_all()
    meta.create_all()
