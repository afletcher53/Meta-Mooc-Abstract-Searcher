# Download the dataset if it doesnt exist
import os
from collections import Counter
import csv
import wget
from nltk.stem.snowball import SnowballStemmer
from tqdm import tqdm

STEM = True
WRITE_RESULTS_TO_CSV = True
PATH_TO_ACL_BIB_FILE = "./data/acl_bib_file.txt"

if not os.path.exists(PATH_TO_ACL_BIB_FILE):
    PATH_TO_ACL_BIB_FILE_ZIP = "./data/anthology+abstracts.bib.gz"
    print("Downloading the ACL bib file...")
    URL = "https://aclanthology.org/anthology+abstracts.bib.gz"
    wget.download(URL, PATH_TO_ACL_BIB_FILE_ZIP)
    import gzip

    with gzip.open(PATH_TO_ACL_BIB_FILE_ZIP, "rb") as f_in:
        with open(PATH_TO_ACL_BIB_FILE, "wb") as f_out:
            f_out.write(f_in.read())
    os.remove(PATH_TO_ACL_BIB_FILE_ZIP)


newlines = (
    open(PATH_TO_ACL_BIB_FILE, encoding="utf-8").read().split("inproceedings")
)

if STEM:
    stemmer = SnowballStemmer("english")

if STEM:
    stemmer = SnowballStemmer("english")


ORIGINAL_SEARCH_TERM_1 = [
    "Electronic Health Records",
    "Patient Discharge",
    "Patient Discharge Summaries",
    "health record",
    "medical record",
    "patient discharge",
    "discharge record",
    "discharge summar",
    "clinical narrative",
    "clinical domain",
    "medical domain",
    "clinical note",
    "clinical record",
    "clinical text",
    "medical text",
]

ORIGINAL_SEARCH_TERM_2 = [
    "Natural Language Processing",
    "natural language",
    "language processing",
    "translation",
    "NLP",
    "inference",
    "generation",
    "relation extraction",
    "relation-extraction",
    "entity recognition",
    "entity-recognition",
    "concept normalization",
    "concept-normalisation",
    "relation classification",
    "sequence label",
    "summarization",
    "summarisation",
    "parts-of-speech",
    "information-retrieval",
    "information retrieval",
    "informationgrouping",
    "sentiment",
    "semantic",
    "temporal-expression",
    "co-reference",
    "word-sense-disambiguation",
]

ORIGINAL_SEARCH_TERM_3 = ["similarity", "coherence", "feature"]

ORIGINAL_SEARCH_TERM_4 = [
    "Datasets as Topic",
    "shared task",
    "shared-task",
    "annotat",
    "question-entailment",
    "question-answering",
    "challenge",
    "community",
    "bakeoff",
    "bake-off",
    "benchmark",
    "evaluation",
    "assessment",
    "track",
    "public data",
    "public dataset",
    "public datasets",
    "publicly available dataset",
    "publicly available datasets",
    "public corpus",
]

if STEM:
    search_term1 = [stemmer.stem(i) for i in ORIGINAL_SEARCH_TERM_1]
    search_term2 = [stemmer.stem(i) for i in ORIGINAL_SEARCH_TERM_2]
    search_term4 = [stemmer.stem(i) for i in ORIGINAL_SEARCH_TERM_4]
else:
    search_term1 = ORIGINAL_SEARCH_TERM_1
    search_term2 = ORIGINAL_SEARCH_TERM_2
    search_term4 = ORIGINAL_SEARCH_TERM_4


def extract_record(bibterm):
    """
    Extracts structured items from a BibTeX term.

    Args:
    - bibterm (str): A BibTeX term as a string.

    Returns:
    - structured_items (dict): A dictionary of structured items extracted from the BibTeX term.
    """
    biblines = bibterm.split("\n")
    structured_items = {}
    for l in biblines[1:]:
        if "=" in l:
            item = l.split("=")
            structured_items[item[0].strip()] = item[1]
    return structured_items


def search_over_full_bib(newlines):
    """
    Searches for records in a list of strings `newlines` that contain specific search terms.
    Returns a list of hits, where each hit is a list containing the title, abstract, full record,
    and the search terms that matched.
    Also returns a list of the full records that matched and a list of the URLs
    associated with the records.

    Args:
        newlines (list): A list of strings representing the records to search over.
        flag (bool, optional): A flag indicating whether to use stemming when searching.
        Defaults to True.

    Returns:
        tuple: A tuple containing three lists: the hits, the full records that matched,
        and the URLs associated with the records.
    """
    hits, bibs, urls = [], [], []

    for line in tqdm(newlines, desc="Processing Full BIBs"):
        newl = stemmer.stem(line) if STEM else line.lower()
        if any(j in newl for j in terms1) and \
           any(k in newl for k in terms2) and \
           any(o in newl for o in terms4):
            record = extract_record(line)
            title = record.get("title", "")
            abstract = record.get("abstract", "")
            url = record.get("url", "")
            matching_terms = [term for term in terms1+terms2+terms4 if term in newl]
            hits.append([title, abstract, line] + matching_terms)
            bibs.append(line)
            urls.append(url)

    print(f"Found {len(hits)} Records from Full Bib Search")

    return hits, bibs, urls


