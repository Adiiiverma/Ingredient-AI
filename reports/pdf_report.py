from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(filename, overall_score, analysis, ai_result):

    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate(filename)

    story = []

    story.append(Paragraph("<b>IngredientAI Report</b>", styles["Title"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(f"<b>Overall Health Score:</b> {overall_score:.1f}/10", styles["BodyText"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Ingredient Analysis</b>", styles["Heading2"]))

    for item in analysis:

        story.append(
            Paragraph(
                f"""
                <b>{item['name']}</b><br/>
                Category: {item['category']}<br/>
                Health Score: {item['health_score']}/10<br/>
                Risk Level: {item['risk_level']}<br/>
                Benefits: {item['benefits']}<br/>
                Side Effects: {item['side_effects']}<br/>
                Recommendation: {item['recommendation']}
                """,
                styles["BodyText"]
            )
        )

    story.append(Paragraph("<br/>", styles["Normal"]))
    story.append(Paragraph("<b>AI Recommendation</b>", styles["Heading2"]))
    story.append(Paragraph(ai_result, styles["BodyText"]))

    story.append(Paragraph("<br/><br/>Made with ❤️ by Aditya Verma", styles["Italic"]))

    pdf.build(story)