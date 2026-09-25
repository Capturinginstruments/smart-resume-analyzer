class ResumeScorer:
    """
    Implements the 7 sub-scoring functions specified for the mini-project:
    1. calculate_structure_score()   [max 20]
    2. calculate_skill_score()       [max 20]
    3. calculate_experience_score()  [max 20]
    4. calculate_action_score()      [max 10]
    5. calculate_contact_score()     [max 10]
    6. calculate_keyword_score()     [max 10]
    7. calculate_formatting_score()  [max 10]
    Total = 100
    """

    def __init__(self, analysis_data: dict):
        self.contact = analysis_data['contact']
        self.sections = analysis_data['sections']
        self.skills = analysis_data['skills']
        self.action_words = analysis_data['action_words']
        self.career_field = analysis_data['career_field']
        self.word_count = analysis_data['word_count']

    def calculate_structure_score(self) -> int:
        """Calculates structure score based on presence of standard resume sections."""
        score = 0
        if self.sections.get('Contact Information'): score += 4
        if self.sections.get('Education'): score += 4
        if self.sections.get('Skills'): score += 4
        if self.sections.get('Projects'): score += 3
        if self.sections.get('Experience'): score += 3
        if self.sections.get('Certifications'): score += 2
        return min(score, 20)

    def calculate_skill_score(self) -> int:
        """Calculates skill score based on detected technical skills count."""
        count = len(self.skills)
        if count >= 7: return 20
        elif count >= 5: return 17
        elif count >= 3: return 13
        elif count >= 1: return 8
        return 0

    def calculate_experience_score(self) -> int:
        """Calculates projects & experience section score."""
        score = 0
        if self.sections.get('Projects'): score += 10
        if self.sections.get('Experience'): score += 10
        return min(score, 20)

    def calculate_action_score(self) -> int:
        """Calculates action words score based on strong action verbs used."""
        count = self.action_words.get('count', 0)
        if count >= 6: return 10
        elif count >= 4: return 8
        elif count >= 2: return 5
        elif count >= 1: return 3
        return 0

    def calculate_contact_score(self) -> int:
        """Calculates contact info score (Email, Phone, LinkedIn, GitHub)."""
        score = 0
        if self.contact.get('email'): score += 3
        if self.contact.get('phone'): score += 3
        if self.contact.get('has_linkedin'): score += 2
        if self.contact.get('has_github'): score += 2
        return min(score, 10)

    def calculate_keyword_score(self) -> int:
        """Calculates keyword score based on skills and career relevance."""
        if len(self.skills) >= 5 and self.career_field != 'Other':
            return 10
        elif len(self.skills) >= 3:
            return 8
        elif len(self.skills) >= 1:
            return 6
        return 4

    def calculate_formatting_score(self) -> int:
        """Calculates formatting & length score based on word count."""
        if 350 <= self.word_count <= 1000:
            return 10
        elif 200 <= self.word_count < 350:
            return 8
        elif 100 <= self.word_count < 200:
            return 6
        elif self.word_count > 1000:
            return 7
        return 4

    def calculate_final_score(self) -> dict:
        """Computes all sub-scores, final aggregate score, strengths, and suggestions."""
        structure = self.calculate_structure_score()
        skills = self.calculate_skill_score()
        experience = self.calculate_experience_score()
        action = self.calculate_action_score()
        contact = self.calculate_contact_score()
        keyword = self.calculate_keyword_score()
        formatting = self.calculate_formatting_score()

        total = structure + skills + experience + action + contact + keyword + formatting
        total = max(0, min(total, 100))

        if total >= 80:
            status = "Good Resume"
            summary_msg = "Your resume has a solid foundation. A few focused improvements can make it even stronger."
        elif total >= 60:
            status = "Average Resume"
            summary_msg = "Your resume covers the basics well, but adding missing sections and skills will elevate it."
        else:
            status = "Needs Improvement"
            summary_msg = "Your resume is missing key sections or skills. Follow the suggestions below to fix it."

        # Compute Strengths
        strengths = []
        if len(self.skills) >= 3:
            strengths.append("Good technical skills included")
        if self.sections.get('Projects'):
            strengths.append("Projects section included")
        if self.contact.get('email') and self.contact.get('phone'):
            strengths.append("Complete contact information available")
        if self.action_words.get('count', 0) >= 3:
            strengths.append("Strong action verbs used in descriptions")
        if self.sections.get('Education'):
            strengths.append("Clear education section")
        if not strengths:
            strengths.append("Clean file structure detected")

        # Compute Suggestions
        suggestions = []
        if not self.sections.get('Certifications'):
            suggestions.append("Add certifications or course completion details")
        if not self.contact.get('has_linkedin'):
            suggestions.append("Add your LinkedIn profile link")
        if not self.contact.get('has_github'):
            suggestions.append("Add your GitHub profile link")
        if self.action_words.get('count', 0) < 3:
            suggestions.append("Use more professional action words (e.g., Developed, Designed, Optimized)")
        if not self.sections.get('Experience') and not self.sections.get('Projects'):
            suggestions.append("Add measurable project results and work experience")
        if len(self.skills) < 4:
            suggestions.append("List more technical skills and frameworks you are familiar with")
        if self.word_count < 250:
            suggestions.append("Expand your resume text to provide more detail on projects and achievements")

        # Missing sections
        missing_sections = [sec for sec, found in self.sections.items() if not found]

        return {
            'total_score': total,
            'status_label': status,
            'summary_msg': summary_msg,
            'breakdown': {
                'structure': structure,
                'skills': skills,
                'experience': experience,
                'action_words': action,
                'contact': contact,
                'keywords': keyword,
                'formatting': formatting,
            },
            'strengths': strengths,
            'suggestions': suggestions,
            'missing_sections': missing_sections,
        }
