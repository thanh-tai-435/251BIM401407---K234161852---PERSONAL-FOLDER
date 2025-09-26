#XML
#Thư viện 1
from bs4 import BeautifulSoup
with open('../DATA_PROCESSING/Dataset/SalesTransactions/SalesTransactions.xml','r') as f :
    data = f.read()
    bs_data = BeautifulSoup(data,'xml')

    UelSample = bs_data.find_all('UelSample')
    print(UelSample)

# Thư viện 2
import pandas as pd
df = pd.read_xml(".././Dataset/SalesTransactions/SalesTransactions.xml")
print(df)
print(df.iloc[0])
data = df.iloc[0]
print(data[0])
print(data[1])
print(data[1]["OrderID"])

#----------------------------------------------------------------------------------------#
#Excel
import pandas as pd 
df = pd.read_excel("../DATA_PROCESSING/Dataset/SalesTransactions/SalesTransactions.xlsx")
print(df)

#------------------------------------------#
#JSON
df = pd.read_json("../DATA_PROCESSING/Dataset/SalesTransactions/SalesTransactions.json",encoding = 'utf-8',dtype = 'unicode')
print(df)
#-----------#
#CSV
df2 = pd.read_csv("../DATA_PROCESSING/Dataset/SalesTransactions/SalesTransactions.csv",encoding = 'utf-8',dtype='unicode',low_memory = False)
print(df2)
#-------------#
#txt
import pandas
df3 = pd.read_csv("../DATA_PROCESSING/Dataset/SalesTransactions/SalesTransactions.txt",encoding = 'utf-8',dtype='unicode',sep = "\t",low_memory = False)
print(df3)