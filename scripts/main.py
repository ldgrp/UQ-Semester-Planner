from course import get_course_info, course_can_be_taken, is_course_code

import csv

PATH_TO_HISTORY = "history.csv"

def input_course_history():
    history = []
    print("Input course history")
    while True:
        course = input("Course Code: ")
        if not course:
            break
        history.append(course)
    return history

def read_history_from_file():
    with open(PATH_TO_HISTORY) as historyfile:
        historyreader = csv.reader(historyfile)
        history = [row[0] for row in historyreader]
        history = [row for row in history if is_course_code(row)]
    return history

def main():
    print("1) Manual input")
    print("2) Read from file.")

    choice = input("Input: ")
    history = []
    if choice == '1':
        history = input_course_history()    
    elif choice == '2':
        history = read_history_from_file()

    print(history)

    print("\n\nWhat course do you want to take?")
    course = input("Course Code: ")

    info = get_course_info(course)
    print(course_can_be_taken(info, history))
    
if __name__ == "__main__":
    main()
