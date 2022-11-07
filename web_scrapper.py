import requests
import re
import pandas as pd
import bs4


class Scrapper:
    response = requests.get("https://opentender.eu/")

   #try:
        #response.raise_for_status()
    #except Exception as exc:
        #print('There was a problem.')

    
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a',href = True) #link of countries

    references = []
    for reference in links[5:38]:
        final_link = 'https://opentender.eu' + reference.get('href')
        references.append(final_link)

    no_of_tenders = soup.find_all('div')[21:54] #tenders via each country
    tenders = []

    for n in no_of_tenders:
        tenders.append(n.text)

    u = re.compile(r'\d+.?\d+')       #To convert into float
    total_tenders = []

    for t in tenders:
        if 'Million' in t:
            mo = u.findall(t)
            corrected_num = float(mo[0]) * 1000000
            total_tenders.append(corrected_num)
        else:
            total_tenders.append(t)

   
    year = {}
    eu = {}    
    for i in range(len(references)):
        res = requests.get(references[i])
        page = res.text
        read = bs4.BeautifulSoup(page, 'html.parser')
        country = read.find_all('span')

        years = read.find(class_ = 'x axis')
        num = years.find_all('title') 

        for sp in num:
            year[sp.text] = 0


        eu[country[2].text] = year

    

    '''Extract by pandas library '''

    df = pd.DataFrame(eu)
    data = df.T
    data['Total Tenders'] = total_tenders


    '''CSV file conversion'''
    data.to_csv('scrapper_data.csv', encoding='utf-8', index= True)