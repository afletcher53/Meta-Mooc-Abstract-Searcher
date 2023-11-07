# Download the dataset if it doesnt exist
import os
from collections import Counter
import csv
import wget
from nltk.stem.snowball import SnowballStemmer

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
    hits = []
    bibs = []
    urls = []
    for l in newlines:
        if STEM:
            newl = stemmer.stem(l)
        else:
            newl = l.lower()
        for j in search_term1:
            if j.lower() in newl:
                for k in search_term2:
                    if k.lower() in newl:
                        for o in search_term4:
                            if o.lower() in newl:
                                record = extract_record(l)
                                if "title" not in record:
                                    title = ""
                                else:
                                    title = record["title"]
                                if "abstract" not in record:
                                    abstract = ""
                                else:
                                    abstract = record["abstract"]
                                hits.append([title, abstract, l, j, k, o])
                                bibs.append(l)
                                urls.append(record["url"])
                                break
                        break
                break

    print(f"Found {len(hits)} Records from Full Bib Search")
    return hits, bibs, urls


def search_over_title(newlines):
    hits = []
    bibs = []
    urls = []
    for l in newlines:
        if len(l) == 0:
            continue
        record = extract_record(l)
        if "title" not in record:
            continue
        title = record["title"]
        if STEM:
            title = stemmer.stem(title)
        for j in search_term1:
            if j.lower() in title:
                for k in search_term2:
                    if k.lower() in title:
                        for o in search_term4:
                            if o.lower() in title:
                                hits.append([title, j, k, o])
                                bibs.append(l)
                                urls.append(record["url"])
                                break
                        break
                break

    print(f"Found {len(hits)} Records from Title Search")
    return hits, bibs, urls


def search_over_abstract(newlines):
    hits = []
    bibs = []
    urls = []
    for l in newlines:
        if len(l) == 0:
            continue
        record = extract_record(l)
        if "abstract" not in record:
            continue
        abstract = record["abstract"]
        if STEM:
            abstract = stemmer.stem(abstract)
        for j in search_term1:
            if j.lower() in abstract:
                for k in search_term2:
                    if k.lower() in abstract:
                        for o in search_term4:
                            if o.lower() in abstract:
                                if "title" in record:
                                    title = record["title"]
                                    hits.append([title, abstract, j, k, o])
                                else:
                                    hits.append(["", abstract, j, k, o])
                                bibs.append(l)
                                urls.append(record["url"])
                                break
                        break
                break

    print(f"Found {len(hits)} Records from Abstract Search")
    return hits, bibs, urls


fulltext_search, fulltext_bibs, fulltext_urls = search_over_full_bib(newlines)
title_search, title_bibs, title_urls = search_over_title(newlines)
abstract_search, abstract_bibs, abstract_urls = search_over_abstract(newlines)

full_terms1 = []
full_terms2 = []
full_terms4 = []

"""
Write searching results to csv file, make files based on fullbib/title/abstract searching 
"""


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
                "Tintle",
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
