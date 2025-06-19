from flask import Blueprint, render_template, request, redirect, url_for, send_file, session, flash
import os
from .utils import file_parser, nlp_processor, scoring, report_generator
from config import Config
import uuid
import pandas as pd
from io import BytesIO 

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_desc = request.form['job_desc']
        resume_files = request.files.getlist('resumes')
        
        if not job_desc or not resume_files:
            flash('Please provide a job description and at least one resume.', 'error')
            return redirect(url_for('main.index'))

        session_id = str(uuid.uuid4())
        session['session_id'] = session_id

        # Save job description to file
        job_desc_path = os.path.join(Config.JOB_DESCRIPTION_FOLDER, f"{session_id}.txt")
        with open(job_desc_path, 'w') as f:
            f.write(job_desc)

        resume_data = []
        for file in resume_files:
            if file.filename == '':
                continue

            filename = file.filename
            file_path = os.path.join(Config.UPLOAD_FOLDER, f"{session_id}_{filename}")
            file.save(file_path)

            text = file_parser.extract_text(file_path)
            contact_info = file_parser.extract_contact_info(text)
            skills = nlp_processor.extract_skills(text)
            experience = nlp_processor.extract_experience(text)

            resume_data.append({
                'path': file_path,
                'text': text,
                'name': filename,
                'contact': contact_info,
                'skills': list(skills),  # Ensure JSON-serializable
                'experience': experience
            })

        preprocessed_job_desc = nlp_processor.preprocess_text(job_desc)
        preprocessed_resumes = [nlp_processor.preprocess_text(r['text']) for r in resume_data]

        scores = scoring.calculate_scores(preprocessed_job_desc, preprocessed_resumes, resume_data)

        for i, resume in enumerate(resume_data):
            resume['score'] = scores[i]
            resume['rank'] = i + 1

        ranked_resumes = sorted(resume_data, key=lambda x: x['score'], reverse=True)

        job_skills = set(nlp_processor.extract_skills(job_desc))
        for resume in ranked_resumes:
            resume['skill_gaps'] = list(job_skills - set(resume['skills']))  # Safely serializable

        session['rankings'] = ranked_resumes
        session['job_desc'] = job_desc

        return redirect(url_for('main.results'))

    return render_template('index.html')


@bp.route('/results')
def results():
    rankings = session.get('rankings', [])
    job_desc = session.get('job_desc', '')
    return render_template('results.html', rankings=rankings, job_desc=job_desc)


@bp.route('/download_report/<report_type>')
def download_report(report_type):
    rankings = session.get('rankings', [])
    if not rankings:
        flash('No ranking data available', 'error')
        return redirect(url_for('main.index'))

    if report_type == 'csv':
        path = report_generator.generate_csv_report(rankings)
        return send_file(path, as_attachment=True, download_name='resume_ranking_report.csv')

    elif report_type == 'pdf':
        pdf_data = report_generator.generate_pdf_report(rankings, session.get('job_desc', ''))
        if pdf_data is None:
            flash('Failed to generate PDF report.', 'error')
            return redirect(url_for('main.results'))
        return send_file(pdf_data, mimetype='application/pdf', as_attachment=True,
                         download_name='resume_ranking_report.pdf')

    flash('Invalid report type', 'error')
    return redirect(url_for('main.results'))




@bp.route('/view_analysis/<filename>')
def view_analysis(filename):
    rankings = session.get('rankings', [])
    resume = next((r for r in rankings if r['name'] == filename), None)

    if not resume:
        flash('Resume not found', 'error')
        return redirect(url_for('main.results'))

    job_desc = session.get('job_desc', '')
    job_skills = nlp_processor.extract_skills(job_desc)

    return render_template('analysis.html', resume=resume, job_skills=job_skills, job_desc=job_desc)
