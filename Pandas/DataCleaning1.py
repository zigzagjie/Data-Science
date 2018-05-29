"""
Case: suppose the dataframe has two columns with categorical data

goal: get relative frequency for each type combination
"""
#Case
#create such a dataframe
import pandas as pd
df1=pd.DataFrame()
df1['Name']=['A','A','A','B','B','B','C','C','C','C','C']
df1['Setting']=['Flower','Sun','Flower','Way','Way','Way','pp','pp','ll','ll','pp']

"""
The example dataframe looks like:
>>> df1
   Name Setting
0     A  Flower
1     A     Sun
2     A  Flower
3     B     Way
4     B     Way
5     B     Way
6     C      pp
7     C      pp
8     C      ll
9     C      ll
10    C      pp

"""

# we would like to count the frequency of combination of Name and Setting
df1.groupby('Name')['Setting'].value_counts()

"""
results:

Name  Setting
A     Flower     2
      Sun        1
B     Way        3
C     pp         3
      ll         2
"""

# we would like to get the frequency of Name
df1.groupby('Name')['Setting'].count()


"""
Name
A    3
B    3
C    5
"""

# Then we can get relative frequency of (Name,Setting) combination in each Name group
 df1.groupby(['Name'])['Setting'].value_counts()/df1.groupby('Name')['Setting'].count()
Name  Setting
A     Flower     0.666667
      Sun        0.333333
B     Way        1.000000
C     pp         0.600000
      ll         0.400000
Name: Setting, dtype: float64

####
"""
Ultimate goal: we just want to get the most frequent combination in each name
like 

A     Flower     0.666667
B     Way        1.000000
C     pp         0.600000

Actually, notice that the df we get before is multi-level indexed. 
"""

#Method 1 using multi-level indexed
df2=df1.groupby(['Name'])['Setting'].value_counts()/df1.groupby('Name')['Setting'].count()
df2.max(level='Name')

"""
Result:
Name
A    0.666667
B    1.000000
C    0.600000
Name: Setting, dtype: float64

It is close but we also need the setting column information.

"""
df3=df2.max(level='Name')

"""
>>> df3
Name
A    0.666667
B    1.000000
C    0.600000
Name: Setting, dtype: float64
>>> df2
Name  Setting
A     Flower     0.666667
      Sun        0.333333
B     Way        1.000000
C     pp         0.600000
      ll         0.400000
Name: Setting, dtype: float64
>>> df2-df3
Name  Setting
A     Flower     0.000000
      Sun       -0.333333
B     Way        0.000000
C     pp         0.000000
      ll        -0.200000
Name: Setting, dtype: float64
>>> df2-df3==0
Name  Setting
A     Flower      True
      Sun        False
B     Way         True
C     pp          True
      ll         False
Name: Setting, dtype: bool
>>> df2[df2-df3==0]
Name  Setting
A     Flower     0.666667
B     Way        1.000000
C     pp         0.600000
Name: Setting, dtype: float64
"""

#In conclusion
df2=df1.groupby(['Name'])['Setting'].value_counts()/df1.groupby('Name')['Setting'].count()
df3=df2.max(level='Name')
df2[df2-df3==0]



