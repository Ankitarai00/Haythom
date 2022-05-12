#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 19:44:50 2020

@author: haythamomar
"""
import pandas as pd
import numpy as np
import seaborn as sns
import inventorize3 as inv


retail= pd.read_csv('online_retail2.csv')

retail= retail.drop_duplicates()
retail= retail.dropna()
retail= retail[retail.Quantity > 0]
retail_clean= retail.copy()
retail_clean['Revenue']= retail['Price']* retail['Quantity']
retail_clean.to_csv('retail_clean.csv')
retail_clean.columns
grouped= retail_clean.groupby('Description'
            ).agg(total_sales= ('Quantity',np.sum),
                  total_revenue= ('Revenue',np.sum)).reset_index()

grouped.to_csv('for_abc.csv')


grouped

a=inv.ABC(grouped[['Description','total_sales']])

a.Category.value_counts()

sns.countplot(x='Category',data=a)
sns.barplot(x= 'Category',y= 'total_sales',data=a)


#### multi creteria abc analyisis 

b=inv.productmix(grouped['Description'],grouped['total_sales'],grouped['total_revenue'])
b.columns
b.product_mix.value_counts()

sns.countplot(x='product_mix',data= b)
sns.barplot(x='product_mix',y='sales',data= b)
sns.barplot(x='product_mix',y='revenue',data= b)



retail_clean.groupby(['Country','Description']).agg(total_sales=('Quantity',np.sum),
                                                    total_revenue= ('Revenue',np.sum)).reset_index()

## Manipulation of data to multi-creteria
by_store= retail_clean.groupby(['Country','Description']).agg(total_sales=('Quantity',np.sum),
                                                    total_revenue= ('Revenue',np.sum)).reset_index()

mix_country=inv.productmix_storelevel(by_store['Description'],
                          by_store['total_sales'], 
                          by_store['total_revenue'],
                          by_store['Country'])

mix_country.columns

product_mix=mix_country.groupby(['storeofsku','product_mix']).count().reset_index().iloc[:,0:3]


product_mix[product_mix.storeofsku=='Australia']


##### supplier segmentation

supplier= pd.read_csv('supplier_data.csv')
supplier.head()
supplier.columns

supplier['risk_index']= supplier['availability']+supplier['no_suppliers']+supplier['standard']+supplier['price_fluctuation']


supplier['value']= supplier['price']*supplier ['Quantity']
supplier.value.describe()

def category(x,y):
    if((x>= 3000000)& (y >= 1)):
        return 'strategic'
    if((x>= 3000000)& (y < 1)):
        return 'leverage'
    if((x < 3000000)& (y >= 1)):
        return 'Critical'
    if((x < 3000000)& (y < 1)):
        return 'Routine'

for i in range(supplier.shape[0]):
    supplier.loc[i,'category']=category(supplier.loc[i,'value'],
                                        supplier.loc[i,'risk_index'])


supplier.category.value_counts()

sns.scatterplot(x='value',y='risk_index',data=supplier, hue='category')
































