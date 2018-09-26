# TODO: Add flexibility for storing the output files beyond the cwd
# TODO: make function arguments more dynamic
import os

## iterables is a dictionary of compatible iterable types
## with their construction characters as values
iterables = {'tuple':'()', 'list':'[]', 'dict':'{}'}

## Takes an object and ensures that it is a compatible iterable and returns
## the type simplified to just the class name
def get_itertype(obj):
    objtype = str(type(obj))
    for itertype in iterables.keys():
        if itertype in objtype:
            return itertype
    else:
        print("obj not of class: tuple, list or dict")
        return None

# helper function for printing to output file
# TODO: reduce redundancy in get functions so this helper in non-trivial
def print_file(output, obj, formatted):
    output.write(formatted(obj))

## Takes an object and the reference name (optional) and creates
## a python file in the current directory with the object's data
## listed out, each item on it's own line
def rows(obj, ref=None):
    objtype = get_itertype(obj)
    if objtype:
        if not ref:
            ref = objtype
        with open(ref + 'rows.py', 'w+') as output:
            opener, closer = list(str(iterables[objtype]))
            output.write('{} = {}\n'.format(ref, opener))
            if objtype == 'dict':
                print_file(output, obj, get_dict_rows)
            else:
                print_file(output, obj, get_list_rows)
            output.write(closer)

## Takes an object and the reference name (optional) and creates
## a python file in the current directory with the object's data
## in a multi-line string, listed out in a tabular format
def table(obj, ref=None):
    objtype = get_itertype(obj)
    if objtype:
        if not ref:
            ref = objtype
        with open(ref + 'table.py', 'w+') as output:
            output.write("\"\"\"\n")
            if objtype == 'dict':
                print_file(output, obj, get_dict_table)
            else:
                print_file(output, obj, get_list_table)
            output.write("\"\"\"")

## The get functions build the formatted strings to be printed to the output file
def get_dict_rows(dct):
    string = ""
    for k, v in dct.items():
        string += "\t{} : {},\n".format(repr(k), repr(v))
    return string

def get_list_rows(lst):
    string = ""
    for item in lst:
        string += "\t{},\n".format(repr(item))
    return string

def get_dict_table(dct):
    string = "key\t|\tvalue\n\n"
    for k, v in dct.items():
        string += '{}\t|\t{}\n'.format(k, v)
    return string

def get_list_table(lst):
    string = "index\t\t|\t\titem\n\n"
    for index, item in enumerate(lst):
        spaces = " " * (12 - len(str(index)))
        string += '{}{}|\t\t{}\n'.format(index, spaces, item)
    return string

#################################################################################

# test

food =  {'a':'apple','b':'banana','c':'carrot'}
nums = [5,4,6,3,67,9]
rows(food, 'food')
table(food, 'food')
table(nums, 'nums')
rows(nums, 'nums')
