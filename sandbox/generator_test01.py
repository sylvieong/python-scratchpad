import math

def get_primes_returns_list(input_list):
    return [element for element in input_list if is_prime(element)]

def get_primes_generator_function(start_number):
    number = start_number
    while(True):
        if is_prime(number):
            yield number
        number += 1

# not germane to the example, but here's a possible implementation of
# is_prime...

def is_prime(number):
    if number > 1:
        if number == 2:
            return True
        if number % 2 == 0:
            return False
        for current in range(3, int(math.sqrt(number) + 1), 2):
            if number % current == 0: 
                return False
        return True
    return False

if __name__=="__main__":
    for pn in get_primes_generator_function(0):
        print (pn)
        if pn > 20:
            print("Exiting loop calling generator function")
            break
        #nput("Press Enter to continue...")

    for pn in get_primes_returns_list(list(range(0,100))):
        print (pn)

