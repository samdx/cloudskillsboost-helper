import sys
from pathlib import Path as PathlibPath
from config.settings import *
from models.collection import Collection
from models.path import Path
from models.course import Course
from services.launch_browser import launch_browser


# Main class for the CloudSkillsBoost Automation Script
class CloudSkillsBoost:
    def __init__(self):
        self.paths_collection, self.courses_collection, self.labs_collection = self.load_data()

    @staticmethod
    def load_data():
        col_paths = Collection(type='paths', name='Paths Collection')
        col_paths.load_json()

        col_courses = Collection(type='courses', name='Courses Collection')
        col_courses.load_json()

        col_labs = Collection(type='labs', name='Labs Collection')
        col_labs.load_json()

        return col_paths, col_courses, col_labs

    # Task Coordinator
    def tasks_coordinator(self, a_path_id=None, a_course_id=None) -> None:
        """
        Coordinate the tasks for a given path or course.

        :param a_path_id: Path ID.
        :param a_course_id: Course ID.
        """

        mark_complete_video_task = False
        extract_transcript_task = False
        both_tasks = False

        task_selection = True
        while task_selection:
            # Ask for what to do with the selected path id or course id.
            task_to_do = input("WHAT TASK YOU WANT TO GO WITH? (THIS IS A MUST): \n"
                               "\t\t1 - m. Mark Videos Completed (Logged in is required)\n"
                               "\t\t2 - e. Extract Transcripts\n"
                               "\t\t3 - a. Both The Tasks (NOT IMPLEMENTED YET)\n"
                               "\t\t4 - b. Back\n"
                               "\t\t5 - q. Quit\n"
                               "•PLEASE SELECT: ")

            # Set variables accordingly for each selection.
            if task_to_do.lower() == "1" or task_to_do.lower() == "m":
                mark_complete_video_task = True
                task_selection = False
            elif task_to_do.lower() == "2" or task_to_do.lower() == "e":
                extract_transcript_task = True
                task_selection = False
            elif task_to_do.lower() == "3" or task_to_do.lower() == "a":
                both_tasks = True
                task_selection = False
            elif task_to_do.lower() == "4" or task_to_do.lower() == "b":
                return
            elif task_to_do.lower() == "5" or task_to_do.lower() == "q":
                print("Got it. Bye.")
                sys.exit(0)
            else:
                print("Please select a valid choice: 1, 2, 3, or q to quit the program.")
                continue

        #  =======================================================================
        # If no path id, extract transcript for a certain course id only.
        if a_path_id is None and a_course_id:

            if a_course_id in self.courses_collection.collection:
                course_name = self.courses_collection.collection[a_course_id]
            else:
                course_name = '(Unknown Course Yet)'

            # If the user wants to mark the videos as completed
            if mark_complete_video_task:
                heading = f"Mark Complete Videos: {a_course_id} - {course_name.upper()}"
                print(f"\n\033[45m[{heading:^85}]\033[0m")
                a_webdriver = launch_browser(profile_folder=WEBDRIVER_PROFILE_FOLDER_NAME,
                                             headless=False,
                                             browser='edge')
                course = Course(id=a_course_id, name=course_name)
                course.complete_videos()
                a_webdriver.quit()
                print("(tasks_coordinator) The course videos has been marked as completed.")

            # If the user wants to extract the transcript
            if extract_transcript_task:
                heading = f"Extract Transcript: {a_course_id} - {course_name.upper()}"
                print(f"\n\033[45m[{heading:^85}]\033[0m")
                course = Course(id=a_course_id, name=course_name)
                course.extract_transcript()

            # If the user wants to do both tasks
            if both_tasks:
                heading = f"Both Tasks: {a_course_id} - {course_name.upper()}"
                print(f"\n\033[45m[{heading:^85}]\033[0m")
                # TODO: Async
                # Use Edge for a logged in user; Chrome for a non-logged user.
                edge_webdriver = launch_browser(profile_folder=WEBDRIVER_PROFILE_FOLDER_NAME,
                                                headless=False,
                                                browser='edge')
                course = Course(id=a_course_id, name=course_name)
                course.complete_videos()
                course.extract_transcript()
                edge_webdriver.quit()
                print(
                    "(tasks_coordinator) The course videos has been marked as completed and the transcript has been extracted.")

        #  =======================================================================
        # A path is submitted, list all the courses in the path and let user select
        if a_path_id:
            path_data = Path(id=a_path_id)
            path_data.load_json()

            # If the path has no data yet
            # Load it from the web, save it
            # Add its courses to courses collection
            # Print out its courses to the screen and prompting to user
            if not path_data.courses:
                path_data.fetch_data()

                # Save the Path's details into files, JSON and MD
                path_data.save_json()
                path_data.save_markdown()

                # Add courses from this path to the courses collection
                for course in path_data.courses.values():
                    course_id = course['id']
                    course_name = course['name']
                    self.courses_collection.add_item(course_id, course_name)

                # Save the course collection to file.
                self.courses_collection.save_json()

            # List all the courses in the path for the user to select
            path_data.courses_list()

            # TODO: Extract the logic below into a separated method.
            a_course_id = input("\nPLEASE SELECT A COURSE [id or A(ll) (e to exit back, q to quit)]: ")

            if a_course_id.lower() == "a" or a_course_id.lower() == "all":
                if mark_complete_video_task:
                    a_webdriver = launch_browser(profile_folder=WEBDRIVER_PROFILE_FOLDER_NAME,
                                                 headless=False,
                                                 browser='edge')
                    for course in path_data.courses.values():
                        current_course_id: str = course['id']
                        current_course_name: str = course['name']
                        heading = f"Mark Complete Videos: {current_course_id} - {current_course_name.upper()}"
                        print(f"\n\033[45m[{heading:^85}]\033[0m")
                        course_instance = Course(id=current_course_id, name=current_course_name)
                        course_instance.complete_videos()
                        print("(tasks_coordinator) The course videos has been marked as completed.")
                    a_webdriver.quit()

                if extract_transcript_task:
                    for course in path_data.courses.values():
                        current_course_id: str = course['id']
                        current_course_name: str = course['name']

                        heading = f"Extract Transcript: {current_course_id} - {current_course_name.upper()}"
                        print(f"\n\033[45m[{heading:^85}]\033[0m")

                        course_instance = Course(id=current_course_id, name=current_course_name)
                        course_instance.extract_transcript()
                        print("(tasks_coordinator) The transcript has been extracted.\n")

                if both_tasks:
                    for course in path_data.courses.values():
                        current_course_id: str = course['id']
                        current_course_name: str = course['name']

                        heading = f"Both Tasks: {current_course_id} - {current_course_name.upper()}"
                        print(f"\n\033[45m[{heading:^85}]\033[0m")

                        # TODO: Async
                        # Use Edge for a logged in user; Chrome for a non-logged user.
                        edge_webdriver = launch_browser(profile_folder=WEBDRIVER_PROFILE_FOLDER_NAME,
                                                        headless=False,
                                                        browser='edge')
                        course_instance = Course(id=course['id'], name=course['name'])
                        course_instance.complete_videos()
                        course_instance.extract_transcript()
                        edge_webdriver.quit()
                        print(
                            "(tasks_coordinator) The course videos has been marked as completed and the transcript has been extracted.")

            elif a_course_id.isdigit():
                if mark_complete_video_task:

                    heading = f"Mark Complete Videos: {a_course_id} - {path_data.courses[a_course_id]['name'].upper()}"
                    print(f"\n\033[45m[{heading:^85}]\033[0m")

                    a_webdriver = launch_browser(profile_folder=WEBDRIVER_PROFILE_FOLDER_NAME,
                                                 headless=False,
                                                 browser='edge')
                    course_instance = Course(id=a_course_id, name=path_data.courses[a_course_id]['name'])
                    course_instance.complete_videos()
                    a_webdriver.quit()
                    print("(tasks_coordinator) The course videos has been marked as completed.")

                if extract_transcript_task:
                    heading = f"Extract Transcript: {a_course_id} - {path_data.courses[a_course_id]['name'].upper()}"
                    print(f"\n\033[45m[{heading:^85}]\033[0m")

                    course_instance = Course(id=a_course_id, name=path_data.courses[a_course_id]['name'])
                    course_instance.extract_transcript()

                if both_tasks:
                    heading = f"Both Tasks: {a_course_id} - {path_data.courses[a_course_id]['name'].upper()}"
                    print(f"\n\033[45m[{heading:^85}]\033[0m")

                    # TODO: Async
                    # Use Edge for a logged in user; Chrome for a non-logged user.
                    edge_webdriver = launch_browser(profile_folder=WEBDRIVER_PROFILE_FOLDER_NAME,
                                                    headless=False,
                                                    browser='edge')
                    course_instance = Course(id=a_course_id, name=path_data.courses[a_course_id]['name'])
                    course_instance.complete_videos()
                    course_instance.extract_transcript()
                    edge_webdriver.quit()
                    print(
                        "(tasks_coordinator) The course videos has been marked as completed and the transcript has been extracted.")

            elif a_course_id.lower() == "e":
                print("\t[<< Going Back]\n")
                return

            elif a_course_id.lower() == "q":
                print("Got it. Bye.")
                sys.exit(0)

            else:
                print("You need to choose a course id or A(ll) or q to quit the program.")
                return

    # Interactive mode for the CloudSkillsBoost Automation Script
    # TODO: Command-line interface for the CloudSkillsBoost Automation Script
    def interactive_mode(self):
        """
        Interactive mode for the CloudSkillsBoost Automation Script.
        """

        print("\033[34mInitializing the CloudSkillsBoost Automation Script...\033[0m\n")

        running = True
        while running:
            #  ===================================================================
            # Gathers all the courses or path names and prompts the user for selection
            # Allows working with a path, courses, or both options via a user-friendly interface
            course_or_path = input("\033[34m"
                                   "WHAT DO YOU WANT TO WORK WITH?:"
                                   "\033[0m\n"
                                   "\t\t1. c: A Certain Course Only\n"
                                   "\t\t2. p: A Path To Select Course(s)\n"
                                   "\t\t3. l: Show me a list\n"
                                   "\t\t4. q: Quit\n"
                                   "•PLEASE SELECT: ")

            #  ===================================================================
            if course_or_path.lower() == "1" or course_or_path.lower() == "c":
                course_id = input(f"•{'COURSE ID: ':>15}")
                if not course_id.strip().isdigit():
                    print("ERROR: INVALID OR MISSING COURSE ID. "
                          "PLEASE PROVIDE A VALID NUMERIC COURSE ID!")
                    sys.exit(1)

                if self.courses_collection and course_id in self.courses_collection.collection:
                    course_title = self.courses_collection.collection[course_id]
                    print(f"•{'SELECTED: ':>15}\033[45m"
                          f"{course_id}: {course_title}"
                          f"\033[0m\n")

                # Proceed with the certain course only
                self.tasks_coordinator(a_course_id=course_id)

            #  ===================================================================
            elif course_or_path.lower() == "2" or course_or_path.lower() == "p":

                path_id = input(f"•{'PATH ID: ':>15}")
                if not path_id.strip().isdigit():
                    print("\n\033[33m[ERROR: INVALID OR MISSING PATH ID. "
                          "PLEASE PROVIDE A VALID NUMERIC PATH ID!]\033[0m\n")
                    continue

                # Proceed with the certain path and course
                path_title = self.paths_collection.collection.get(path_id)
                if path_title:
                    print(f"•{'SELECTED: ':>15}\033[45m"
                          f"{path_id} - {path_title}"
                          f"\033[0m\n")
                else:
                    self.paths_collection.fetch_paths()
                    self.paths_collection.save_json()
                    path_title = self.paths_collection.collection.get(path_id)
                    if path_title:
                        print(f"•{'SELECTED: ':>15}\033[45m"
                              f"{path_id} - {path_title}"
                              f"\033[0m\n")
                    else:
                        print(f"\n"
                              "\033[33mYOU PROVIDED A WRONG PATH ID, I BELIEVE: {path_id}\n"
                              "PLEASE RETRY WITH THE FOLLOWING LIST OF PATH:\033[0m\n")
                        self.paths_collection.print_list()
                        continue

                self.tasks_coordinator(a_path_id=path_id)

            #  ===================================================================
            elif course_or_path.lower() == "3" or course_or_path.lower() == "l":

                # If a path list is gathered successfully
                self.paths_collection.print_list()
                # Use the hidden menu to fetch path list instead
                # if paths_collection.collection:
                #     # Print out all the paths
                #     paths_collection.print_list()
                # else:
                #     paths_collection.fetch_paths()
                #     # Write the new path list to the file
                #     paths_collection.save_json()

                #     # Prompt user to select a path
                #     paths_collection.print_list()

                # Prompt user to select a path to proceed with
                path_id = input("\033[34m"
                                "\n"
                                "SELECT A PATH ID (q to quit): "
                                "\033[0m")

                if not path_id.strip().isdigit():
                    print("\n\033[33m[ERROR: INVALID OR MISSING PATH ID. "
                          "PLEASE PROVIDE A VALID NUMERIC PATH ID!]\033[0m\n")
                    continue

                # Ensure the user enter a correct path id which is a number
                if path_id.strip().isdigit():
                    path_title = self.paths_collection.collection[path_id]
                    print(f"Entering... \033[45m"
                          f"•--{path_id:>{len(path_id) + 1}}: {path_title.upper()}"
                          f"\033[0m\n")

                    # Proceed with the selected path id
                    self.tasks_coordinator(a_path_id=path_id)

                # User can q at this stage if not wanting to continue
                elif path_id.lower() == "q":
                    print("Bye.")
                    sys.exit(0)

            elif course_or_path.lower() == '4' or course_or_path.lower() == "q":
                print("Ya. Good day.")
                running = False
            
            elif course_or_path.lower() == '5' or course_or_path.lower() == 'g':
                course_id = input(f"•{'COURSE ID: ':>15}")
                if not course_id.strip().isdigit():
                    print("ERROR: INVALID OR MISSING COURSE ID. "
                          "PLEASE PROVIDE A VALID NUMERIC COURSE ID!")
                    sys.exit(1)

                if self.courses_collection and course_id in self.courses_collection.collection:
                    course_title = self.courses_collection.collection[course_id]
                    print(f"•{'SELECTED: ':>15}\033[45m"
                          f"{course_id}: {course_title}"
                          f"\033[0m\n")
                    
                    course = Course(id=course_id, name=course_title)
                    course.generate_prompt()
                    print("Generating prompt completed. Going back...\n")

            elif course_or_path.lower() == '99':
                print(f"\n"
                      "\033[35mDEBUG: RELOADING THE COURSES LIST... in several minutes\033[0m\n")
                # Refresh Paths list
                if self.paths_collection.fetch_paths():
                    print("Paths List refreshed. Proceed with courses of each path.\n")
                    self.paths_collection.save_json()
                    self.paths_collection.write_md()
                else:
                    print("Paths List NOT refreshed. Proceed with courses of each path.\n")

                # Get all courses from all the paths
                for path_id, path_name in self.paths_collection.collection.items():
                    print(f"+|-• \033[35m[{path_id:>5} - {path_name:<72}]\033[0m")
                    path_data = Path(id=path_id, name=path_name)
                    path_data.fetch_data()
                    # Save the path data to the file: JSON
                    path_data.save_json()
                    # Save the path data to the file: MD
                    path_data.save_markdown()
                    # Add courses from this path to the courses collection
                    for course in path_data.courses.values():
                        self.courses_collection.add_item(course['id'], course['name'])
                self.courses_collection.save_json()
                print("\n"
                      "\033[35mDEBUG: COURSES LIST RELOADED.\033[0m\n")

            else:
                print("\033[31m"
                      f"[INVALID CHOICE] {course_or_path}\n"
                      "PLEASE SELECT 1, 2, 3, or q TO QUIT THE PROGRAM."
                      "\033[0m\n")
                continue


