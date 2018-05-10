class Employee:
    def __init__(self, first, last):
        #self.first = first # replace by caling setter for the fullname property
        #self.last = last   # for the fullname property
        #self.email = first.lower() + "." + last.lower() + "@gmail.com" #replaced by a method
        self.fullname_set = first + " " + last

    @property     
    def email(self):
        first = self.first if self.first is not None else ''
        last = self.last if self.last is not None else ''
        return first.lower() + "." + last.lower() + "@gmail.com"

    @property    
    def fullname(self):
        first = self.first if self.first is not None else ''
        last = self.last if self.last is not None else ''
        return first + " " + last

    @fullname.setter
    #def fullname(self, name):  # can I use a different method name ?
    def fullname_set(self, name):  # using a different name to tease out where ?
        first, last = name.split(" ")
        self.first = first
        self.last = last    

    @fullname.deleter
    def fullname(self):
        print(f"Deleting name: {self.first} {self.last}")
        self.first = None
        self.last = None    

 
if __name__ == "__main__":

    emp1 = Employee("Jane", "Smith")

    # emp1.first = "Jim" # use setter instead
    #emp1.fullname = "Jim Jones"

    print(emp1.first)   # should probably take these lines out so as not to directly access
    print(emp1.last)    # object's variables

    # print(emp1.email()) # don't want this beacause that would break legacy code that accessed email 
                          # as an attribute
    print(emp1.email)     # access email like an attribute even though it is a method                    

    # print(emp1.fullname()) # have also converted fullname method to be accessed like an attribute
    print(emp1.fullname)  # also access fullname like an attribute even though it is a method

    del emp1.fullname

    print(emp1.fullname)

    emp1.fullname_set = "Jimmy Page"

    print(emp1.fullname)
    print(emp1.email)
