import re

class Resume:
    """Data container object representing an uploaded resume."""
    def __init__(self, raw_text: str, filename: str, file_type: str, file_size_kb: float = 0.0):
        self.raw_text = raw_text or ""
        self.clean_text = self.raw_text.lower()
        self.filename = filename
        self.file_type = file_type
        self.file_size_kb = file_size_kb
        # Count words using simple python split
        words = re.findall(r'\w+', self.raw_text)
        self.word_count = len(words)


class ResumeAnalyzer:
    """Core domain class for analyzing resume text using Regular Expressions and simple Python logic."""

    COMMON_SKILLS = [
        'Python', 'Java', 'C', 'C++', 'JavaScript', 'HTML', 'CSS', 
        'Django', 'React', 'SQL', 'MySQL', 'MongoDB', 'Git', 'GitHub', 
        'AWS', 'Machine Learning', 'Docker', 'Linux', 'Node.js', 'REST API',
        'TypeScript', 'PHP', 'Flutter', 'Android'
    ]

    ACTION_WORDS = [
        'developed', 'designed', 'created', 'implemented', 'built', 
        'managed', 'analyzed', 'tested', 'improved', 'optimized', 
        'engineered', 'spearheaded', 'led', 'established', 'automated', 
        'configured', 'maintained', 'deployed', 'orchestrated'
    ]

    def __init__(self, resume: Resume):
        self.resume = resume

    def detect_contact_info(self) -> dict:
        """Uses Regular Expressions (re) to extract Email, Phone, LinkedIn, and GitHub."""
        text = self.resume.raw_text

        # Email regex pattern
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        email = email_match.group(0) if email_match else None

        # Phone regex pattern (various formats)
        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        phone = phone_match.group(0) if phone_match else None

        # LinkedIn link or handle
        linkedin_match = re.search(r'(linkedin\.com/in/[\w-]+|linkedin)', text, re.I)
        has_linkedin = bool(linkedin_match)

        # GitHub link or handle
        github_match = re.search(r'(github\.com/[\w-]+|github)', text, re.I)
        has_github = bool(github_match)

        return {
            'email': email,
            'phone': phone,
            'has_linkedin': has_linkedin,
            'has_github': has_github
        }

    def detect_sections(self) -> dict:
        """Detects presence of key resume sections."""
        clean = self.resume.clean_text
        contact_info = self.detect_contact_info()

        sections = {
            'Contact Information': bool(contact_info['email'] or contact_info['phone']),
            'Education': bool(re.search(r'\b(education|academic|qualification|degree|b\.tech|btech|bachelor|university|college|gpa|cgpa)\b', clean)),
            'Skills': bool(re.search(r'\b(skill|skills|technical skills|technologies|competencies|expertise)\b', clean)),
            'Projects': bool(re.search(r'\b(project|projects|key projects|academic projects|personal projects)\b', clean)),
            'Experience': bool(re.search(r'\b(experience|work experience|internship|employment|history|work history)\b', clean)),
            'Certifications': bool(re.search(r'\b(certification|certifications|certificates|courses|certified)\b', clean)),
            'LinkedIn': contact_info['has_linkedin'],
            'GitHub': contact_info['has_github'],
        }
        return sections

    def detect_skills(self) -> list:
        """Identifies skills present in the resume text."""
        detected = []
        clean = self.resume.clean_text

        for skill in self.COMMON_SKILLS:
            # Special regex escaping for skills like C++, C#, REST API
            pattern = r'\b' + re.escape(skill) + r'\b'
            if skill == 'C++':
                pattern = r'c\+\+'
            elif skill == 'C':
                pattern = r'\bc\b'

            if re.search(pattern, clean, re.IGNORECASE):
                detected.append(skill)

        return detected

    def count_action_words(self) -> dict:
        """Counts total action words and list unique action words found."""
        clean = self.resume.clean_text
        found_words = []

        for word in self.ACTION_WORDS:
            matches = re.findall(r'\b' + re.escape(word) + r'\b', clean, re.IGNORECASE)
            if matches:
                found_words.extend(matches)

        return {
            'count': len(found_words),
            'unique_words': list(set(found_words))
        }

    def detect_career_field(self) -> str:
        """Determines career field based on keyword frequency."""
        clean = self.resume.clean_text

        field_keywords = {
            'Web Development': ['html', 'css', 'javascript', 'react', 'web', 'frontend', 'backend', 'full stack', 'django', 'node'],
            'Data Science': ['data science', 'pandas', 'numpy', 'scikit', 'machine learning', 'analytics', 'statistic', 'data analyst'],
            'AI/ML': ['machine learning', 'deep learning', 'artificial intelligence', 'neural network', 'nlp', 'pytorch', 'tensorflow'],
            'Cybersecurity': ['security', 'cybersecurity', 'penetration', 'firewall', 'network', 'vulnerability', 'cryptography'],
            'Cloud Computing': ['aws', 'cloud', 'azure', 'gcp', 'devops', 'docker', 'kubernetes'],
            'Software Engineering': ['software', 'developer', 'python', 'java', 'c++', 'git', 'system', 'algorithm', 'data structure', 'oop'],
        }

        scores = {field: 0 for field in field_keywords}

        for field, keywords in field_keywords.items():
            for kw in keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', clean, re.IGNORECASE):
                    scores[field] += 1

        best_field = max(scores, key=scores.get)
        if scores[best_field] == 0:
            return 'Software Engineering'
        return best_field

    def analyze(self) -> dict:
        """Aggregates all analysis findings."""
        contact = self.detect_contact_info()
        sections = self.detect_sections()
        skills = self.detect_skills()
        action_data = self.count_action_words()
        career_field = self.detect_career_field()

        return {
            'contact': contact,
            'sections': sections,
            'skills': skills,
            'action_words': action_data,
            'career_field': career_field,
            'word_count': self.resume.word_count,
        }
