from fpdf import FPDF
import logging
from io import BytesIO

logger = logging.getLogger(__name__)



def generate_pdf_report(rankings, job_desc):
    try:
        class PDF(FPDF):
            def header(self):
                self.set_font('Helvetica', 'B', 16)
                self.cell(0, 10, 'AI-Powered Resume Ranking Report', 0, 1, 'C')
                self.ln(10)

            def footer(self):
                self.set_y(-15)
                self.set_font('Helvetica', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Helvetica', '', 12)

        # Job Description
        pdf.set_font('Helvetica', 'B', 14)
        pdf.cell(0, 10, 'Job Description', 0, 1)
        pdf.set_font('Helvetica', '', 12)
        truncated_desc = job_desc[:500] + "..." if len(job_desc) > 500 else job_desc
        pdf.multi_cell(0, 8, truncated_desc)
        pdf.ln(10)

        # Rankings Table
        pdf.set_font('Helvetica', 'B', 14)
        pdf.cell(0, 10, 'Candidate Rankings', 0, 1)

        pdf.set_fill_color(200, 220, 255)
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(10, 10, 'R', 1, 0, 'C', 1)
        pdf.cell(60, 10, 'Name', 1, 0, 'C', 1)
        pdf.cell(30, 10, 'Score', 1, 0, 'C', 1)
        pdf.cell(90, 10, 'Contact', 1, 1, 'C', 1)

        pdf.set_font('Helvetica', '', 12)
        for rank, candidate in enumerate(rankings, 1):
            contact = f"{candidate['contact'].get('email', '')} | {candidate['contact'].get('phone', '')}"
            pdf.cell(10, 10, str(rank), 1, 0, 'C')
            pdf.cell(60, 10, candidate['name'][:30], 1)
            pdf.cell(30, 10, f"{candidate['score']:.2f}%", 1, 0, 'C')
            pdf.cell(90, 10, contact[:40], 1, 1)

        # Skill Gap Analysis
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 14)
        pdf.cell(0, 10, 'Skill Gap Analysis', 0, 1)

        for candidate in rankings[:5]:
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(0, 10, f"Candidate: {candidate['name']}", 0, 1)
            pdf.set_font('Helvetica', '', 12)

            skill_gaps = candidate.get('skill_gaps', [])
            if skill_gaps:
                gap_text = ", ".join(skill_gaps[:10])
                pdf.multi_cell(0, 8, f"Missing Skills: {gap_text}")
            else:
                pdf.cell(0, 8, "No significant skill gaps.")

            pdf.ln(5)

        # Write PDF to BytesIO
        buffer = BytesIO()
        pdf.output(buffer)
        buffer.seek(0)
        return buffer

    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")
        return None
