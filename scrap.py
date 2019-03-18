import urllib.request
import bs4 as bs 
import pandas as pd 


source = urllib.request.urlopen('https://pythonprogramming.net/parsememcparseface/sitemap.xml').read()
soup = bs.BeautifulSoup(source,'xml')

js_test = soup.find('p',clss_ = 'jstest')


# nav = soup.body

# for p in nav.find_all('p'):
#     print(p.text)

# table = soup.table 
# table = soup.find ('table')
# table_rows = table.find_all('tr')

# for tr in table_rows :
#     td = tr.find_all('td')
#     row = [i.text for i in td ]

# dfs = pd.read_html('https://pythonprogramming.net/parsememcparseface/')
# for df in dfs :
#     print (df)