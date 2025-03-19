import argparse
from get_papers_list.fetch import fetch_papers
from get_papers_list.filter import filter_non_academic_authors
from get_papers_list.output import save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed research papers.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename.")

    args = parser.parse_args()

    papers = fetch_papers(args.query)
    filtered_papers = filter_non_academic_authors(papers)

    if args.file:
        save_to_csv(args.file, filtered_papers)
    else:
        print(filtered_papers)

if __name__ == "_main_":
    main()