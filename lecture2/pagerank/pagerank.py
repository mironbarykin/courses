import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Initialising response's distribution dictionary
    response = dict()
    for element in corpus:
        response[element] = 0

    # If there are no links on the page return equal probability
    if len(corpus[page]) == 0:
        for element in response:
            response[element] = 1 / len(corpus)
        return response

    links = corpus[page]

    for element in response:
        # Assigning random probability to the page
        response[element] += (1 - damping_factor) / len(corpus)

        if element in links:
            # Adding click probability to the page
                response[element] += damping_factor / len(links)
    return response



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    entries = dict()
    for element in corpus:
        entries[element] = 0

    current_page = random.choice(list(corpus.keys()))
    entries[current_page] += 1

    for i in range(0, n-1):
        model = transition_model(corpus, current_page, damping_factor)

        value = random.random()
        total = 0

        for element, probability in model.items():
            total += probability
            if value <= total:
                current_page = element
                break

        entries[current_page] += 1

    response = dict()
    for element, amount_of_entries in entries.items():
        response[element] = amount_of_entries / n

    return response

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Defining variables and constants
    amount_of_elements = len(corpus)
    default_probability = 1 / amount_of_elements
    random_probability = (1 - damping_factor) / amount_of_elements

    count = 0


    pages = dict()
    response = dict()
    for element in corpus:
        pages[element] = default_probability
        response[element] = None

    change = default_probability

    while change > 0.001:

        count += 1
        change = 0

        for element in corpus:
            probability = 0
            for other_element in corpus:
                if len(corpus[other_element]) == 0:
                    probability += pages[other_element] * default_probability
                elif element in corpus[other_element]:
                    probability += pages[other_element] / len(corpus[other_element])

            response[element] = random_probability + damping_factor * probability

        final = sum(response.values())
        for element, result in response.items():
            response[element] = result / final

        for element in corpus:
            new_change = abs(pages[element] - response[element])
            if new_change > change:
                change = new_change

        pages = response.copy()

    return pages

if __name__ == "__main__":
    main()
