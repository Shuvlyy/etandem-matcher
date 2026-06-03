import pandas as pd

from student import Student


class MatchResults:
    def __init__(self, score: int, percentage: float, common_interests: str):
        self.score = score
        self.percentage = percentage
        self.common_interests = common_interests

    def __repr__(self):
        return f"MatchResults(score={self.score}, percentage={self.percentage}, common_interests={self.common_interests})"


class Matcher:
    def __init__(self, internationals: list, locals: list):
        self.internationals = internationals
        self.locals = locals

    def _match(self, student_a: Student, student_b: Student) -> MatchResults:
        """Computes the compatibility score between two students."""
        score = 0
        max_possible = 0

        # age (gap <= 2: +5 pts, <= 4: +2 pts)
        max_possible += 5
        if pd.notna(student_a.age) and pd.notna(student_b.age):
            age_gap = abs(student_a.age - student_b.age)
            if age_gap <= 2:
                score += 5
            elif age_gap <= 4:
                score += 2

        # +5 pts per common interest
        max_possible += len(student_a.interests) * 5
        common_interests = student_a.interests.intersection(student_b.interests)
        score += len(common_interests) * 5

        # +3 pts if same sector
        max_possible += 3
        if student_a.sector.intersection(student_b.sector):
            score += 3

        if max_possible > 0:
            percentage = int((score / max_possible) * 100)
            percentage = min(100, percentage)  # clip
        else:
            percentage = 0

        return MatchResults(
            score=score,
            percentage=percentage,
            common_interests=", ".join(common_interests).title(),
        )

    def get_top_matches(self, top_n: int = 3) -> pd.DataFrame:
        results = []

        for inter_student in self.internationals:
            matches_for_this_student = []

            for local_student in self.locals:
                match_info = self._match(inter_student, local_student)

                matches_for_this_student.append(
                    {
                        "International Student (A)": inter_student.name,
                        "Proposed Match (B)": local_student.name,
                        "Compatibility": f"{match_info.percentage} %",
                        "Raw Score": match_info.score,
                        "Common Interests": match_info.common_interests,
                    }
                )

            # keeping only first top_n matches
            matches_for_this_student.sort(key=lambda x: x["Raw Score"], reverse=True)
            results.extend(matches_for_this_student[:top_n])

        return pd.DataFrame(results)
