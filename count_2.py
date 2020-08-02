from bs4 import BeautifulSoup
import csv
import os
# it gets value of variable in the file
# it takes ('name of the variable','location of the line','collections of line')


def wrapper_example_function(original_function):
    def wrapper(f_var, *args):
        print("wrapper ran")
        return(original_function(f_var, *args))

    return wrapper

# this function takes single line as argument. This line must contain an '=' symbol
# otherwise unexpected error will show up


def get_value_of_variable(single_line_from_file):
    # The step written below captures the RHS of the equation or = in JAVASCRIPT
    variable_value = single_line_from_file.split('=')[1]
    # variable_value mei variable ki value " value  " mei hoti hai
    # variable_value[1:-1] karne se inverted commas hat jate hai
    # when "let classList" is passed as an argument it return a comma separated string
    return variable_value[1:-1]


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

# this function searches names of students in the arrival times list.
# if they arrived then the line has their names with their arrival time
# this function takes following arguments
#                   (line in which you want to search, term your want to search)
# it returns TRUE or FALSE


def search_name(single_line_from_file, name_for_search):
    if name_for_search in single_line_from_file:
        return "Present"

    return "Absent"


def check_integerity_of_html(html_file_name):
    # step written below deals with the given file. it get Name of the class and Date of
    # the class conduct from the file name
    if html_file_name.split(' ')[0].lower() != "class":
        # print(html_file_name.split(' ')[0])
        print("File is not created by AL extension for google meet")
        return False

    class_name, date_of_class_conducted = html_file_name.split(
        ' ')[1], html_file_name.split(' ')[3][1:-1]
    date_of_class_conducted = date_of_class_conducted.split(')')[0]
    with open(f'./html_folder/{html_file_name}', encoding="utf8") as html_file:
        # it is a list and each element is the line in the document
        lines = html_file.read().split("\n")

    in_class_name, in_classdate = get_value_of_variable(lines[check_word_in_line(lines, 'let className')[
                                                        0]]), get_value_of_variable(lines[check_word_in_line(lines, 'let classDate')[0]])
    in_class_name = in_class_name.split(' ')[1]

    if class_name == in_class_name:
        if date_of_class_conducted == in_classdate:
            return True

    return False

    # DEBUGGING
    # print("====================================")
    # print(f'_{class_name}_  || _{in_class_name}_')
    # print(f'_{date_of_class_conducted}_  || _{in_classdate}_')
# ================================================================================================#
# ================================================================================================#
# ================================================================================================#
# ================================================================================================#
directories = os.listdir('./html_folder')

with open("Class 8 2020 (2020-07-29) (2).html", encoding="utf8") as html_file:

    # it is a list and each element is the line in the document
    lines = html_file.read().split("\n")


# print("Number of lines is {} in the HTML file".format(len(lines)))


# check_word_in_line = wrapper_example_function(check_word_in_line)
line_no = check_word_in_line(lines, 'let classList')[0]
student_names = get_value_of_variable(lines[line_no]).split(',')


# print(student_names)
# getting the arrival timings row
line_no = check_word_in_line(lines, 'let _arrivalTimes')[0]
number_of_present = 0
for student_name in student_names:
    if search_name(lines[line_no].lower(), student_name.lower()) == "Present":
        number_of_present = number_of_present + 1


print(number_of_present)
