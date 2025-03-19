import requests
import xml.etree.ElementTree as ET
from typing import List, Dict

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_papers(query: str, max_results: int = 10) -> List[Dict]:
    """Fetches papers from PubMed using the provided query."""
    search_url = f"{BASE_URL}esearch.fcgi?db=pubmed&term={query}&retmax={max_results}&retmode=json"
    search_response = requests.get(search_url)
    search_response.raise_for_status()

    paper_ids = search_response.json().get("esearchresult", {}).get("idlist", [])
    if not paper_ids:
        return []

    fetch_url = f"{BASE_URL}efetch.fcgi?db=pubmed&id={','.join(paper_ids)}&retmode=xml"
    fetch_response = requests.get(fetch_url)
    fetch_response.raise_for_status()

    return parse_pubmed_xml(fetch_response.text)

def parse_pubmed_xml(xml_data: str) -> List[Dict]:
    """Parses PubMed XML and extracts relevant paper details."""
    root = ET.fromstring(xml_data)
    papers = []
    
    for article in root.findall(".//PubmedArticle"):
        paper_id = article.find(".//PMID").text
        title = article.find(".//ArticleTitle").text
        pub_date = article.find(".//PubDate/Year")
        pub_date = pub_date.text if pub_date is not None else "Unknown"
        
        authors = []
        companies = []
        corresponding_email = None

        for author in article.findall(".//Author"):
            last_name = author.find("LastName")
            fore_name = author.find("ForeName")
            affiliation = author.find(".//AffiliationInfo/Affiliation")
            
            if last_name is not None and fore_name is not None and affiliation is not None:
                full_name = f"{fore_name.text} {last_name.text}"
                authors.append((full_name, affiliation.text))
        
        papers.append({
            "PubmedID": paper_id,
            "Title": title,
            "Publication Date": pub_date,
            "Authors": authors
        })

    return papers