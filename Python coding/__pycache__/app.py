# tut from: https://medium.com/@darshankhandelwal12/scrape-google-scholar-using-python-3f35a3a6597b
import requests
from bs4 import BeautifulSoup

def getScholarProfiles():
    try:
        url = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=Quantum+Physics"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        scholar_profiles = []
        for el in soup.select('.gsc_1usr'):
            profile = {
                'name': el.select_one('.gs_ai_name').get_text(),
                'name_link': 'https://scholar.google.com' + el.select_one('.gs_ai_name a')['href'],
                'position': el.select_one('.gs_ai_aff').get_text(),
                'email': el.select_one('.gs_ai_eml').get_text(),
                'departments': el.select_one('.gs_ai_int').get_text(),
                'cited_by_count': el.select_one('.gs_ai_cby').get_text().split(' ')[2]
            }
            scholar_profiles.append({k: v for k, v in profile.items() if v})
        
        print(scholar_profiles)
    except Exception as e:
        print(e)

getScholarProfiles()
    