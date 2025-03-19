from typing import List, Dict, Tuple

NON_ACADEMIC_KEYWORDS = ["Pharma", "Biotech", "Inc.", "Ltd.", "Corporation", "GmbH"]

def filter_non_academic_authors(papers: List[Dict]) -> List[Dict]:
    """Filters out authors affiliated with non-academic institutions."""
    results = []
    
    for paper in papers:
        non_academic_authors = []
        company_affiliations = []
        
        for author, affiliation in paper["Authors"]:
            if any(keyword in affiliation for keyword in NON_ACADEMIC_KEYWORDS):
                non_academic_authors.append(author)
                company_affiliations.append(affiliation)

        if non_academic_authors:
            results.append({
                "PubmedID": paper["PubmedID"],
                "Title": paper["Title"],
                "Publication Date": paper["Publication Date"],
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(company_affiliations),
            })
    
    return results