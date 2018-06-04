##https://stackoverflow.com/questions/6531482/how-to-check-if-a-string-contains-an-element-from-a-list-in-python

"""
In pandas dataframe, you usually need to apply function on string column. Typically they are just the same as the string function. 
However, you need to transform series to str function ready to apply string function
"""
# Task 1: Remove extra blanks
s='hello the world        yes!'
snew=" ".join(s.split())
