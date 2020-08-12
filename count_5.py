from bs4 import BeautifulSoup
import csv
import os
import datetime
from datetime import datetime, date, time

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
                # print("Word \"{}\" found in line {}".format(
                #     searched_word, i + 1))
                word_line_no.append(i)
                continue  # break ki jagah isko use kiya search karo isko

    # print('checking complete')
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
        print(
            f"File '{html_file_name}' is not created by AL extension for google meet")
        return False

    class_name, date_of_class_conducted = html_file_name.split(
        ' ')[1], html_file_name.split(' ')[3][1:-1]
    date_of_class_conducted = date_of_class_conducted.split(')')[0]
    with open(f'./html_folder/{html_file_name}', encoding='utf8') as html_file:
        # it is a list and each element is the line in the document
        lines = html_file.read().split("\n")

    try:
        in_class_name, in_classdate = get_value_of_variable(lines[check_word_in_line(lines, 'let className')[
                                                            0]]), get_value_of_variable(lines[check_word_in_line(lines, 'let classDate')[0]])
        in_class_name = in_class_name.split(' ')[1]

        if class_name == in_class_name:
            if date_of_class_conducted == in_classdate:
                return True
    except:
        print(f'cannot read {html_file_name}')
        return False

    return False

    # DEBUGGING
    # print("====================================")
    # print(f'_{class_name}_  || _{in_class_name}_')
    # print(f'_{date_of_class_conducted}_  || _{in_classdate}_')

# this function gets the list of classes from the directory
# it first verifies whether files is generated by AL Google Meet attendance extension
# get_list_compatible_files() this function should run first
# it takes a list of files in the compatible folders folder as an argument


def get_list_of_classes(list_of_cptble_files_in_the_directory):
    list_of_class = []

    for item in list_of_cptble_files_in_the_directory:

        if item.split(' ')[1] not in list_of_class:
            list_of_class.append(item.split(' ')[1])

    return list_of_class

# this function makes list of compatible files
# so check_integerity_of_html() function runs only one time
# it saves a lot of time


def get_list_compatible_files(list_of_files):
    cptble_file_name = []

    for item in list_of_files:
        if check_integerity_of_html(item) == True:
            cptble_file_name.append(item)
    print(f'Number of Compatible Files: {len(cptble_file_name)}')
    return cptble_file_name


# The following function wil return the list of filenames of a specific class
# I will use it as a decorator
# EXAMPLE OF A DECORATOR FUNCTION
# def wrapper_example_function(original_function):
#     def wrapper(f_var, *args):
#         print("wrapper ran")
#         return(original_function(f_var, *args))

#     return wrapper


def filter_class_file(original_function):
    def wrapper(list_of_file_names, class_name, *args):
        filtered_list_of_files = []
        for item in list_of_file_names:
            if item.split(' ')[1] == class_name:
                filtered_list_of_files.append(item)
        return original_function(filtered_list_of_files, class_name, *args)

    return wrapper


# This function will get names of all students of a specific class
# from all available files
# it takes list of compatible files and Name of the Class as arguments
# Aim to make it count attendance and date
@filter_class_file
def get_names_from_class(list_of_cptble_files_in_the_directory, class_name):
    student_names = []  # it saves the name, and name should be unique

    for item in list_of_cptble_files_in_the_directory:
        with open(f'./html_folder/{item}', encoding='utf8') as html_file:
            # it is a list and each element is the line in the document
            lines = html_file.read().split("\n")
        if item.split(' ')[1] == class_name:
            line_no = check_word_in_line(lines, 'let classList')[0]

            student_names_from_file = get_value_of_variable(
                lines[line_no]).split(',')

            for name_of_stu in student_names_from_file:
                if name_of_stu.lower().strip() == "":
                    continue
                else:
                    if name_of_stu.lower().strip() not in student_names:
                        student_names.append(name_of_stu.lower().strip())

    print(f'Number of students in Class {class_name} : {len(student_names)}')
    return student_names


# At this point we have list of all students
# so we have to check names in the arrival list all over again
# we can also delete those names too who were never present
# this usually occured when I accidently used other class list
# for the present class
@filter_class_file
def get_stu_attendance_from_class_files(list_of_cptble_files_in_the_directory, class_name, *student_names):
    outer_array = []  # this will contain each student details
    for name_of_stu in student_names:
        inner_array = []  # this will contain elements stu_name, date/absent
        inner_array.append(class_name)
        inner_array.append(name_of_stu)
        present_count = 0
        for item in list_of_cptble_files_in_the_directory:
            with open(f'./html_folder/{item}', encoding='utf8') as html_file:
                # it is a list and each element is the line in the document
                lines = html_file.read().split("\n")
            # gets Date of class conducted
            date_of_class_conducted = get_value_of_variable(
                lines[check_word_in_line(lines, 'let classDate')[0]])
            if search_name(lines[check_word_in_line(lines, 'let _arrivalTimes')[0]].lower(), name_of_stu.lower()) == "Present":
                inner_array.append(date_of_class_conducted)
                # many times, more than one html file is generated
                # it counts present one present per one day
                if inner_array[-2] != date_of_class_conducted:
                    present_count += 1
            else:
                inner_array.append("absent")
            # adding a check that data should not be vague
        inner_array.insert(2, present_count)
        if present_count != 0:
            outer_array.append(inner_array)

    return outer_array



# ================================================================================================#
# ================================================================================================#
# ================================================================================================#
# ================================================================================================#
directories = os.listdir('./html_folder')

# selecting only compatible files
directories = get_list_compatible_files(directories)

for name_of_class in get_list_of_classes(directories):
    students_name_list = get_names_from_class(directories, name_of_class)
    time_stamp = datetime.now()

    with open(f'Class {name_of_class} Attendance {str(time_stamp.strftime("%Y%m%d"))} {str(time_stamp.strftime("%H%M%S"))}.csv', 'a', encoding='utf8') as csv_sample:
        csv_reader = csv.reader(csv_sample)
        csv_writer = csv.writer(csv_sample)
        for stu_data in get_stu_attendance_from_class_files(directories, name_of_class, *students_name_list):
            csv_writer.writerow(stu_data)

    print(
        f'Successfully written data for Class {name_of_class}, {len(get_stu_attendance_from_class_files(directories, name_of_class, *students_name_list))}')
    print('-----------------------------------------------------')
