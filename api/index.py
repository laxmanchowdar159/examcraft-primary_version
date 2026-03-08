from flask import Flask, render_template, request, make_response
import os
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
        f"Create a model question paper for class 10 {subject}, "
        f"{chapter} chapter, difficulty level: {difficulty}. "
        "Structure the paper as follows: "
        "Section A: 10 questions, 1 mark each; "
        "Section B: 4 questions, 2 marks each; "
        "Section C: 2 questions, 4 marks each; "
        "Section D: 1 question, 4 marks. "
        "Include suitable questions strictly matching the difficulty level, "
        "but add one challenging question in each section. "
        f"Some extra suggestions: {suggestions}. "
        "Use plain text with clear mathematical symbols, "
        "such as superscripts (x\u00b2) and fractions (a/b). "
        "Avoid LaTeX notation and delimiters like \\( \\) or $$. "
        "Follow Andhra Pradesh board syllabus and question format strictly. "
        "Respond only with the exam questions and heading\u2014no hints, explanations, or extra details, "
        "as the response will be printed as a PDF."
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 2048}
    }

    resp = requests.post(url, json=payload, timeout=55)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


def create_exam_pdf(text, subject, chapter):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)

    font_path = os.path.join(BASE_DIR, '..', 'static', 'fonts', 'DejaVuSans.ttf')
    font_path = os.path.normpath(font_path)
    pdf.add_font("DejaVu", "", font_path)
    pdf.add_font("DejaVu", "B", font_path)
    pdf.add_font("DejaVu", "I", font_path)

    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font("DejaVu", "B", 16)
    pdf.cell(0, 12, f"Class 10 Model Paper - {subject} - {chapter}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(10)

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            pdf.ln(4)
            continue
        if line.startswith("**Section"):
            pdf.set_font("DejaVu", "B", 14)
            pdf.cell(0, 10, line.replace("**", ""), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(3)
        else:
            pdf.set_font("DejaVu", "", 12)
            pdf.multi_cell(page_width, 7.5, line)
            pdf.ln(0.5)

    pdf.ln(5)
    pdf.set_font("DejaVu", "I", 12)
    pdf.cell(0, 10, "*End of Paper*", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

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
