import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from config.settings import BASE_URL, BASE_URL_COURSES, BASE_URL_LAB, BASE_URL_PATHS
from models.course import Course
from models.lab import Lab
from models.path import Path
from models.collection import Collection
from pathlib import Path as PathLib

app = Flask(__name__)

# Initialize collections
paths_collection = Collection(type='paths', name='Paths Collection')
courses_collection = Collection(type='courses', name='Courses Collection')
labs_collection = Collection(type='labs', name='Labs Collection')

# Load data into collections
paths_collection.load_json()
courses_collection.load_json()
labs_collection.load_json()

topics = set()
topics_to_courses = {}

@app.context_processor
def inject_global_data():
    """
    Inject global data into all templates.
    """

    return {
        'labs': labs_collection.collection,
        'courses': courses_collection.collection,
        'paths': paths_collection.collection,
        'topics': topics,
        'BASE_URL_LAB': BASE_URL_LAB,
        'BASE_URL_COURSES': BASE_URL_COURSES,
        'BASE_URL_PATHS': BASE_URL_PATHS,
        'BASE_URL': BASE_URL
    }

@app.route('/')
def home():
    """
    Home page for the Cloud Skills Boost Helper.
    """

    return render_template(
        'index.html'
    )


@app.route('/course/<course_id>')
def course_details(course_id):
    """
    Display details of a specific course.
    """
    course = courses_collection.collection.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    return render_template(
        'course.html',
        course=course
    )


@app.route('/path/<path_id>')
def path_details(path_id):
    """
    Display details of a specific path.
    """
    path = paths_collection.collection.get(path_id)
    if not path:
        return jsonify({"error": "Path not found"}), 404

    # Load path data
    path_data = Path(id=path_id)
    path_data.load_json()

    return render_template(
        'path.html',
        path=path_data
    )


@app.route('/labs/<lab_id>')
def lab_details(lab_id):
    # Logic to fetch and display lab details
    lab = labs_collection.collection.get(lab_id)
    if not lab:
        return jsonify({"error": "Lab not found"}), 404
    # Load lab data
    lab_data = Lab(id=lab_id)
    lab_data.load_json()
    return render_template(
        'lab.html',
        lab=lab_data,
    )


@app.route('/course/<course_id>/complete_videos', methods=['POST'])
def complete_videos(course_id):
    """
    Mark videos in a course as completed.
    """
    course = Course(id=course_id)
    course.complete_videos()
    return jsonify({"message": f"Videos for course {course_id} marked as completed."})


@app.route('/course/<course_id>/extract_transcript', methods=['POST'])
def extract_transcript(course_id):
    """
    Extract the transcript for a course.
    """
    course = Course(id=course_id)
    course.extract_transcript()
    return jsonify({"message": f"Transcript for course {course_id} extracted."})


@app.route('/path/<path_id>/process', methods=['POST'])
def process_path(path_id):
    """
    Process all courses in a path (mark videos as completed and/or extract transcripts).
    """
    action = request.form.get('action')  # 'complete_videos', 'extract_transcripts', or 'both'
    path_data = Path(id=path_id)
    path_data.load_json()

    for course in path_data.courses.values():
        course_instance = Course(id=course['id'], name=course['name'])
        if action == 'complete_videos':
            course_instance.complete_videos()
        elif action == 'extract_transcripts':
            course_instance.extract_transcript()
        elif action == 'both':
            course_instance.complete_videos()
            course_instance.extract_transcript()

    return jsonify({"message": f"Processed all courses in path {path_id} with action: {action}."})

@app.route('/browse/topic/<topic>')
def browse_by_topic(topic):
    """
    filtered_courses = topics_to_courses.get(topic, [])

    This route filters and displays courses associated with the given topic.
    """
    # Filter courses, paths, and labs by the selected topic
    filtered_courses = topics_to_courses.get(topic, {})

    return render_template(
        'browse_by_topic.html',
        courses=filtered_courses
    )


