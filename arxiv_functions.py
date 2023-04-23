"""CSC108/A08: Fall 2021 -- Assignment 3: arxiv.org

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Anya Tafliovich.

"""

import copy  # needed in examples of functions that modify input dict
from typing import Dict, List, TextIO

# remove unused constants from this import statement when you are
# finished your assignment
from constants import (ID, TITLE, CREATED, MODIFIED, AUTHORS,
                       ABSTRACT, END, SEPARATOR, NameType,
                       ArticleValueType, ArticleType, ArxivType)


EXAMPLE_ARXIV = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''},
    '031': {
        'identifier': '031',
        'title': 'Calculus is the best course ever',
        'created': None,
        'modified': '2021-09-02',
        'authors': [('Breuss', 'Nataliya')],
        'abstract': '''We discuss the reasons why Calculus I
is the best course.'''},
    '067': {'identifier': '067',
            'title': 'Discrete Mathematics is the best course ever',
            'created': '2021-09-02',
            'modified': '2021-10-01',
            'authors': [('Bretscher', 'Anna'), ('Pancer', 'Richard')],
            'abstract': ('We explain why Discrete Mathematics is the best ' +
                         'course of all times.')},
    '827': {
        'identifier': '827',
        'title': 'University of Toronto is the best university',
        'created': '2021-08-20',
        'modified': '2021-10-02',
        'authors': [('Bretscher', 'Anna'),
                    ('Ponce', 'Marcelo'),
                    ('Tafliovich', 'Anya Y.')],
        'abstract': '''We show a formal proof that the University of
Toronto is the best university.'''},
    '042': {
        'identifier': '042',
        'title': None,
        'created': '2021-05-04',
        'modified': '2021-05-05',
        'authors': [],
        'abstract': '''This is a very strange article with no title
and no authors.'''}
}

EXAMPLE_BY_AUTHOR = {
    ('Ponce', 'Marcelo'): ['008', '827'],
    ('Tafliovich', 'Anya Y.'): ['008', '827'],
    ('Bretscher', 'Anna'): ['067', '827'],
    ('Breuss', 'Nataliya'): ['031'],
    ('Pancer', 'Richard'): ['067']
}


# We provide this PARTIAL docstring to show the use of examples.
def make_author_to_articles(id_to_article: ArxivType) -> Dict[NameType,
                                                              List[str]]:
    """Return a dict that maps each author name to a list (sorted in
    lexicographic order) of IDs of articles written by that author,
    based on the information in id_to_article.

    >>> make_author_to_articles(EXAMPLE_ARXIV) == EXAMPLE_BY_AUTHOR
    True
    """
    new_dict = {}

    for sub in id_to_article:
        for name in id_to_article[sub][AUTHORS]:#key error
            if name not in new_dict:
                new_dict[name] = []
            if name in new_dict:
                new_dict[name].append(id_to_article[sub][ID])
            new_dict[name].sort()
    return new_dict

def get_coauthors(id_to_article: ArxivType,
                  author: NameType) -> List[NameType]:
    """Return a list of coauthors of the author in lexcogtaphic order.

    >>> get_coauthors(EXAMPLE_ARXIV, ('Tafliovich', 'Anya Y.'))
    [('Bretscher', 'Anna'), ('Ponce', 'Marcelo')]

    >>> get_coauthors(EXAMPLE_ARXIV, ('Bretscher', 'Anna'))
    [('Pancer', 'Richard'), ('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]
    """
    result = []
    for sub in id_to_article:
        for name in id_to_article[sub][AUTHORS]:
            if author in id_to_article[sub][AUTHORS] and name != author:
                result.append(name)
    result = list(sorted(dict.fromkeys(result)))
    return result

def get_most_published_authors(id_to_article: ArxivType) -> List[NameType]:
    """Return a list of authors (or single author) who published the most
    articles in lexicographic order.

    >>> get_most_published_authors(EXAMPLE_ARXIV)
    [('Bretscher', 'Anna'), ('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]
    """
    most_published_author = []
    longest_len = 0
    author_articles = make_author_to_articles(id_to_article)

    for key in author_articles:
        if len(author_articles[key]) > longest_len:
            longest_len = len(author_articles[key])
    for key in author_articles:
        if len(author_articles[key]) == longest_len:
            most_published_author.append(key)
    return sorted(most_published_author)

def suggest_collaborators(id_to_article: ArxivType,
                          author: NameType) -> List[NameType]:
    """Return a list of authors with whom the author is encouraged to
    collaborate in lexicographic order.Criteria for collaboration is to be a
    collaborator of the author's coauthor, not including previous coauthors of
    the author nor the author him/herself.

    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Pancer', 'Richard'))
    [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]

    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Tafliovich', 'Anya Y.'))
    [('Pancer', 'Richard')]
    """
    suggest = []
    author_coauthor = get_coauthors(id_to_article, author)
    for name in author_coauthor:
        for co_coauthor in get_coauthors(id_to_article, name):
            if co_coauthor != author and co_coauthor not in author_coauthor:
                suggest.append(co_coauthor)
    return sorted(suggest)

