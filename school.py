import pandas as pd
from typing import List, Dict, Tuple, Union
# custom imports
from database import engine, results
from errors.errors import MatchError


class Semester:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def __repr__(self) -> str:
        return f'<Semester - {self.gpa}>'
    
    @property
    def gpa(self) -> float:
        return round(self.get_gpa(), 2)

    def titles(self) -> pd.Series:
        return self.df['Title']

    def title(self, course: str) -> pd.Series:
        return self.df['Title'][course]

    def units(self) -> pd.Series:
        return self.df['Unit']

    def unit(self, course: str) -> pd.Series:
        return self.df['Unit'][course]

    def statuses(self) -> pd.Series:
        return self.df['Status']

    def status(self, course: str) -> pd.Series:
        return self.df['Status'][course]

    def cas(self) -> pd.Series:
        return self.df['CA']

    def ca(self, course: str) -> pd.Series:
        return self.df['CA'][course]
    
    def show(self) -> pd.DataFrame:
        return self.df
    
    def exams(self) -> pd.Series:
        return self.df['Exam']

    def exam(self, course: str) -> pd.Series:
        return self.df['Exam'][course]

    def totals(self) -> pd.Series:
        return self.df['Total']

    def total(self, course: str) -> pd.Series:
        return self.df['Total'][course]

    def grades(self) -> pd.Series:
        return self.df['Grade']

    def grade(self, course: str) -> pd.Series:
        return self.df['Grade'][course]

    def gradients(self) -> pd.Series:
        return self.df['Gradient']

    def gradient(self, course: str) -> pd.Series:
        return self.df['Gradient'][course]
    
    def get_gpa(self) -> float:
        try:
            return sum(self.gradients()) / sum(self.units())
        except ZeroDivisionError:
            return float(0)


class Session(Semester):
    def __init__(self, level: str, semesters: List[Semester]):
        self.level = level
        self.first_semester = semesters[0]
        try:
            self.second_semester = semesters[1]
        except IndexError:
            self.second_semester = None
        try:
            self.third_semester = semesters[2]
        except IndexError:  # in cases of sessions that only have 2 semesters
            self.third_semester = None
        
    def __repr__(self) -> str:
        return f'<{self.level}L Session[{len(self)} Semesters] - {self.get_gpa():.2f}>'
    
    def __len__(self) -> int:
        return 3 if self.third_semester else 2
    
    @property
    def harmattan(self) -> Semester:
        return self.first_semester
    
    @property
    def rain(self) -> Semester:
        return self.second_semester
    
    @property
    def df(self) -> pd.DataFrame:
        """
        This attribute is the concatenation of all the Student's Semesters'
        data into a single DataFrame and returns the DataFrame.
        :return: pandas.DataFrame
        """
        list_of_sems = [self.first_semester, self.second_semester, self.third_semester]
        list_of_sems = list(filter(lambda x: x is not None, list_of_sems))
        return pd.concat([sems.df for sems in list_of_sems])

    def show(self) -> pd.DataFrame:
        """
        This method is used to display the Students data in a table form.
        :return: pandas.DataFrame
        """
        return self.df


class Student(Semester):
    # noinspection PyMissingConstructor
    def __init__(self, matric_no: Union[str, int]):
        self.matric_no = matric_no.upper()
        self.__sessions = dict()
        self.__cgpa_after = dict()
        self.fullname = None
        self.faculty = None
        self.department = None
        self.current_level = None
        self.update()

    def __repr__(self) -> str:
        return f"<{self.fullname} - {self.matric_no}>\n\
            {self.current_level}L || {self.department} || {self.faculty}"
    
    @property
    def df(self) -> pd.DataFrame:
        """
        This attribute is the concatenation of all the Student's Sessions'
        data into a single DataFrame and returns the DataFrame.
        :return: pandas.DataFrame
        """
        return pd.concat([session.df for session in self.sessions])
    
    @property
    def sessions(self) -> List[Session]:
        """
        This attribute is the list of all the Session object the Student has.
        It return a list of all the sessions.
        :return: List[Session]
        """
        return list(self.__sessions.values())
    
    @property
    def cgpa(self) -> float:
        """
        This method returns the CGPA of the student in 2 decimal places.
        :return: float
        """
        return round(self.get_cgpa(), 2)
    
    def __parse_html(self, file, sessional=True) -> Tuple:
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
        matric, name, fac, dept, level = pd.read_html(file)[0][1]
        try:
            assert(self.matric_no == matric.upper())
        except AssertionError:
            raise MatchError("[MATRICULATION NUMBER]: The matriculation number does not match"
                             "with the one on the results.")
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
        if sessional:
            return dfs[1:], name, fac, dept, level
        return dfs[-1], name, fac, dept, level
    
    def show(self) -> pd.DataFrame:
        """
        This method is used to display the Students data in a table form.
        :return: pandas.DataFrame
        """
        return self.df

    def add_session(self, level: str, session: Session):
        """This method adds another Session object to a particular Student."""
        self.__sessions.update({level: session})
        self.__cgpa_after.update({level: self.cgpa})

    def _get_html_content(self) -> List:
        with engine.begin() as conn:
            s = results.select().where(self.matric_no == results.c.student_id)
            result = conn.execute(s)
            return [row.html for row in result]

    def update(self):
        """This method locates the HTML files containing the results and updates
        the student's data by adding the data for each sessions."""

        name = fac = dept = None
        current_level = '100'

        for f in self._get_html_content():
            dfs, name, fac, dept, level = self.__parse_html(f, sessional=True)
            semesters = [Semester(df) for df in dfs]
            session = Session(level, semesters)
            self.add_session(level, session)
            current_level = level if level >= current_level else current_level
        self.fullname = name
        self.faculty = fac
        self.department = dept
        self.current_level = current_level

    def get_session(self, level: str) -> Session:
        """
        This method gets and return specified Session by `level`.
        :return: Session
        """
        return self.__sessions.get(level)

    def get_cgpa(self) -> float:
        """
        This method gets returns the CGPA of the student.
        :return: float
        """
        return self.get_gpa()
    
    def high(self) -> Session:
        """This method returns the Session where the Student has the highest GPA.
        :return: Session"""
        h = self.sessions[0]
        for s in self.sessions[1:]:
            if s.gpa >= h.gpa:
                h = s
        return h
    
    def low(self) -> Session:
        """This method returns the Session where the Student has the lowest GPA.
        :return: Session"""
        low = self.sessions[0]
        for s in self.sessions[1:]:
            if s.gpa <= low.gpa:
                low = s
        return low
    
    def get_cgpa_after_level(self) -> Dict:
        """This method returns a dictionary of the Student's CGPA after every level.
        : return: Dict"""
        return self.__cgpa_after
    
    def get_cgpa_after(self, level: str) -> float:
        """This methods helps to get the CGPA of the student after the specified `level`."""
        return self.__cgpa_after[level]
