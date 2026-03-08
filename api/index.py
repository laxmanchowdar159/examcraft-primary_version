from flask import Flask, render_template, request, make_response
import os
import re
import requests
from fpdf import FPDF
from fpdf.enums import XPos, YPos

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------- Generate Paper --------------------
def generate_paper(subject, chapter, difficulty, suggestions):
    api_key = os.environ.get("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    prompt = (
        f"Create a complete model question paper for class 10 {subject}, "
        f"{chapter} chapter, difficulty level: {difficulty}. "
        "Structure the paper as follows: "
        "Section A: 10 questions, 1 mark each (write all 10); "
        "Section B: 4 questions, 2 marks each (write all 4); "
        "Section C: 2 questions, 4 marks each (write both); "
        "Section D: 1 question, 4 marks (write it). "
        "Include suitable questions strictly matching the difficulty level, "
        "but add one challenging question in each section. "
        f"Extra suggestions: {suggestions}. "
        "IMPORTANT FORMATTING RULES: "
        "- Do NOT use markdown bold (**text**) anywhere. Use plain text only. "
        "- Write section headings as: SECTION A (10 x 1 = 10 Marks) "
        "- Use plain text with clear mathematical symbols like x2 for squared, a/b for fractions. "
        "- Do NOT use LaTeX like \\( \\) or $$. "
        "- Follow Andhra Pradesh board syllabus strictly. "
        "- Output ONLY the questions and section headings. No hints, answers, or explanations."
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 8192}
    }

    resp = requests.post(url, json=payload, timeout=55)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


def clean_line(line):
    """Strip all markdown formatting from a line."""
    # Remove bold/italic markers
    line = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', line)
    # Remove markdown heading hashes
    line = re.sub(r'^#{1,6}\s*', '', line)
    return line.strip()


def create_exam_pdf(text, subject, chapter):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)

    font_path = os.path.normpath(os.path.join(BASE_DIR, '..', 'static', 'fonts', 'DejaVuSans.ttf'))
    pdf.add_font("DejaVu", "", font_path)
    pdf.add_font("DejaVu", "B", font_path)
    pdf.add_font("DejaVu", "I", font_path)

    page_width = pdf.w - 2 * pdf.l_margin

    # Title
    pdf.set_font("DejaVu", "B", 16)
    pdf.cell(0, 12, f"Class 10 Model Paper - {subject} - {chapter}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(6)

    for line in text.split('\n'):
        line = clean_line(line)
        if not line:
            pdf.ln(3)
            continue

        # Detect section headings like "SECTION A" or "Section A"
        if re.match(r'^(SECTION|Section)\s+[A-D]', line):
            pdf.ln(4)
            pdf.set_font("DejaVu", "B", 13)
            pdf.cell(0, 10, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(2)
        else:
            pdf.set_font("DejaVu", "", 11)
            pdf.multi_cell(page_width, 7, line)
            pdf.ln(1)

    # Footer
    pdf.ln(5)
    pdf.set_font("DejaVu", "I", 11)
    pdf.cell(0, 10, "--- End of Paper ---", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    return bytes(pdf.output(dest="S"))


# -------------------- Routes --------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        chapter = request.form['chapter']
        difficulty = request.form['difficulty']
        suggestions = request.form.get('suggestions', '')

        paper_text = generate_paper(subject, chapter, difficulty, suggestions)
        pdf_content = create_exam_pdf(paper_text, subject, chapter)

        response = make_response(pdf_content)
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'attachment',
                             filename=f"{subject}_{chapter}.pdf")
        return response

    return render_template('form.html')