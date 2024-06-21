class Node:
    '''Node for use with doubly-linked list'''
    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None

class OrderedList:
    '''A doubly-linked ordered list of items, from lowest (head of list) to highest (tail of list)'''

    def __init__(self):
        '''Use ONE dummy node as described in class
           ***No other attributes***
           DO NOT have an attribute to keep track of size'''
        self.sentinel = None

    def is_empty(self):
        '''Returns True if OrderedList is empty
            MUST have O(1) performance'''
        if self.sentinel is None:
            return True
        return False

    def add(self, item):
        '''Adds an item to OrderedList, in the proper location based on ordering of items
           from lowest (at head of list) to highest (at tail of list) and returns True.
           If the item is already in the list, do not add it again and return False.
           MUST have O(n) average-case performance.  Assume that all items added to your 
           list can be compared using the < operator and can be compared for equality/inequality.
           Make no other assumptions about the items in your list'''
        newnode = Node(item)
        if self.sentinel is None:       #list is empty
            self.sentinel = newnode
            self.sentinel.prev = newnode
            self.sentinel.next = newnode

        elif self.sentinel.item > item or self.sentinel.item == item:  # when item is smallest item
            second = self.sentinel
            third = self.sentinel.prev
            newnode.next = self.sentinel  # set newnode as sentinel
            newnode.prev = self.sentinel.prev
            self.sentinel = newnode
            second.prev = self.sentinel  # old sentinel points back to new sentinel
            third.next = self.sentinel  #last item now points to new sentinel

        elif self.sentinel.prev.item < item or self.sentinel.prev.item == item : #when item is biggest item
            secondlast = self.sentinel.prev
            newnode.next = self.sentinel        #newnode points back to secondlast and front to sentinel
            newnode.prev = secondlast
            self.sentinel.prev = newnode    #sentinel points back to secondlast
            secondlast.next = newnode       #secondlast points to last
        else:       #item is not biggest nor smallest
            travel = self.sentinel
            while travel.item < item:
                travel = travel.next

            prevnode = travel.prev      #newnode points back and forwards
            newnode.next = travel
            newnode.prev = prevnode

            prevnode.next = newnode #previous node points to newnode
            travel.prev = newnode #node ahead points backwards to newnode

    def remove(self, item):
        '''Removes the first occurrence of an item from OrderedList. If item is removed (was in the list) 
           returns True.  If item was not removed (was not in the list) returns False
           MUST have O(n) average-case performance'''
        travel = self.sentinel
        if item > self.sentinel.prev.item:
            return False        #if item that we're looking for is bigger than all items

        while travel.item < item:
            travel = travel.next
        if item == travel.item:
            previtem = travel.prev
            nextitem = travel.next
            previtem.next = nextitem
            nextitem.prev = previtem
            return True
        else:
            return False


    def index(self, item):
        '''Returns index of the first occurrence of an item in OrderedList (assuming head of list is index 0).
           If item is not in list, return None
           MUST have O(n) average-case performance'''
        travel = self.sentinel
        if item > self.sentinel.prev.item:
            return None

        idx = 0
        while travel.item < item:
            travel = travel.next
            idx += 1
        if item == travel.item:
            return idx
        else:
            return None

    def pop(self, index):
            '''Removes and returns item at index (assuming head of list is index 0).
               If index is negative or >= size of list, raises IndexError
               MUST have O(n) average-case performance'''
            if index < 0:
                raise IndexError
            travel = self.sentinel

            for i in range(index):
                travel = travel.next
                if travel == self.sentinel:
                    raise IndexError


            previtem = travel.prev
            nextitem = travel.next
            previtem.next = nextitem
            nextitem.prev = previtem
            if self.sentinel == self.sentinel.next:
                self.sentinel = None

            if travel == self.sentinel:
                self.sentinel = nextitem

            return travel.item


    def search(self, item, current = None):
        '''Searches OrderedList for item, returns True if item is in list, False otherwise"
           To practice recursion, this method must call a RECURSIVE method that
           will search the list
           MUST have O(n) average-case performance'''
        if current is None:
            current = self.sentinel
        if current.item == item:
            return True
        if current.next == self.sentinel:
            return False
        return self.search(item, current.next)

    def python_list(self):
        '''Return a Python list representation of OrderedList, from head to tail
           For example, list with integers 1, 2, and 3 would return [1, 2, 3]
           MUST have O(n) performance'''
        if self.sentinel == self.sentinel.prev:
            return [self.sentinel.item.char]

        newlist = [self.sentinel.item.char]
        travel = self.sentinel.next

        while travel != self.sentinel.prev:
            tempitem = travel.item
            newlist.append(tempitem.char)
            travel = travel.next
        newlist.append(travel.item.char)
        return newlist

    def python_list_reversed(self , current = None):
        '''Return a Python list representation of OrderedList, from tail to head, using recursion
           For example, list with integers 1, 2, and 3 would return [3, 2, 1]
           To practice recursion, this method must call a RECURSIVE method that
           will return a reversed list
           MUST have O(n) performance'''
        if self.sentinel == self.sentinel.prev:
            return [self.sentinel.item]

        if current == self.sentinel:
            return [current.item]


        if current is None:
            current = self.sentinel.prev

        return [current.item] + self.python_list_reversed(current.prev)

    def size(self , current = None):
        '''Returns number of items in the OrderedList
           To practice recursion, this method must call a RECURSIVE method that
           will count and return the number of items in the list
           MUST have O(n) performance'''
        if self.sentinel == self.sentinel.prev:
            return 1

        if current == self.sentinel:
            return 1

        if current is None:
            current = self.sentinel.prev

        return 1 + self.size(current.prev)
