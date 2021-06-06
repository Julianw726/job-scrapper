import requests
from bs4 import BeautifulSoup
import pandas as pd



max_results_per_city = 100
# Crawling more results, will also take much longer. First test your code on a small number of results and then expand.
i = 0
results = []
df_more = pd.DataFrame(columns=["Title","Location","Company","Salary", "Synopsis"])
for city in set(['Baltimore %2C+MD', 'remote']):
    for start in range(0, max_results_per_city, 10):
        # Grab the results from the request (as above) 
        #change the q= to job you're looking for
        url = 'https://www.indeed.com/jobs?q=dietitian&l='+str(city)+'&sort=date&start=' + str(start) 
        #Bottom url is for pulling last 24 hours. uncomment 
#       url = https://www.indeed.com/jobs?q=dietitian&l='+str(city)+'&sort=date&fromage=1&start='+ str(start)
        # Append to the full set of results
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
        for each in soup.find_all(class_= "result" ):
            try: 
                title = each.find(name="h2", attrs=("span",'title')).text.replace('\n', '')
            except:
                title = None
            try:
                location = each.find(name='span', attrs={'class':"location" }).text.replace('\n', '')
            except:
                location = None
            try: 
                company = each.find(name="span", attrs={"class":"company"}).text.replace('\n', '')
            except:
                company = None
            try:
                salary = each.find('span', {'class':'no-wrap'}).text
            except:
                salary = None
            try:
                synopsis = each.find(name="div", attrs={"class":"summary"}).text.replace('\n', '')
            except:
                synopsis = None
            print(title, location, company, salary, synopsis)
            df_more = df_more.append({'Title':title, 'Location':location, 'Company':company, 'Salary':salary, 'Synopsis':synopsis}, ignore_index=True)
            i += 1

df_more.to_csv("test.csv", encoding='utf-8')
