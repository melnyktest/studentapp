class SubjectTransformer:
    subjects = ["mathmatics", "literature", "computer"]

    @staticmethod
    def subject_to_number(subject):
        try:
            return SubjectTransformer.subjects.index(subject)
        except ValueError:
            raise ValueError(f"{subject} is not a valid subject")

    @staticmethod
    def number_to_subject(number):
        try:
            return SubjectTransformer.subjects[number]
        except IndexError:
            raise ValueError(f"{number} is not a valid index")