if __name__ == "__main__":

    # Create the OUTPUT FOLDERS if they do not exist
    if not PathlibPath(OUTPUT_FOLDER_NAME).exists():
        PathlibPath(OUTPUT_FOLDER_NAME).mkdir(parents=True, exist_ok=True)
    
    # Create the DATA FOLDERS if they do not exist
    if not PathlibPath(DATA_FOLDER_NAME).exists():
        PathlibPath(OUTPUT_FOLDER_NAME).mkdir(parents=True, exist_ok=True)

    # STARTING THE PROGRAM
    # https://talyian.github.io/ansicolors/
    # https://en.wikipedia.org/wiki/ANSI_escape_code
    print()
    print("\033[45m"
          "=================================================================="
          "\033[0m")
    print("                CloudSkillsBoost Automation Script                ")
    print("NOTE:"
          "\n\tDO NOT NEED TO LOGIN TO CLOUDSKILLSBOOST.GOOGLE"
          "\n\tHOWEVER, TO SAVE THE PROGRESS, PLEASE LOGIN.")
    print("\033[45m"
          "=================================================================="
          "\033[0m"
          "\n")

    # Create an instance of CloudSkillsBoost and start interactive mode
    cloud_skills_boost = CloudSkillsBoost()
    cloud_skills_boost.interactive_mode()

    sys.exit(0)

# TODO: Check if published_date is newer then update the path data
# TODO: Separated webdriver in tasks_coordinator()
# TODO: Check for existing course/lab md files.
# TODO: Make the collected data persistent, in another words, the application is stateful.
# TODO: Mark correct quiz(es) answers/options.
# TODO: Enable async to speed up the tasks
# TODO: LLM for transcript formatting, split into multiple semantic paragraphs.
# TODO: Non-login user.
# TODO: Remove <p> <p> <br/> from the transcript/text/description.
