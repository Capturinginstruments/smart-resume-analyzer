import os
from django import forms
from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.jpg', '.jpeg', '.png']
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

class ResumeUploadForm(forms.Form):
    resume_file = forms.FileField(
        label="Upload Resume",
        widget=forms.FileInput(attrs={
            'id': 'resumeInput',
            'accept': '.pdf,.docx,.doc,.jpg,.jpeg,.png',
            'class': 'file-input-hidden'
        })
    )

    def clean_resume_file(self):
        file = self.cleaned_data.get('resume_file')
        if not file:
            raise ValidationError("Please select a valid file.")

        # Validate file size
        if file.size > MAX_FILE_SIZE:
            size_mb = round(file.size / (1024 * 1024), 2)
            raise ValidationError(f"File size ({size_mb} MB) exceeds the 5 MB limit. Please upload a smaller file.")

        if file.size == 0:
            raise ValidationError("The uploaded file is empty. Please upload a valid resume.")

        # Validate file extension
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValidationError(f"Unsupported file format '{ext}'. Allowed formats: PDF, DOCX, JPG, JPEG, PNG.")

        return file
