from django.db import models

class ResumeAnalysis(models.Model):
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    file_size_kb = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)
    word_count = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    status_label = models.CharField(max_length=50, default='Average')
    career_field = models.CharField(max_length=100, default='Software Engineering')
    
    # Analysis details stored as JSON fields
    skills = models.JSONField(default=list)
    sections_found = models.JSONField(default=dict)
    missing_sections = models.JSONField(default=list)
    strengths = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)
    score_breakdown = models.JSONField(default=dict)
    
    # Metadata
    raw_text = models.TextField(blank=True, default='')

    @property
    def breakdown_pct(self):
        """Returns percentage values for the 7 breakdown progress bars."""
        b = self.score_breakdown or {}
        return {
            'structure': round((b.get('structure', 0) / 20) * 100),
            'skills': round((b.get('skills', 0) / 20) * 100),
            'experience': round((b.get('experience', 0) / 20) * 100),
            'action_words': round((b.get('action_words', 0) / 10) * 100),
            'contact': round((b.get('contact', 0) / 10) * 100),
            'keywords': round((b.get('keywords', 0) / 10) * 100),
            'formatting': round((b.get('formatting', 0) / 10) * 100),
        }

    def __str__(self):
        return f"{self.filename} ({self.score}/100) - {self.date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-date']
