import csv
from typing import List, Dict

def save_to_csv(filename: str, papers: List[Dict]):
    """Saves the filtered papers to a CSV file."""
    headers = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(papers)

    print(f"Results saved to {filename}")