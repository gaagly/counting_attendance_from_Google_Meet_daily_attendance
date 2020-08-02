from bs4 import BeautifulSoup
import csv

# it gets value of variable in the file
# it takes ('name of the variable','location of the line','collections of line')


def get_value_of_variable(original_function):
    def wrapper(f_var, *args):
        print("wrapper ran")
        return(original_function(f_var, *args))

    return wrapper


def check_word_in_line(lines_from_file, *searched_words):
    word_line_no = []  # this will capture the line number of words in order
    for i, line in enumerate(lines_from_file):
        for searched_word in searched_words:
            if searched_word in line:
                print("Word \"{}\" found in line {}".format(
                    searched_word, i + 1))
                word_line_no.append(i)
                continue  # break ki jagah isko use kiya search karo isko

    print('checking complete')
    return word_line_no  # return the line numbers of the word entered


with open("Class 8 2020 (2020-07-29) (2).html", encoding="utf8") as html_file:

    lines = html_file.read().split("\n")


print("Number of lines is {}".format(len(lines)))
check_word_in_line = get_value_of_variable(check_word_in_line)
for line_no in check_word_in_line(lines, 'let classList', 'let _arrivalTimes'):
    print(lines[line_no])
