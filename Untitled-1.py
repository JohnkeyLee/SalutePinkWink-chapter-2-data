# %%
import pandas as pd
import numpy as np

df = pd.read_csv('G:\\My Drive\\Jongki-study\\05_Manual\\17_Python\\DataScience\\data\\salesfunnel.csv')
print(df.head())

# %%
# This is to creat a pivot table based on the designated index (here, 'Name')
# All the character based data is gone and the numbered data leaves
# The numbers are averaged which is the default set up
print(pd.pivot_table(df, index=['Name']))
print(pd.pivot_table(df, index=['Name', 'Rep', 'Manager']))

# %%

# This is to create the pivot table based on two index and show the price
print(pd.pivot_table(df, index=['Manager', 'Rep'], values=["Price"]))
# This is to create the same table above, but it will return summation
print(pd.pivot_table(df, index=['Manager', 'Rep'], values=['Price'], aggfunc=np.sum))
# This is to create a big pivot table based on the designated indexes ('Manager', 'Rep', 'Product') and it will return the data in 'Price' and 'Quantity'
# 'aggfunc' is to apply a designated calculation, and here there are two returns (sum and mean)
# 'fill_value=0' is to return 0 when a cell has NaN
# If 'margins=True', ALL columns and rows will be added with partial group aggregates across the categories on the rows and columns.
print(pd.pivot_table(df, index=['Manager', 'Rep', 'Product'], values=['Price', 'Quantity'], aggfunc=[np.sum,np.mean], fill_value=0,margins=True))


# %%