def search_over_title(newlines):
    hits, bibs, urls = [], [], []


    for line in tqdm(newlines, desc="Processing titles"):
        if not line:
            continue
        
        record = extract_record(line)
        title = record.get("title", "").lower()

        if STEM:
            title = stemmer.stem(title)

        # Check if any search term from each category is found in the title
        if any(j in title for j in terms1) and \
           any(k in title for k in terms2) and \
           any(o in title for o in terms4):

            # Extract URL or set to empty string if not present
            url = record.get("url", "")

            # Create a list of matching terms for the current title
            matching_terms = [term for term in terms1+terms2+terms4 if term in title]

            hits.append([record["title"]] + matching_terms)  # original title for display
            bibs.append(line)
            urls.append(url)

    print(f"Found {len(hits)} Records from Title Search")

    return hits, bibs, urls


def search_over_abstract(newlines):
    """
    Searches over abstracts in a list of newline-separated bibliographic records.
    
    Args:
        newlines (list): A list of newline-separated strings representing bibliographic records.
        STEM (bool, optional): A flag indicating whether to use stemming on abstracts. 
        Defaults to True.

    Returns:
        tuple: A tuple of three lists: hits, full records, and URLs of matched abstracts.
    """
    hits, bibs, urls = [], [], []


    for line in tqdm(newlines, desc="Processing abstracts"):
        if not line:
            continue
        record = extract_record(line)
        abstract = record.get("abstract", "").lower()

        if STEM:
            abstract = stemmer.stem(abstract)

        # Check if any search term from each category is found in the abstract
        if any(j in abstract for j in terms1) and \
           any(k in abstract for k in terms2) and \
           any(o in abstract for o in terms4):

            title = record.get("title", "")
            url = record.get("url", "")
            matching_terms = [term for term in terms1+terms2+terms4 if term in abstract]
            hits.append([title, record["abstract"]] + matching_terms)
            bibs.append(line)
            urls.append(url)

    print(f"Found {len(hits)} Records from Abstract Search")
    return hits, bibs, urls


terms1 = [term.lower() for term in search_term1]
terms2 = [term.lower() for term in search_term2]
terms4 = [term.lower() for term in search_term4]

fulltext_search, fulltext_bibs, fulltext_urls = search_over_full_bib(newlines)
title_search, title_bibs, title_urls = search_over_title(newlines)
abstract_search, abstract_bibs, abstract_urls = search_over_abstract(newlines)

full_terms1 = []
full_terms2 = []
full_terms4 = []

OUTPUT_TO_CSV_FULLBIB_SEARCH = (
    "./data/acl_bib_search_fullbib_stem" + str(STEM) + ".csv"
)
OUTPUT_TO_CSV_TITLE_SEARCH = (
    "./data/acl_bib_search_title_stem" + str(STEM) + ".csv"
)
OUTPUT_TO_CSV_ABSTRACT_SEARCH = (
    "./data/acl_bib_search_abstract_stem" + str(STEM) + ".csv"
)

with open(OUTPUT_TO_CSV_FULLBIB_SEARCH, "w", encoding="utf-8") as cout:
    wr = csv.writer(cout)
    wr.writerow(
        [
            "Title",
            "Abstract",
            "Bib Item",
            "Matched Search Term 1",
            "Matched Search Term 2",
            "Matched Search Term 4",
        ]
    )
    for l in fulltext_search:
        wr.writerow(l)
        full_terms1.append(l[3])
        full_terms2.append(l[4])
        full_terms4.append(l[5])


if WRITE_RESULTS_TO_CSV:
    with open(OUTPUT_TO_CSV_TITLE_SEARCH, "w", encoding="utf-8") as cout:
        wr = csv.writer(cout)
        wr.writerow(
            [
                "Title",
                "Matched Search Term 1",
                "Matched Search Term 2",
                "Matched Search Term 4",
            ]
        )
        for l in title_search:
            wr.writerow(l)

    with open(OUTPUT_TO_CSV_ABSTRACT_SEARCH, "w", encoding="utf-8") as cout:
        wr = csv.writer(cout)
        wr.writerow(
            [
                "Title",
                "Abstract",
                "Matched Search Term 1",
                "Matched Search Term 2",
                "Matched Search Term 4",
            ]
        )
        for l in abstract_search:
            wr.writerow(l)


term1_cnt = Counter(full_terms1)
term2_cnt = Counter(full_terms2)
term4_cnt = Counter(full_terms4)

if WRITE_RESULTS_TO_CSV:
    import io

    with io.open(
        "./data/acl_bib_search_term1_cnt_stem" + str(STEM) + ".csv",
        "w",
        encoding="utf-8",
    ) as cout:
        wr = csv.writer(cout)
        wr.writerow(["Term", "Cnt"])
        for k, v in term1_cnt.items():
            wr.writerow([k, v])

        with open(
            "./data/acl_bib_search_term2_cnt_stem" + str(STEM) + ".csv",
            "w",
            encoding="utf-8",
        ) as cout:
            wr = csv.writer(cout)
            wr.writerow(["Term", "Cnt"])
            for k, v in term2_cnt.items():
                wr.writerow([k, v])

        with open(
            "./data/acl_bib_search_term4_cnt_stem" + str(STEM) + ".csv",
            "w",
            encoding="utf-8",
        ) as cout:
            wr = csv.writer(cout)
            wr.writerow(["Term", "Cnt"])
            for k, v in term4_cnt.items():
                wr.writerow([k, v])
