import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .models import ResumeAnalysis
from .forms import ResumeUploadForm
from .services.extractor import get_extractor
from .services.analyzer import Resume, ResumeAnalyzer
from .services.scorer import ResumeScorer


def dashboard_view(request):
    """Page 1: Dashboard / Home View"""
    return render(request, 'analyzer/dashboard.html')


def upload_view(request):
    """Page 2: Upload Resume View handling file submission & analysis workflow"""
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['resume_file']
            
            # Save file to media directory temporarily
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp'))
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)
            file_size_kb = round(uploaded_file.size / 1024, 1)
            ext = os.path.splitext(uploaded_file.name)[1].lower().replace('.', '').upper()
            
            extracted_text = ""
            try:
                extractor = get_extractor(file_path)
                extracted_text = extractor.extract_text(file_path)
            except Exception as e:
                print(f"Extraction error: {e}")
                extracted_text = ""
            finally:
                # Remove temporary file after reading
                if os.path.exists(file_path):
                    os.remove(file_path)

            # Check if text was successfully extracted
            if not extracted_text or len(extracted_text.strip()) < 10:
                messages.error(request, "Unable to read this resume. Please upload a clearer file or a non-empty document.")
                return render(request, 'analyzer/upload.html', {'form': form})

            try:
                # Run Analysis Workflow: Resume -> ResumeAnalyzer -> ResumeScorer
                resume_obj = Resume(
                    raw_text=extracted_text,
                    filename=uploaded_file.name,
                    file_type=ext,
                    file_size_kb=file_size_kb
                )
                
                analyzer = ResumeAnalyzer(resume_obj)
                analysis_data = analyzer.analyze()
                
                scorer = ResumeScorer(analysis_data)
                score_results = scorer.calculate_final_score()

                # Save Analysis to SQLite Database
                analysis_record = ResumeAnalysis.objects.create(
                    filename=uploaded_file.name,
                    file_type=ext,
                    file_size_kb=file_size_kb,
                    word_count=resume_obj.word_count,
                    score=score_results['total_score'],
                    status_label=score_results['status_label'],
                    career_field=analysis_data['career_field'],
                    skills=analysis_data['skills'],
                    sections_found=analysis_data['sections'],
                    missing_sections=score_results['missing_sections'],
                    strengths=score_results['strengths'],
                    suggestions=score_results['suggestions'],
                    score_breakdown=score_results['breakdown'],
                    raw_text=extracted_text[:1000] # snippet
                )

                return redirect('result', pk=analysis_record.pk)

            except Exception as e:
                messages.error(request, f"An error occurred during analysis: {str(e)}")
                return render(request, 'analyzer/upload.html', {'form': form})

    else:
        form = ResumeUploadForm()

    return render(request, 'analyzer/upload.html', {'form': form})


def result_view(request, pk):
    """Page 3: Analysis Result View displaying score, progress bars, skills & recommendations"""
    analysis = get_object_or_404(ResumeAnalysis, pk=pk)

    # Compute section count & keywords count for Quick Snapshot
    sections_count = sum(1 for found in analysis.sections_found.values() if found)
    keywords_count = len(analysis.skills) + 5  # Estimated keyword signals

    context = {
        'analysis': analysis,
        'sections_count': sections_count,
        'keywords_count': keywords_count,
    }
    return render(request, 'analyzer/result.html', context)


def history_view(request):
    """Page 4: History View displaying past resume analyses stored in SQLite"""
    history_records = ResumeAnalysis.objects.all()
    return render(request, 'analyzer/history.html', {'history_records': history_records})


def about_view(request):
    """Page 5: About View displaying project architecture & Python concepts used"""
    return render(request, 'analyzer/about.html')


def download_report_view(request, pk):
    """Downloadable formatted text summary report for a resume analysis"""
    analysis = get_object_or_404(ResumeAnalysis, pk=pk)
    
    breakdown = analysis.score_breakdown or {}
    skills_list = ", ".join(analysis.skills) if analysis.skills else "None detected"
    missing_list = ", ".join(analysis.missing_sections) if analysis.missing_sections else "None"
    
    strengths_text = "\n".join([f"  • {s}" for s in analysis.strengths]) if analysis.strengths else "  • Clean formatting"
    suggestions_text = "\n".join([f"  • {s}" for s in analysis.suggestions]) if analysis.suggestions else "  • Resume looks great!"

    report_content = f"""====================================================
SMART RESUME ANALYZER - ANALYSIS REPORT
====================================================

File Name:       {analysis.filename}
File Type:       {analysis.file_type}
Date Analyzed:   {analysis.date.strftime('%B %d, %Y - %H:%M')}
Career Field:    {analysis.career_field}

----------------------------------------------------
OVERALL SCORE: {analysis.score} / 100 ({analysis.status_label})
----------------------------------------------------

SCORE BREAKDOWN:
  - Structure:       {breakdown.get('structure', 0)} / 20
  - Skills:          {breakdown.get('skills', 0)} / 20
  - Experience:      {breakdown.get('experience', 0)} / 20
  - Action Words:    {breakdown.get('action_words', 0)} / 10
  - Contact Info:    {breakdown.get('contact', 0)} / 10
  - Keywords:        {breakdown.get('keywords', 0)} / 10
  - Formatting:      {breakdown.get('formatting', 0)} / 10

QUICK METRICS:
  - Word Count:      {analysis.word_count}
  - Skills Found:    {len(analysis.skills)}

DETECTED SKILLS:
  {skills_list}

MISSING SECTIONS:
  {missing_list}

KEY STRENGTHS:
{strengths_text}

RECOMMENDED IMPROVEMENTS:
{suggestions_text}

====================================================
Generated by Smart Resume Analyzer (Django Academic Project)
====================================================
"""
    response = HttpResponse(report_content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="Resume_Report_{analysis.pk}.txt"'
    return response
