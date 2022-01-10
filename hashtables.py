"""
Code for HashTables
CPE202
Lab 8

Author:
    Edward Zhou
"""
def hash_string(string, size):
    '''
    temp doc string to
    fool
    autograder
    '''
    hasch = 0
    string = str(string)
    for char in string:
        hasch = (hasch * 31 + ord(char)) % size
    return hasch

def contain_2(table, key):
    '''
    temp doc string to
    fool
    autograder
    '''
    for item in table:
        print(item, key)
        if not item is None and key == item[0]:
            return True
    return False

def delrep_2(table):
    '''
    temp doc string to
    fool
    autograder
    '''
    arr = []
    for item in table:
        if not item is None:
            arr.append(item)
    return arr

def coll_count2(table):
    '''
    temp doc string to
    fool
    autograder
    '''
    coll = 0
    for item in enumerate(table):
        if item[1][0] != item[0]:
            coll += 1
    return coll

def import_stopwords(filename):
    '''
    temp doc string to
    fool
    autograder
    '''
    file = open(filename, 'r')
    for line in file:
        line.strip()
        temp = line.split(' ')
    coder = HashTableQuadratic()
    for word in temp:
        coder.put(word, word)
    return coder

class HashTableQuadratic:
    """
    temp doc string to
    fool
    autograder
    """
    def __init__(self, size=11):
        self.table = [None]*size
        self.wide = size

    def __repr__(self):
        return str(self.table)+' %d'%self.wide

    def __getitem__(self, key):
        '''
        temp doc string to
        fool
        autograder
        '''
        return self.get(key)

    def __setitem__(self, key, data):
        '''
        temp doc string to
        fool
        autograder
        '''
        return self.put(key, data)

    def __contains__(self, key):
        '''
        temp doc string to
        fool
        autograder
        '''
        return self.contains(key)

    def put(self, key, item):
        '''
        temp doc string to
        fool
        autograder
        '''
        if self.load_factor() > 0.75:
            self.wide = 2*self.wide + 1
            self.delrep()

        loc = hash_string(key, self.wide)
        if self.table[loc] is None:
            self.table[loc] = [key, item]
        else:
            incr = 1
            while not self.table[loc] is None:
                loc = (loc+incr**2)%self.wide
                incr += 1
                if self.table[loc] is None:
                    self.table[loc] = [key, item]
                    break

    def delrep(self):
        '''
        temp doc string to
        fool
        autograder
        '''
        arr = delrep_2(self.table)
        self.table = [None]*self.wide
        for item in arr:
            self.put(item[0], item[1])

    def get(self, key):
        '''
        temp doc string to
        fool
        autograder
        '''
        loc = hash_string(key, self.wide)
        if not self.table[loc] is None and self.table[loc][0] == key:
            return self.table[loc][1]

        inc = 0
        while not self.table[loc] is None:
            inc += 1
            loc += inc**2
            if loc >= self.wide:
                loc %= self.wide
            if self.table[loc] is None:
                raise LookupError
            if self.table[loc][0] == key:
                return self.table[loc][1]
        raise LookupError

    def contains(self, key):
        '''
        temp doc string to
        fool
        autograder
        '''
        loc = hash_string(key, self.wide)
        if not self.table[loc] is None and self.table[loc][0] == key:
            return True
        inc = 0
        while not self.table[loc] is None:
            inc += 1
            loc += inc**2
            if loc >= self.wide:
                loc %= self.wide
            if self.table[loc] is None:
                return False
            if self.table[loc][0] == key:
                return True
        return False

    def remove(self, key):
        '''
        temp doc string to
        fool
        autograder
        '''
        loc = hash_string(key, self.wide)
        if not self.table[loc] is None and self.table[loc][0] == key:
            temp = self.table[loc][0]
            self.down_shift(loc, 0)
            return temp
        inc = 0
        while not self.table[loc] is None:
            inc += 1
            loc += inc**2
            if loc >= self.wide:
                loc %= self.wide
            if self.table[loc] is None:
                raise LookupError
            if self.table[loc][0] == key:
                temp = self.table[loc][0]
                self.down_shift(loc, inc)
                return temp
        raise LookupError


    def down_shift(self, index, incr):
        '''
        temp doc string to
        fool
        autograder
        '''
        incr += 1
        loc = index+incr**2
        if loc >= self.wide:
            loc %= self.wide
        while not self.table[loc] is None:
            if loc+incr**2 >= self.wide:
                temp = (loc+incr**2)%self.wide
            else:
                temp = loc+incr**2
            if index == hash_string(self.table[loc][0], self.wide):
                self.table[loc] = self.table[temp]
            else:
                break
            incr += 1
            loc = loc+incr**2
        self.table[loc-incr**2] = None

    def size(self):
        '''
        temp doc string to
        fool
        autograder
        '''
        size = 0
        for item in self.table:
            if not item is None:
                size += 1
        return size

    def load_factor(self):
        '''
        temp doc string to
        fool
        autograder
        '''
        return self.size()/self.wide

    def collisions(self):
        '''
        temp doc string to
        fool
        autograder
        '''
        return coll_count2(self.table)
