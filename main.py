from models.collection import Collection
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

