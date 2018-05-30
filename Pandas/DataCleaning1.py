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

##########
# advanced goal: to impute Nan with the most frequent name in the group 

"""
we have some missing data in df1
>>> df1
   Name Setting Setting2   Num
0     A     Sun      Sun   1.0
1     A     Sun      Sun   2.0
2     A    Moon     Moon   3.0
3     A    None      NaN   NaN
4     B      YY       YY   2.0
5     B      YY       YY   3.0
6     B      YY       YY   4.0
7     B      XX       XX   5.0
8     B    None      NaN   NaN
9     C    Tree     Tree   9.0
10    C    None      NaN   NaN
11    C    Tree     Tree  10.0
12    C    Tree     Tree  11.0
13    C    None      NaN   NaN
14    C    Tree     Tree  12.0
15    C    None      NaN   NaN
"""
df1.groupby('Name')['Setting2'].transform(lambda x: x.fillna(x.mode().ix[0]))

"""
>>> df1.groupby('Name')['Setting2'].transform(lambda x: x.fillna(x.mode().ix[0]))
0      Sun
1      Sun
2     Moon
3      Sun
4       YY
5       YY
6       YY
7       XX
8       YY
9     Tree
10    Tree
11    Tree
12    Tree
13    Tree
14    Tree
15    Tree
Name: Setting2, dtype: object

That's the only way to impute cell with mode 
actually impute with groupby mean is easier

>>> df1['Num']=df1.groupby('Name')['Num'].transform(lambda x: x.fillna(x.mean()))
>>> df1
   Name Setting Setting2   Num
0     A     Sun      Sun   1.0
1     A     Sun      Sun   2.0
2     A    Moon     Moon   3.0
3     A    None      NaN   2.0
4     B      YY       YY   2.0
5     B      YY       YY   3.0
6     B      YY       YY   4.0
7     B      XX       XX   5.0
8     B    None      NaN   3.5
9     C    Tree     Tree   9.0
10    C    None      NaN  10.5
11    C    Tree     Tree  10.0
12    C    Tree     Tree  11.0
13    C    None      NaN  10.5
14    C    Tree     Tree  12.0
15    C    None      NaN  10.5

"""
# Transform function is important aligned with groupby
# mode function should be scrutinized
# pandas is powerful but need to learned well. 

###### groupby function details

import pandas as pd
df1=pd.DataFrame()
df1['Name']=['A','A','A','A','B','B','B','C','C','C','C','C','C']
df1['Setting']=['Sun','Sun','Moon',None,'Tree','Tree','P','LL','LL','MM','MM','MM','MM']

"""
>>> df1
   Name Setting
0     A     Sun
1     A     Sun
2     A    Moon
3     A    None
4     B    Tree
5     B    Tree
6     B       P
7     C      LL
8     C      LL
9     C      MM
10    C      MM
11    C      MM
12    C      MM
"""

# group by two equivalent functions

df1.groupby('Name')['Setting'].value_counts()
"""
Name  Setting
A     Sun        2
      Moon       1
B     Tree       2
      P          1
C     MM         4
      LL         2
Name: Setting, dtype: int64
"""

df1['Setting'].groupby(df1['Name']).value_counts()
""""
Name  Setting
A     Sun        2
      Moon       1
B     Tree       2
      P          1
C     MM         4
      LL         2
Name: Setting, dtype: int64
>>>
"""

# https://towardsdatascience.com/pandas-tips-and-tricks-33bcc8a40bb9

# goal is still to get the max frequent item in each group
df1.groupby('Name').apply(lambda x:x['Setting'].value_counts()).reset_index().groupby('Name').first()

"""
>>> df1.groupby('Name').apply(lambda x:x['Setting'].value_counts()).reset_index().groupby('Name').first()
     level_1  Setting
Name
A        Sun        2
B       Tree        2
C         MM        4

"""









