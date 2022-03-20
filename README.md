# Student-Data
**A mini school management system**
This project is built using the University of Ilorin, Nigeria as a case study.

All that is needed is the HTML file of the result, thereafter reffered to as 'result files' (i.e downloaded from the result page).

The user needs to move these result files to the `results` folder in the root directory of the project file so the program could see it.


This project has a 'school.py' module which contains a `Semester` class, a `Session` class and a `Student` class.


**Class Semester:**
The `Semester` class can be initiated with a Pandas DataFrame of the table containing the results for that semester. It has a `show` method that 
displays the results table (best view in Jupyter lab or notebook environment).

>>> first_semester = Semester(df: pandas.DataFrame)

>>> first_semester.show() # this will display the result in well formatted table

>>> first_semester.gpa  # this will return the gpa of the `Semester` object in floating point number rounded to 2 decimal places

>>> first_semester.get_gpa() # just like the `gpa` attribute, it return the gpa in floating point number but not rounded at all


**Class Session:**
There is also a `Session` class which can be initiated with a  `level` and a list of `Semester` objects. This class inherit the `Semester` class.
It can only accept 2 Semesters or 3 Semesters (for Faculties like Engineering and Technology that
sometimes has a third semester).

>>> sess = Session('200', semesters: List[Semesters])

>>> sess.show() # behaves like the Semester class show method

>>> sess.gpa # this returns the gpa of the student for that session


**Class Student:**
This class can be initiated with the 'matriculation number' of the student (e.g 17/30GC***) and inherits from the `Semester` class. It has an `update` method which updates the `Student` object by
pulling the student's data from the database and populating the object. The `Student` class also has different methods for performing the desired functions.

>>> student = Student('17/30GC000') # creating the Student object automatically updates the student's data from the database

>>> student.cgpa  # this property returns the current cgpa of the student as calculated from the results uploaded

>>> student.get_cgpa_after('300')`# this returns the cgpa of the student after 300 level.

>>> student.get_cgpa_after_level()`# this return a dictionary that contains the student's cgpa after each level in a key-value pair

>>> student.low() # this returns the `Session` object where the student had the lowest gpa

>>> student.high()  # this returns the `Session` object where the student had the highest gpa


**NOTE:** This program also handles the complications that comes with the Faculty of Engineering and Technology students' 100 level results where only GNS matters.

This app also has a **Console User Interface**. You can run it just by running the `app.py` module and there you can do all sort of things like creating an
account (i.e signing up), login, reset password (for lost password). By signing up using your matriculation number and password, the user can upload their results
which already would have been placed in the `results` folder in the root directory. Thereafter, the user can then perform operations like checking their
cgpa and a summary of their results by entering the right options from the menu.

There is also **admin** priviledge for the **super user** (for example, the Level Adviser) which can only be accessed using an `admin key`.This allows the **super user** to perform operations like batch uploading of all the students results at the same time instead of uploading individually.


**NOTE:** The user **password** are hashed before being stored which makes it more secure against threat so you don't have to worry about your details.
