from query_course import get_course_info

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
    for course in history:
        print(course, ": ", get_course_info(course))

if __name__ == "__main__":
    main()
