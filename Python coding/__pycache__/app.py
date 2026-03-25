import time
import json
import csv
from scholarly import scholarly
import pandas
import requests
from bs4 import BeautifulSoup

def getScholarData():
    try:
        url = "https://scholar.google.com.au/scholar?hl=en&as_sdt=0%2C5&q=accessibility+in+digital+design&btnG=&oq=access"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.361681261652"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        scholar_results = []
 
        for el in soup.select(".gs_r"):
            scholar_results.append({
                "title": el.select(".gs_rt")[0].text,
                "title_link": el.select(".gs_rt a")[0]["href"],
                "id": el.select(".gs_rt a")[0]["id"],
                "displayed_link": el.select(".gs_a")[0].text,
                "snippet": el.select(".gs_rs")[0].text.replace("\n", ""),
                "cited_by_count": el.select(".gs_nph+ a")[0].text,
                "cited_link": "https://scholar.google.com" + el.select(".gs_nph+ a")[0]["href"],
                "versions_count": el.select("a~ a+ .gs_nph")[0].text,
                "versions_link": "https://scholar.google.com" + el.select("a~ a+ .gs_nph")[0]["href"] if el.select("a~ a+ .gs_nph")[0].text else "",
            })
 
        for i in range(len(scholar_results)):
            scholar_results[i] = {key: value for key, value in scholar_results[i].items() if value != "" and value is not None}
 
        print(scholar_results)
 
    except Exception as e:
        print(e)
 
def save_csv(data: list[dict], filepath: str) -> None:
    if not data:
        print("No data to save to CSV.")
        return

    fieldnames = ["query", "title", "authors", "year", "journal",
                  "abstract", "citations", "url"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"CSV save in {filepath}")

getScholarData()



from scholarly import ProxyGenerator
pg = ProxyGenerator()
pg.ScraperAPI("YOUR_FREE_KEY")
scholarly.use_proxy(pg)


if __name__ == "__main__":
    main()