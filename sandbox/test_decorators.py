def parent(num):

    def first_child():
        return "Printing from the first_child() function."

    def second_child():
        return "Printing from the second_child() function."

    try:
        assert num == 10
        return first_child
    except AssertionError:
        return second_child


def my_decorator(some_function):

    def wrapper():

        print("Something is happening before some_function() is called.")

        some_function()

        print("Something is happening after some_function() is called.")

    return wrapper


def just_some_function():
    print("Wheee!")

