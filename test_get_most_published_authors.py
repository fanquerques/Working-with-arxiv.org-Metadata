"""CSC108/A08: Fall 2021 -- Assignment 3: arxiv.org

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Anya Tafliovich.

"""

import copy
import unittest
from arxiv_functions import get_most_published_authors as get_mpas
from arxiv_functions import EXAMPLE_ARXIV

EXAMPLE_ARXIV_1 = {
    '001': {
        'identifier': '001',
        'title': 'Funtions and graphs',
        'created': '2020-01-01',
        'modified': None,
        'authors': [('Laura', 'Taalman'), ('Peter', 'Kohn')],
        'abstract': '''Functions and their properties will be at the
core of everything we study in this text.'''        
    },
    '002': {
        'identifier': '002',
        'title': 'Limits',
        'created': '2020-01-01',
        'modified':'2021-02-14',
        'authors': [('Laura', 'Taalman')],
        'abstract': '''Limits are the backbone of calculus'''          
    },
    '003': {
        'identifier': '003',
        'title': 'Drivatives',
        'created': None,
        'modified':'2021-03-11',
        'authors': [('Peter', 'Kohn')],
        'abstract': '''Limits are the backbone of calculus'''         
    }
}

EXAMPLE_ARXIV_2 = {
    '001': {
        'identifier': '001',
        'title': 'Funtions and graphs',
        'created': '2020-01-01',
        'modified': None,
        'authors': [],
        'abstract': '''Functions and their properties will be at the
core of everything we study in this text.'''        
    },
    '002': {
        'identifier': '002',
        'title': 'Limits',
        'created': '2020-01-01',
        'modified':'2021-02-14',
        'authors': [],
        'abstract': '''Limits are the backbone of calculus'''          
    },
    '003': {
        'identifier': '003',
        'title': 'Drivatives',
        'created': None,
        'modified':'2021-03-11',
        'authors': [],
        'abstract': '''Limits are the backbone of calculus'''         
    }
}

EXAMPLE_ARXIV_3 = {
    '001': {
        'identifier': '001',
        'title': 'Funtions and graphs',
        'created': '2020-01-01',
        'modified': None,
        'authors': [('Peter', 'Kohn')],
        'abstract': '''Functions and their properties will be at the
core of everything we study in this text.'''        
    },
    '002': {
        'identifier': '002',
        'title': 'Limits',
        'created': '2020-01-01',
        'modified':'2021-02-14',
        'authors': [],
        'abstract': '''Limits are the backbone of calculus'''          
    },
    '003': {
        'identifier': '003',
        'title': 'Drivatives',
        'created': None,
        'modified':'2021-03-11',
        'authors': [],
        'abstract': '''Limits are the backbone of calculus'''         
    }
}

EXAMPLE_ARXIV_4 = {
    '001': {
        'identifier': '001',
        'title': 'Funtions and graphs',
        'created': '2020-01-01',
        'modified': None,
        'authors': [('Laura', 'Taalman'), ('Peter', 'Kohn'),
                    ('Author', 'Name.A'), ('Author', 'Name.B'),
                    ('Author', 'Name.C')],
        'abstract': '''Functions and their properties will be at the
core of everything we study in this text.'''        
    },
    '002': {
        'identifier': '002',
        'title': 'Limits',
        'created': '2020-01-01',
        'modified':'2021-02-14',
        'authors': [('Laura', 'Taalman'), ('Peter', 'Kohn'),
                    ('Author', 'Name.A'), ('Author', 'Name.B'),
                    ('Author', 'Name.D'), ('Author', 'Name.E')],
        'abstract': '''Limits are the backbone of calculus.'''          
    },
    '003': {
        'identifier': '003',
        'title': 'Drivatives',
        'created': None,
        'modified':'2021-03-11',
        'authors': [('Laura', 'Taalman'), ('Peter', 'Kohn'),
                    ('Author', 'Name.A'), ('Author', 'Name.B'),
                    ('Author', 'Name.D'), ('Author', 'Name.E'),
                    ('Author', 'Name.F'), ('Author', 'Name.G')],
        'abstract': '''Limits are the backbone of calculus'''         
    }
}

EXAMPLE_ARXIV_5 = {
    '001': {
        'identifier': '001',
        'title': 'Funtions and graphs',
        'created': '2020-01-01',
        'modified': None,
        'authors': [('A', 'C'), ('B', 'D'),
                    ('F', 'E'), ('A', 'B'),
                    ('C', 'D')],
        'abstract': '''Functions and their properties will be at the
core of everything we study in this text.'''        
    },
    '002': {
        'identifier': '002',
        'title': 'Limits',
        'created': '2020-01-01',
        'modified':'2021-02-14',
        'authors': [('A', 'C'), ('B', 'D'),
                    ('G', 'E'), ('B', 'C'),
                    ('A', 'B'), ('E', 'E')],
        'abstract': '''Limits are the backbone of calculus.'''          
    },
    '003': {
        'identifier': '003',
        'title': 'Drivatives',
        'created': None,
        'modified':'2021-03-11',
        'authors': [('A', 'C'), ('P', 'K'),
                    ('G', 'S'), ('A', 'N'),
                    ('B', 'D'), ('A', 'B'),
                    ('J', 'F'), ('L', 'G')],
        'abstract': '''Limits are the backbone of calculus'''         
    }
}
class TestGetMostPublishedAuthors(unittest.TestCase):
    """Test the function get_most_published_authors."""

    def test_handout_example(self):
        """Test get_most_published_authors with the handout example.
        """
        arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
        expected = [('Bretscher', 'Anna'),
                    ('Ponce', 'Marcelo'),
                    ('Tafliovich', 'Anya Y.')]
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_same_amount_of_publishes(self):
        """Test the function get_most_published_authors when all the 
        authors have the same amount of published articles in EXAMPLE_ARXIV_1. 
        """
        arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV_1)
        expected = [('Laura', 'Taalman'),
                    ('Peter', 'Kohn')]
        actual =get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)        

    def test_no_authors(self):
        """Test the function get_most_published_authors when EAMPLE_ARXIV_2
        contains no authors for all articals. 
        """
        arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV_2)
        expected = []
        actual =get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_single_author(self):
        """Test the function get_most_published_authors when EAMPLE_ARXIV_3
        only contains a single author. 
        """
        arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV_3)
        expected = [('Peter', 'Kohn')]
        actual =get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_many_authors(self):
        """Test the function get_most_published_authors when EAMPLE_ARXIV_4
        contains many authors for each article. 
        """
        arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV_4)
        expected = [ ('Author', 'Name.A'),
                     ('Author', 'Name.B'),
                     ('Laura', 'Taalman'),
                     ('Peter', 'Kohn')]
        actual =get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg) 


    def test_lexicographic_order(self):
        """Test the function get_most_published_authors returns the list of
        most published author from EAMPLE_ARXIV_5 in lexicographic order.
        """
        arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV_5)
        expected = [ ('A', 'B'), ('A', 'C'), ('B', 'D')]
        actual =get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)


def message(test_case: dict, expected: list, actual: object) -> str:
    """Return an error message saying the function call
    get_most_published_authors(test_case) resulted in the value
    actual, when the correct value is expected.

    """

    return ("When we called get_most_published_authors(" + str(test_case) +
            ") we expected " + str(expected) +
            ", but got " + str(actual))


if __name__ == '__main__':
    unittest.main(exit = False)
