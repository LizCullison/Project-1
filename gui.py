import csv
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QSizePolicy, QSpacerItem
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from StudentGrading import StudentGrader

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Grading')
        self.setFixedSize(350, 350)  # Adjusted size
        
        # Labels
        self.student_label = QLabel('Student Name:')
        self.attempts_label = QLabel('No. of Attempts:')
        self.score_labels = [QLabel(f'Score {i+1}:') for i in range(4)]
        
        # Inputs
        self.student_input = QLineEdit()
        self.attempts_input = QLineEdit()
        self.score_inputs = [QLineEdit() for _ in range(4)]  # Pre-generate 4 score input boxes
        for score_input in self.score_inputs:
            score_input.hide()  # Initially hide all score input boxes
        
        # Hide score labels
        for score_label in self.score_labels:
            score_label.hide()
            
        # Button
        self.submit_button = QPushButton('Submit')
        self.submit_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)  # Constrain size
        
        # Error Label
        self.error_label = QLabel()
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setStyleSheet("color: red;")
        
        # Layout
        layout = QVBoxLayout()
        
        # Add Student Name widgets to the layout
        student_layout = QHBoxLayout()
        student_layout.addWidget(self.student_label)
        student_layout.addWidget(self.student_input)
        layout.addLayout(student_layout)
        
        # Add Number of Attempts widgets to the layout
        attempts_layout = QHBoxLayout()
        attempts_layout.addWidget(self.attempts_label)
        attempts_layout.addWidget(self.attempts_input)
        layout.addLayout(attempts_layout)
        
        # Add score input boxes to the layout
        for score_label, score_input in zip(self.score_labels, self.score_inputs):
            score_layout = QHBoxLayout()
            score_layout.addWidget(score_label)
            score_layout.addWidget(score_input)
            layout.addLayout(score_layout)
        
        # Add spacer to push submit button to the bottom
        layout.addStretch()
        
        # Add Submit button
        submit_layout = QHBoxLayout()
        submit_layout.addStretch(1)  
        submit_layout.addWidget(self.submit_button)
        submit_layout.addStretch(1)  
        layout.addLayout(submit_layout)
        
        layout.addWidget(QLabel())  # Empty label for one line of whitespace
        layout.addWidget(self.error_label)
        
        self.setLayout(layout)
        
        self.submit_button.clicked.connect(self.submit_data)
        self.attempts_input.returnPressed.connect(self.generate_score_inputs)
    
    def generate_score_inputs(self):
        attempts_text = self.attempts_input.text()
        if not attempts_text.isdigit() or not (1 <= int(attempts_text) <= 4):
            self.error_label.setText('Error: Attempts must be between 1 and 4.')
            return
        attempts = int(attempts_text)
        
        # Hide all score input boxes
        for score_label, score_input in zip(self.score_labels, self.score_inputs):
            score_label.hide()
            score_input.hide()
        
        # Show score input boxes up to the number of attempts
        for i in range(attempts):
            self.score_labels[i].show()
            self.score_inputs[i].show()

    def submit_data(self):
        student_name = self.student_input.text()
        attempts_text = self.attempts_input.text()

        #Validate student name
        if (not student_name) or (student_name.isdigit()):
            self.error_label.setStyleSheet('color: red;')
            self.error_label.setText('Error: Enter a name')
            return

        # Validate attempts input
        if not attempts_text.isdigit() or not (1 <= int(attempts_text) <= 4):
            self.error_label.setText('Error: Attempts must be between 1 and 4.')
            return
        
        # Generate score inputs
        self.generate_score_inputs()  

        attempts = int(attempts_text)

        #Get scores
        scores = []
        for score_input in self.score_inputs:
            score_text = score_input.text()
            score = int(score_text) if score_text.isdigit() else 0
            scores.append(score)
        
        #Calculate final score
        final_score = max(scores)
        
        #Write to CSV
        with open('student_grades.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            if csvfile.tell() == 0:
                writer.writerow(['Name', 'Score 1', 'Score 2', 'Score 3', 'Score 4', 'Final'])
                
            writer.writerow([student_name] + scores + [final_score])
            
        #Show submission message
        self.error_label.setStyleSheet('color: red;')
        self.error_label.setText('Submitted')
        
        #Clear inputs
        self.student_input.clear()
        self.attempts_input.clear()
        for input_ in self.score_inputs:
            input_.clear()

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec())