def extract_unique_topics(courses_collection):
    """
    Gather all unique topics from the downloaded courses in the 'data/courses/' folder.

    :param courses_collection: The collection of courses.
    :return: A sorted list of unique topics.
    """

    topics_set = set()  # Use a set to avoid duplicate topics
    topics_to_courses = {}  # Dictionary to map topics to courses
    courses_folder = PathLib("data/courses")  # Path to the courses folder

    if not isinstance(courses_collection.collection, dict):
        raise TypeError("courses_collection.collection must be a dictionary")

    for course_id, course_name in courses_collection.collection.items():  # Updated to use items()
        course_file = courses_folder / f"{course_id}.json"  # Construct the file path

        if course_file.exists():  # Check if the course JSON file exists
            course = Course(id=course_id)  # Create a new Course instance
            course.load_json()  # Load the JSON file
            topics = course.topics  # Extract the 'topics' key
            topics_set.update(topics)  # Add topics to the set
            for topic in topics:
                # Ensure the topic is a string
                if not isinstance(topic, str):
                    raise ValueError(f"Topic '{topic}' is not a string")
                # Map topic to course name
                if topic not in topics_to_courses:
                    topics_to_courses[topic] = {}
                topics_to_courses[topic][course_id] = course_name  # Map topic to course name directly
        else:
            # Skip if the file does not exist
            continue
    # Sort the topics set to get a consistent order
    return sorted(topics_set), topics_to_courses  # Return a sorted list of unique topics


if __name__ == '__main__':
    topics, topics_to_courses = extract_unique_topics(courses_collection)
    app.run(host='0.0.0.0', port=8080, debug=True)

# Note:
# The above code assumes the existence of models for Course, Path, and Collection.
# The models should handle the logic for loading data from JSON files and processing courses.
# The templates (index.html, course.html, path.html) should be created to render the respective pages.
# The application should be run in an environment where Flask is installed.
# To run the application, save this code in a file named application.py and run:
# python application.py
# Ensure you have Flask installed in your Python environment.
# You can install Flask using pip:
# pip install Flask
# The application will be accessible at http://localhost:8080
# Ensure you have the required JSON files in the same directory as this script.
# The JSON files should contain the data for paths, courses, and labs.
# The structure of the JSON files should match the expected format for the models.
# The application can be extended with more features as needed.
# This code is a basic structure for a Flask web application that manages courses and paths.
# The application can be further improved with error handling, logging, and user authentication.
# The application can be deployed on a web server for production use.
# The application can be containerized using Docker for easier deployment and scaling.
# The application can be integrated with a database for persistent storage.
# The application can be tested using unit tests and integration tests.
# The application can be monitored using tools like Prometheus and Grafana.
# The application can be secured using HTTPS and authentication mechanisms.
# The application can be documented using tools like Swagger or OpenAPI.
# The application can be versioned using Git for source control.
# The application can be packaged using tools like PyInstaller for distribution.
# The application can be improved with a better user interface using frontend frameworks like React or Vue.js.
# The application can be optimized for performance using caching mechanisms.
# The application can be made responsive for better usability on mobile devices.
# The application can be localized for different languages and regions.
# The application can be integrated with third-party APIs for additional functionality.
# The application can be extended with user profiles and progress tracking.
# The application can be enhanced with notifications and alerts for users.
# The application can be improved with search functionality for courses and paths.
# The application can be extended with user feedback and ratings for courses.
# The application can be improved with a recommendation system for courses and paths.
# The application can be extended with social sharing features for courses and paths.
# The application can be improved with analytics and reporting features.
# The application can be extended with gamification features for user engagement.
# The application can be improved with accessibility features for users with disabilities.
# The application can be extended with a blog or news section for updates and announcements.
# The application can be improved with a help center or FAQ section for user support.
# The application can be extended with a community forum for user discussions.
# The application can be improved with a contact form for user inquiries.
# The application can be extended with a newsletter subscription feature for updates.
