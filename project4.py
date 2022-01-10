"""
Code for a Search Engine
CPE202
Project 4

Author: Edward Zhou
"""

import os
import math
import hashtables

class SearchEngine:
    '''
    A bunch of HashTable objects which store words, filenames, and word
        frequencies for those files.
    Attributes:
        stopwords (HashTable): A hash table of words to not include in a
            search.
        doc_length (HashTable): A hash table of filenames and their respective
            word count.
        term_freqs (HashTable): A hash table of words consisting of hash tables
            that have filenames and the word count of said word.
    '''
    def __init__(self, directory, stopwords):
        self.stopwords = stopwords #a hash table
        self.doc_length = hashtables.HashTableQuadratic()
        self.term_freqs = hashtables.HashTableQuadratic()
        self.index_files(directory)

    def read_file(self, infile):
        '''
        Reads in a file labeled as infile.
        Args:
            infile (str): A filename
        Returns:
            temp (array): An array of lines in a text file.
        '''
        file = open(infile, 'r')
        temp = []
        for line in file:
            temp.append(line)
        file.close()
        return temp

    def parse_words(self, lines):
        '''
        Gets the words in a file.
        Args:
            lines (array): An array of lines of text in a text file.
        Returns
            function call (self.exclude_stopwords)
        '''
        words = []
        for line in lines:
            line.strip()
            wordo = line.split()
            for word in wordo:
                symbols = [",", ".", "(", ")", "'"]
                for symbol in symbols:
                    word = word.strip(symbol)
                words.append(word.lower())
        return self.exclude_stopwords(words)

    def exclude_stopwords(self, words):
        '''
        Excludes the stopwords in an array of words.
        Args:
            words (array): An array of words in a file.
        Returns:
            temp (array): An array of words in a file without the stopwords.
        '''
        temp = []
        for word in words:
            in_table = False
            for item in self.stopwords.table:
                if not item is None and word == item[0]:
                    in_table = True
            if not in_table:
                temp.append(word)
        return temp

    def count_words(self, filename, words):
        '''
        Counts the amount of words in a file and adds that to self.term_freqs.
        Args:
            filename (str): The name of a file.
            words (array): The array of words in a file.
        '''
        self.doc_length.put(filename, len(words))
        for word in words:
            if not self.term_freqs.contains(word):
                temp = hashtables.HashTableQuadratic()
                temp.put(filename, 1)
                self.term_freqs.put(word, temp)
            else:
                for item in enumerate(self.term_freqs.table):
                    if not item[1] is None and word == item[1][0]:
                        in_files = False
                        for file in enumerate(\
                            self.term_freqs.table[item[0]][1].table):
                            if not file[1] is None and filename == file[1][0]:
                                self.term_freqs.table[item[0]][1].\
                                table[file[0]][1] += 1
                                in_files = True
                        if not in_files:
                            self.term_freqs.table[item[0]][1].put(filename, 1)

    def index_files(self, directory):
        '''
        Gets all the files in a given folder.
        Args:
            directory (str): The name of a folder that contains files to be
                read in to the search engine.
        '''
        files = os.listdir(directory)
        for file in files:
            full_path = os.path.join(directory, file)
            if os.path.isfile(full_path):
                filename = os.path.splitext(file)
                if filename[1] == '.txt':
                    lines = self.read_file(full_path)
                    words = self.parse_words(lines)
                    self.count_words(file, words)

    def get_wf(self, term_freq):
        '''
        Gets the weight of a file.
        Args:
            tf (int): The number of the searched word in a file.
        Returns:
            wf (float): The weight of the file.
        '''
        if term_freq > 0:
            weight = 1 + math.log(term_freq)
        else:
            weight = 0
        return weight

    def get_scores(self, words):
        '''
        Gets the scores (wf) of files.
        Args:
            words (array): An array of words to look for in files.
        Returns:
            scores (array): An array of the scores of the files.
        '''
        temp = hashtables.HashTableQuadratic()
        for word in words:
            if self.term_freqs.contains(word):
                files = self.term_freqs.get(word)
                for file in files.table:
                    if not file is None and not temp.contains(file[0]):
                        temp.put(file[0], self.get_wf(file[1]))
                    elif not file is None:
                        for freq in temp.table:
                            if not freq is None and freq[0] == file[0]:
                                freq[1] += self.get_wf(file[1])
        scores = []
        for file in temp.table:
            if not file is None and file[1] != 0 and \
               self.doc_length.contains(file[0]):
                scores.append((file[0], file[1] /\
                    self.doc_length.get(file[0])))
        return scores

    def rank(self, scores):
        '''
        Sorts the files by score.
        Args:
            scores (array): An array of scores of files.
        Returns:
            function call (sorted): Sorts the files.
        '''
        return sorted(scores, key=lambda x:x[1], reverse=True)

    def search(self, query):
        '''
        Searches through the files for a given set of words (query).
        Args:
            query (str): A string of word(s) to search for.
        Returns:
            function call (self.rank): A ranked order of files by score.
        '''
        words = query.split()
        seen = []
        for word in words:
            if not word in seen:
                seen.append(word.lower())
        scores = self.get_scores(seen)
        return self.rank(scores)

def searcher():
    '''
    The "main" of the search engine.
    '''
    choice = 'p'
    while choice.lower() != 'q':
        stop_words = hashtables.import_stopwords('stop_words.txt')
        words = input('Enter words: ')
        while not 's: ' in words:
            words = input('Enter words: ')
        search = SearchEngine('docs', stop_words)
        scores = search.search(words)
        for file in scores:
            print(file[0])
        choice = input('Would you like to quit (type Q if yes)? ')

if __name__ == '__main__':
    searcher()
