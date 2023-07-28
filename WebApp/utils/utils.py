import re
import io
import pandas as pd

from typing import Dict, Tuple




def get_semester(df):
    """Gets and return the semester of the result as an
    integer from the dataframe."""
    course = df.index[0]
    course_title = df.loc[course]['Title']
    if "SWEP" in course_title:
        return 3
    last_dgt = int(course[-1])
    return 2 if last_dgt % 2 == 0 else 1


def parse_result_html(file) -> Tuple:
    """
    This function parses the HTML file containing the results of a Student (esp. University of Ilorin)
    into a pandas DataFrame and creates a Semester object for each individual semester contained in the result.
    Ensure the HTML files are stored in a folder named 'results' and the filenames are named in ascending order 
    according to their corresponding years to enable the function locate it.
    :return: List[pandas.DataFrame]
    """
    grade = {
        'A': 5,
        'B': 4,
        'C': 3,
        'D': 2,
        'E': 1,
        'F': 0
        }
    # the original names of the variables
    # matric, name, fac, dept, level = pd.read_html(file)[0][1]
    _, _, fac, _, level = pd.read_html(file)[0][1]
    
    # extracting the session id
    # decoding the `file` object which is an io.BytesIO object
    # content = file.getvalue().decode()
    # session = re.search('\d\d\d\d/\d\d\d\d', content).group()
    session = '2017/2018'

    dfs = pd.read_html(file, header=1, index_col=1)
    for df in dfs[1:]:
        df.drop(columns=['Unnamed: 9', 'S/No.'], index='Total', inplace=True)
        df.dropna(inplace=True)
        if fac == 'Engineering and Technology' and level == '100':
            # This handles the complications with Engineering and Technology 100L results where only GNS matters.
            df.drop(labels=[title for title in df.index if not title.startswith('GNS')], axis=0, inplace=True)
        df['Gradient'] = pd.Series(
            [df.loc[f]['Unit'] * grade[df.loc[f]['Grade']] for f in df.index],
            index=df.index,
            dtype='int8'
            )

    return dfs[1:], session, level


def calculate_gpa(df: pd.DataFrame) -> float:
    """Calculates the GPA of a semester result.
    params:
        df: pandas.DataFrame object
    returns:
        Returns the GPA as a floating point number."""
    gradients = df['Gradient']
    units = df['Unit']
    try:
        return sum(gradients) / sum(units)
    except ZeroDivisionError:
        return float(0)