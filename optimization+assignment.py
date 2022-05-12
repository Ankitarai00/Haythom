#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 12:24:41 2020

@author: haythamomar
"""
from pulp import *

model = LpProblem('PILLOWS',LpMaximize)

X1= LpVariable('X1',0,None,'Integer')
X2= LpVariable('X2',0,None,'Integer')
X3= LpVariable('X3',0,None,'Integer')
##define our objeective function

model += X1 *33 +X2 *40 + X3 *34

model += X1* 0.4 +X2 * 0.7 +X3*0.4 <= 40
model += X1* 0.2 +X2 * 0.5 +X3*0.6 <= 40
model += X1* 0.3 +X2 * 0.3 +X3*0.2 <= 40


model.solve()

X1.varValue
X2.varValue
X3.varValue


#### assignment problem no 2

from pulp import *

model= LpProblem('shipping',LpMinimize)

customers=['Australia','Sweeden','Brazil']
factory= ['Factory1','Factory2']
products= ['Chair','Table','Beds']

keys= [(f,p,c) for f in factory for p in products for c in customers]

var= LpVariable.dicts('shipment', keys,0,None,cat='Integer')



costs_value= [50,80,50,
        60,90,60,
        70,90,70,
        80,50,80,
        90,60,90,
        90,70,90]

costs= dict(zip(keys,costs_value))




demand_keys= [(p,c)for c in customers
              for p in products]
demand_values=[90,65,700,
               120,450,40,
               78,52,500]
demand= dict(zip(demand_keys,demand_values))


model+= lpSum(var[(f,p,c)]*costs[(f,p,c)]
   for f in factory for p in products for c in customers )

model += lpSum(var[('Factory1',p,c)]
               for p in products for c in customers)<= 1500
model += lpSum(var[('Factory2',p,c)]
               for p in products for c in customers)<= 2500

for c in customers:
    for p in products:
        model += var[('Factory1',p,c)]+var[('Factory2',p,c)]>= demand[(p,c)]

model.solve()

for i in var: 
    print('{} shipping {}'.format(i,var[i].varValue))





param=pd.read_excel('assignment_ps.xlsx')



param=param.rename(columns={'Unnamed: 0': 'period'} )
param['t']= range(1,13)

param= param.set_index('t')

inventory= LpVariable.dicts('inv',[0,1,2,3,4,5,6,7,8,9,10,11,12],0,None,'Integer')
inventory[0]= 0

production=LpVariable.dicts('Prod',[1,2,3,4,5,6,7,8,9,10,11,12],0,None,'Integer')
binary= LpVariable.dicts('binary',[1,2,3,4,5,6,7,8,9,10,11,12],0,None,'Binary')

time= [1,2,3,4,5,6,7,8,9,10,11,12]


model= LpProblem('Production',LpMinimize)

model += lpSum([ inventory[t]* param.loc[t,'storage cost']+ production[t]* param.loc[t,'var']+
                binary[t]* param.loc[t,'fixed cost'] for t in time])


for t in time:
    model+=  production[t]  -  inventory[t]+ inventory[t-1]>= param.loc[t,'demand']
    model +=   production[t]<=        binary[t]* param.loc[t,'Capacity']
    
model.solve()    
for v in model.variables():
    print(v,v.varValue)

optimization_data= pd.DataFrame({'demand': param['demand'],
    'production': [production[i].varValue for i in production],
    'inventory' : [inventory[i].varValue for i in range(1,13)],
    'opening':   [binary[i].varValue for i in binary]
})











