#A.1 Create a list containing any 4 strings
l_one = ['hello', 'my', 'name', 'is']
#A.2 Print the 3rd item in the list - remember how Python indexes lists!
print(l_one[2])
#A.3 Print the 1st and 2nd item in the list using [:] index slicing.
print(l_one[:2])
#A.4 Add a new string with text “last” to the end of the list and print the list.
l_one.append('last')
print(l_one)
#A.5 Get the list length and print it.
len(l_one)
print(len(l_one))
#A.6 Replace the last item in the list with the string “new” and print
l_one[-1]= "new"
print (l_one)
#B.1 Convert the list into a normal sentence with join(), then print.
sentence_words = ['I', 'am', 'learning', 'Python', 'to', 'manage', 'large', 'datasets', 'and', 'visualize', 'them']
space = " "
print (space.join(sentence_words))
#B.2 Reverse the order of this list using the .reverse() method, then print. Your output should begin with [“them”, ”visualize”, … ].
sentence_words.reverse()
print(sentence_words)
#B.3 Now user the .sort() method to sort the list using the default sort order.
sentence_words.sort()
#B.4 Perform the same operation using the sorted() function. Provide a brief description of how the sorted() function differs from the .sort() method.
sorted(sentence_words)
#sorted() is used with lists or a series of strings, while .sort() works only for lists. In addition, .sort modifies the list in place.

# Part C, Define random function.
from random import randint
# this returns random integer: 100 <= number <= 1000
def random_func(ub, lb=0):
    rand_output=randint(lb, ub)
    print(rand_output)
    return(rand_output)

assert(0 <= random_func(100) <= 100)
assert(50 <= random_func(100, lb = 50) <= 100)

#Part D, String Formatting Function
def s_function(title, n):
    print("The number %d best seller today is: %s." % (n,title))

#E. Password Validation Function
def password_func(password):
    s_chars=['!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=']
    pass_length=len(password)
    if pass_length<8 or pass_length>14:
        print("Enter a password with correct characters")
    if len([x for x in password if x.isdigit()])< 2:
        print("Enter a password with at least two digits")
    if len([x for x in password if x.isupper()])< 1:
        print("Enter a password with at least one uppercase letter")
    if any((c in s_chars) for c in password):
        print("Success!")
    else:
        print("Add a special character")

password_func('MITDusp42!')

#F. Exponentiation Function
def exp_func(base, exp):
    result = 1
    while exp:
        if exp & 1:
            result *= base
        exp >>= 1
        base *= base
    return result

print(exp_func(2,4))

#https://codereview.stackexchange.com/questions/127020/exponentiation-using-while-loop-in-python
