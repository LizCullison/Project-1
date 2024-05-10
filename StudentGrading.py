from typing import List

class StudentGrader:
    def __init__(self, scores: List[int]):
        self.scores = scores
        
    def grade_students(self):
        num_students = len(self.scores)
        best_scores = sorted(self.scores, reverse=True)
        grades = []
        
        for score in self.scores:
            if score >= (best_scores[0] - 10):
                grades.append('A')
            elif score >= (best_scores[0] - 20):
                grades.append('B')
            elif score >= (best_scores[0] - 30):
                grades.append('C')
            elif score >= (best_scores[0] - 40):
                grades.append('D')
            else:
                grades.append('F')
                
        return grades