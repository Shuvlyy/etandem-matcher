import pandas as pd

from student import Student, level_dict


class MatchResults:
    def __init__(
        self,
        score: int,
        percentage: float,
        common_interests: str,
        language_levels: tuple[str, str],
    ):
        self.score = score
        self.percentage = percentage
        self.common_interests = common_interests
        self.language_levels = language_levels


class Matcher:
    def __init__(self, internationals: list[Student], locals: list[Student]):
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

        max_possible += 5
        level_sum = level_dict.get(student_a.target_language_level, 2) + level_dict.get(
            student_b.target_language_level, 2
        )
        BALANCED_SUM = 7
        diff_from_ideal = abs(level_sum - BALANCED_SUM)

        if diff_from_ideal == 0:
            score += 5
        elif diff_from_ideal == 1:
            score += 3
        elif diff_from_ideal == 2:
            score += 1
        # if diff >= 3 (like 2 beginners or 2 experts) no points

        if max_possible > 0:
            percentage = int((score / max_possible) * 100)
            percentage = min(100, percentage)  # clip
        else:
            percentage = 0

        return MatchResults(
            score=score,
            percentage=percentage,
            common_interests=", ".join(common_interests).title(),
            language_levels=(
                student_a.target_language_level,
                student_b.target_language_level,
            ),
        )

    def get_top_matches(self, top_n: int = 3) -> pd.DataFrame:
        results = []

        for inter_student in self.internationals:
            matches_for_this_student = []

            for local_student in self.locals:
                match_info = self._match(inter_student, local_student)

                matches_for_this_student.append(
                    {
                        "International Student (A)": f"{inter_student.surname} {inter_student.name}",
                        "Proposed Match (B)": f"{local_student.surname} {local_student.name}",
                        "Email (A)": inter_student.email,
                        "Email (B)": local_student.email,
                        "Compatibility": f"{match_info.percentage}%",
                        "Common Interests": match_info.common_interests,
                        "Language Level (A)": match_info.language_levels[0],
                        "Language Level (B)": match_info.language_levels[1],
                    }
                )

            # keeping only first top_n matches
            matches_for_this_student.sort(
                key=lambda x: int(x["Compatibility"].replace("%", "")), reverse=True
            )
            results.extend(matches_for_this_student[:top_n])

        return pd.DataFrame(results)
