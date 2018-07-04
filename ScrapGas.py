
# coding: utf-8

# In[1]:


import requests,MySQLdb
from bs4 import BeautifulSoup

# con = MySQLdb.connect("localhost","root","","GasDB", use_unicode=True, charset="utf8" )
# cur=con.cursor()

p_response=requests.get('http://then.gasbuddy.com/GB_Price_List.aspx?cntry=USA#us_cities')
p_t=p_response.text
# print(p_response.text)


# In[3]:


p_s=BeautifulSoup(p_t, "lxml")
p_tbody=p_s.findChildren('tbody')
# print(len(tbody))
# print(tbody[1])
# print(len(tbody[1].findChildren('tr')))
# print(tbody[1].findChildren('tr'))
# print(tbody[1])
#this is for states
# print(tbody[0].findChildren('tr')[0].findChildren('td')[0].findChildren('a')[0]['href'])
#this is for cities
# print(tbody[1].findChildren('tr')[0].findChildren('td')[0].findChildren('a')[0]['href'])
p_rows=p_tbody[1].findChildren('tr')
p_links=[i.findChildren('td')[0].findChildren('a')[0]['href'] for i in p_rows]
# f=open("links",'w')
# f.write(p_links)
# f.close()
# print(p_links)


# In[1]:


count=0
for i in p_links:
    temp=i
#     print(i)
    count+=1
    i+="/index.aspx?fuel=D"
    res=requests.get(i,verify=False)
    text=res.text
#     print(text)
    s=BeautifulSoup(text,"lxml")
    bodies=s.findChildren('tbody')
#     print(bodies)
    
#     recCount=1
    
    for j in bodies:
        for k in j.findChildren("tr"):
            price=''
            brand=''
            amenities=''
            address=''
            try:
                price+=str(k.findChildren("th")[0].findChildren("a")[0].findChildren("div")[0].string)
                brand+=str(k.findChildren("td")[0].findChildren("dl")[0].findChildren("a")[0].string)
                link=temp+'/'+k.findChildren("td")[0].findChildren("dl")[0].findChildren("a")[0]['href']
                resDetail=requests.get(link,verify=False)
                textDetail=resDetail.text
                sDetail=BeautifulSoup(textDetail,"lxml")
                #amenities work start
                features=sDetail.find_all('div', class_ = 'sp_features')
    #             print(features)
    #                 pdb.set_trace()
                features=features[0]

    #             print(features)

    #             features=features.findChildren('div')

    #             print(len(features),features,features[2])

    #             print(features[2])

                features=features.findChildren('div')[2].findChildren('ul')[0].findChildren('li')

    #             print(features)
                for l in features:
                    amenities+=','+l.string
                
                #amenities work end
                

#                 print(amenities)

                address+=str(k.findChildren("td")[0].findChildren("dl")[0].findChildren("dd")[0].string)
                address += str(k.findChildren("td")[2].findChildren("a")[0].string)
            except:
                
#                 print("hello")
                
                continue
            
            cur=con.cursor()
#             cur.execute("""INSERT INTO tbl VALUES (%s,%s,%s)""",(price,brand,address))
#             cur.execute("""INSERT INTO diesel VALUES (%s,%s,%s)""",(price,brand,address))
#             cur.execute("""update gas set amenities = %s where id = %s """,(amenities,recCount))
            #slicing because of remove starting comma
            cur.execute("""INSERT INTO diesel VALUES (%s,%s,%s,%s)""",(price,brand,address,amenities[1:]))
            con.commit()
#             recCount+=1
            
            
#     if count>2:
#         break


    


# In[12]:



con.close()

