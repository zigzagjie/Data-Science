##https://stackoverflow.com/questions/6531482/how-to-check-if-a-string-contains-an-element-from-a-list-in-python

"""
In pandas dataframe, you usually need to apply function on string column. Typically they are just the same as the string function. 
However, you need to transform series to str function ready to apply string function
"""
# Task 1: Remove extra blanks
s='hello the world        yes!'
snew=" ".join(s.split())

# Task 2: Find the index of nth occurence in a string
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start
