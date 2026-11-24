# PubMed search tool using NCBI E-utilities and Biopython

from Bio import Entrez
from langchain_core.tools import tool

from src.config import NCBI_EMAIL

# Identify the application to NCBI
Entrez.email = NCBI_EMAIL
Entrez.tool = "AgenticResearchAssistant"


@tool
def pubmed_search(query: str) -> str:
    """
    Search PubMed for biomedical research papers.

    Use this tool for scientific literature searches,
    medical research topics, and biomedical publications.
    """

    # Search PubMed and retrieve up to five paper IDs
    with Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=5,
        sort="relevance"
    ) as handle:
        search_results = Entrez.read(handle)

    paper_ids = search_results["IdList"]

    if not paper_ids:
        return "No PubMed articles found."

    # Retrieve article metadata
    with Entrez.efetch(
        db="pubmed",
        id=",".join(paper_ids),
        rettype="medline",
        retmode="text"
    ) as handle:
        from Bio import Medline
        papers = list(Medline.parse(handle))

    # Format the results
    results = []

    for paper in papers:
        pmid = paper.get("PMID", "")
        title = paper.get("TI", "Unknown title")
        authors = paper.get("AU", [])
        year = paper.get("DP", "Unknown date")
        abstract = paper.get("AB", "No abstract available")

        results.append(
            f"Title: {title}\n"
            f"Authors: {', '.join(authors[:3])}\n"
            f"Date: {year}\n"
            f"PMID: {pmid}\n"
            f"URL: https://pubmed.ncbi.nlm.nih.gov/{pmid}/\n"
            f"Abstract: {abstract}\n"
        )

    return "\n---\n".join(results)