from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.spider import SpiderChart
import io

def generate_pdf_report(candidate, domain, difficulty, total_score, skill_avgs, feedback, questions, answers, evaluations):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("AI Interview System — Performance Report", styles["Title"]))
    story.append(Spacer(1, 12))

    # Candidate Info
    story.append(Paragraph(f"<b>Candidate:</b> {candidate}", styles["Normal"]))
    story.append(Paragraph(f"<b>Domain:</b> {domain}", styles["Normal"]))
    story.append(Paragraph(f"<b>Difficulty:</b> {difficulty}", styles["Normal"]))
    story.append(Paragraph(f"<b>Overall Score:</b> {total_score:.1f} / 100", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Skill Scores Table
    story.append(Paragraph("<b>Skill Breakdown</b>", styles["Heading2"]))
    table_data = [["Skill", "Score"]]
    for skill, score in skill_avgs.items():
        table_data.append([skill.replace("_", " ").title(), f"{score}/100"])

    table = Table(table_data, colWidths=[300, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4A90D9")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 16))

    # Feedback
    story.append(Paragraph("<b>AI Feedback</b>", styles["Heading2"]))
    story.append(Paragraph(feedback.replace("\n", "<br/>"), styles["Normal"]))
    story.append(Spacer(1, 16))

    # Q&A Breakdown
    story.append(Paragraph("<b>Question-by-Question Breakdown</b>", styles["Heading2"]))
    for i, (q, a, ev) in enumerate(zip(questions, answers, evaluations)):
        story.append(Paragraph(f"<b>Q{i+1}:</b> {q.get('question', '')}", styles["Normal"]))
        story.append(Paragraph(f"<b>Your Answer:</b> {a}", styles["Normal"]))
        story.append(Paragraph(f"<b>Score:</b> {ev.get('overall_score', 0)}/100 — {ev.get('verdict', '')}", styles["Normal"]))
        story.append(Paragraph(f"<b>Strengths:</b> {', '.join(ev.get('strengths', []))}", styles["Normal"]))
        story.append(Paragraph(f"<b>Improvements:</b> {', '.join(ev.get('improvements', []))}", styles["Normal"]))
        story.append(Spacer(1, 10))

    doc.build(story)
    buffer.seek(0)

    return buffer

    return buffer