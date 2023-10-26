import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    corpus = dict()
    
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as file:
            corpus[filename] = file.read()

    return corpus

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    punctuation = string.punctuation
    stopwords = nltk.corpus.stopwords.words("english")
    return [i.lower() for i in nltk.word_tokenize(document) if i not in punctuation + '’' and i not in stopwords]

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = dict()
    for document in documents:
        unique_words = set(documents[document])
        for word in unique_words:
            if word not in words:
                words[word] = 1
            else:
                words[word] += 1
            
    return {word: math.log((len(documents) / words[word])) for word in words}

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    score = {file: 0 for file in files}
    for word in query:
        if word in idfs:
            for file in files:
                score[file] += files[file].count(word) * idfs[word]
    return sorted([file for file in files], key = lambda x: score[x], reverse=True)[:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    score = {sentence: {'idf': 0, 'len': len(nltk.word_tokenize(sentence)), 'query': 0, 'qtd': 0} for sentence in sentences}

    for sentence in sentences:
        current = score[sentence]
        for word in query:
            if word in sentences[sentence]:
                current['query'] += sentences[sentence].count(word)
                current['idf'] += idfs[word]

        current['qtd'] = current['query'] / current['len']
    return sorted([sentence for sentence in sentences], key=lambda x: (score[x]['idf'], score[x]['qtd']), reverse=True)[:n]

if __name__ == "__main__":
    main()

