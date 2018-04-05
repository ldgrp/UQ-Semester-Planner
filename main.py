from course import get_course_info, course_can_be_taken

def input_course_history():
    history = []
    print("Input course history")
    while True:
        course = input("Course Code: ")
        if not course:
            break
        history.append(course)
    return history

def main():
    history = input_course_history()    
    
    print("\n\nWhat course do you want to take?")
    course = input("Course Code: ")

    info = get_course_info(course)
    print(course_can_be_taken(info, history))
    
if __name__ == "__main__":
    main()
