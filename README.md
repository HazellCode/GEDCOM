This is a simple webapp that reads a "UTF-8" formatted GEDCOM file and formats the information for the user.

In the form of:
- A Family Tree
- More Detailed Per Individual Profile Page


This projects uses a Python Backend running Flask to handle parsing and API calls and Client Side JavaScript to render the information to the user.

Lots of the files in /Tools are from a previous build of the application where the parser first formatted the data into python objects then converted those into JSON.
This is very inefficient and it took ages to convert the tree into JSON.

In the 2nd version of the parser the file is converted into JSON at runtime rather than after the fact. By doing this upgrade it has resulted in greately improved parse times, improving the user expeince greatly.