def has_prolific_authors(author_articles: Dict[NameType, List[str]],
                         article_info: ArticleType, threshold: int) -> bool:
    """Return true if and only if the article contains an author that has
    published a number of articles greater or equal to the threshold value.

    >>> author_to_articles = make_author_to_articles(EXAMPLE_ARXIV)
    >>> has_prolific_authors(author_to_articles, EXAMPLE_ARXIV['008'], 2)
    True

    >>> has_prolific_authors(author_to_articles, EXAMPLE_ARXIV['031'], 2)
    False
    """
    for name in article_info[AUTHORS]:
        if len(author_articles[name]) >= threshold:
            return True
    return False

# We provide this PARTIAL docstring to show use of copy.deepcopy.
def keep_prolific_authors(id_to_article: ArxivType,
                          min_publications: int) -> None:
    """Update id_to_article so that it contains only articles published by
    authors with min_publications or more articles published. As long
    as at least one of the authors has min_publications, the article
    is kept.

    >>> arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
    >>> keep_prolific_authors(arxiv_copy, 2)
    >>> len(arxiv_copy)
    3
    >>> '008' in arxiv_copy and '067' in arxiv_copy and '827' in arxiv_copy
    True
    """

    ids_to_remove = []
    author_articles = make_author_to_articles(id_to_article)
    for sub in id_to_article:
        if not has_prolific_authors(author_articles, id_to_article[sub],
                                    min_publications):
            ids_to_remove.append(sub)
    for sub in ids_to_remove:
        if sub in id_to_article:
            id_to_article.pop(sub)

# Note that we do not include example calls since the function works
# on an input file.
def get_title(line: str) -> str:
    """Return the input string as title, if and only if the input string
    is not ''.
    """
    title = line
    if line == '':
        title = None
    return title

def get_created_date(line: str) -> str:
    """Return the input string as created date, if and only if the input string
    is not ''.
    """
    created_date = line
    if line == '':
        created_date = None
    return created_date

def get_modified_date(line: str) -> str:
    """Return the input string as modified date, if and only if the input string
    is not ''.
    """
    modified_date = line
    if line == '':
        modified_date = None
    return modified_date

def get_abstracts(afile_list: List[str]) -> List[List[str]]:
    """Return the a list where each sublist sequentially coresponds to the
    abstract in the afile.
    Percondition: afile is not be empty.
    """
    abstract_list = []
    start_slice = 0
    i = 0
    end_slice = 0
    while i in range(len(afile_list)):
        if afile_list[i] == '\n':
            start_slice = i + 1
        if afile_list[i] == 'END\n':
            end_slice = i
            abstract_list.append(afile_list[start_slice:end_slice])
        i += 1
    return abstract_list

def abstract_extractor(sub_abstract_list: List[str]) -> str:
    """Return the content of sub_abstract_list as a concatenated string.
    Percondition: afile is not be empty.
    """
    abstract_str = ''
    i = 0
    while i < len(sub_abstract_list):
        if i == len(sub_abstract_list) - 1:
            abstract_str += sub_abstract_list[i].strip('\n')
        else:
            abstract_str += sub_abstract_list[i]
        i += 1
    return abstract_str

def read_arxiv_file(afile: TextIO) -> ArxivType:
    """Return a dict containing all arxiv information in afile.

    Precondition: afile is open for reading
                  afile is in the format described in the handout
    """
    meta_dict = {}
    sub_dict = {}
    i = 0
    afile_list = afile.readlines()
    abstracts = get_abstracts(afile_list)
    author_list = []
    j = 0
    while i < len(afile_list):
        sub_dict[ID] = afile_list[i].strip('\n')
        i += 1
        sub_dict[TITLE] = get_title(afile_list[i].strip('\n'))
        i += 1
        sub_dict[CREATED] = get_created_date(afile_list[i].strip('\n'))
        i += 1
        sub_dict[MODIFIED] = get_modified_date(afile_list[i].strip('\n'))
        i += 1
        if afile_list[i] == '\n':
            sub_dict[AUTHORS] = []
            i += 1
        else:
            while afile_list[i] != '\n':
                author_list.append(tuple(afile_list[i].strip('\n')
                                         .split(SEPARATOR)))
                i += 1
        sub_dict[AUTHORS] = sorted(author_list)
        sub_dict[ABSTRACT] = abstract_extractor(abstracts[j])
        j += 1
        while afile_list[i] != 'END\n':
            i += 1
        meta_dict[sub_dict[ID]] = sub_dict
        sub_dict = {}
        author_list = []
        i += 1
    return meta_dict

if __name__ == '__main__':

    import doctest
    doctest.testmod()
    with open('example_data.txt') as example_data:
        example_arxiv = read_arxiv_file(example_data)
        print('Did we produce a correct dict? ',
              example_arxiv == EXAMPLE_ARXIV)

     #uncomment to work with a larger data set
    with open('data.txt') as data:
        arxiv = read_arxiv_file(data)

    author_to_articles = make_author_to_articles(arxiv)
    most_published = get_most_published_authors(arxiv)
    print(most_published)
    print(get_coauthors(arxiv, ('Varanasi', 'Mahesh K.')))  # one
    print(get_coauthors(arxiv, ('Chablat', 'Damien')))  # many
