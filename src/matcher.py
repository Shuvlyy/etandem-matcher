import numpy as np
import pandas as pd

from student import Student


class Matcher:
    def __init__(self, internationals: list, locals: list):
        self.internationals = internationals
        self.locals = locals
        self.score = np.zeros((len(internationals), len(locals)))

    def _calculate_score(self, student_a: Student, student_b: Student) -> int:
        """Computes the compatibility score between two students."""
        score = 0

        # age (gap <= 2: +5 pts, <= 4: +2 pts)
        if pd.notna(student_a.age) and pd.notna(student_b.age):
            age_gap = abs(student_a.age - student_b.age)
            if age_gap <= 2:
                score += 5
            elif age_gap <= 4:
                score += 2

        # +5 pts per common interest
        common_interests = student_a.interests.intersection(student_b.interests)
        score += len(common_interests) * 5

        # +3 pts if same filiere
        if student_a.sector.intersection(student_b.sector):
            score += 3

        return score

    def build_score_matrix(self):
        """Fills the score matrix by comparing each student."""
        for i, inter_student in enumerate(self.internationals):
            for j, local_student in enumerate(self.locals):
                self.score[i][j] = self._calculate_score(inter_student, local_student)

        return self.score
