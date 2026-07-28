import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from backend.schemas.audit import AuditReport
from backend.schemas.ai import AIAnalysisResponse

def generate_pdf_report(report: AuditReport, ai_analysis: AIAnalysisResponse = None) -> bytes:
    """
    Generates a professional PDF audit report using ReportLab.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1e1b4b"),
        spaceAfter=12
    )

    heading2_style = ParagraphStyle(
        'Heading2Style',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#312e81"),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    story = []

    # Title Banner
    story.append(Paragraph("AI Dataset Intelligence Copilot", title_style))
    story.append(Paragraph(f"Dataset Audit & Health Report for: <b>{report.filename}</b>", body_style))
    story.append(Paragraph(f"Analysis Timestamp: {report.analyzed_at}", body_style))
    story.append(Spacer(1, 12))

    # Readiness Score Summary Box
    score_data = [
        ["Overall Readiness Score", "Grade", "Status"],
        [f"{report.readiness_score.overall_score} / 100", report.readiness_score.grade, report.readiness_score.status]
    ]
    score_table = Table(score_data, colWidths=[200, 100, 240])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4338ca")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#e0e7ff")),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor("#1e1b4b")),
        ('FONTSIZE', (0, 1), (-1, 1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#c7d2fe"))
    ]))
    story.append(score_table)
    story.append(Spacer(1, 14))

    # Summary Statistics Table
    story.append(Paragraph("Dataset Overview Metrics", heading2_style))
    summary_data = [
        ["Metric", "Value"],
        ["Total Rows", str(report.summary.total_rows)],
        ["Total Columns", str(report.summary.total_columns)],
        ["Missing Cells", f"{report.summary.total_missing_cells} ({report.summary.total_missing_pct}%)"],
        ["Duplicate Rows", f"{report.summary.total_duplicate_rows} ({report.summary.total_duplicate_pct}%)"],
        ["Outliers (IQR)", str(report.summary.total_outliers)]
    ]
    summary_table = Table(summary_data, colWidths=[250, 290])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 14))

    # Quality Issues
    story.append(Paragraph("Detected Quality Issues", heading2_style))
    if report.issues:
        issue_data = [["Severity", "Column", "Issue Title", "Description"]]
        for iss in report.issues:
            issue_data.append([
                iss.severity.upper(),
                iss.column or "Dataset-wide",
                iss.title,
                iss.description
            ])
        issue_table = Table(issue_data, colWidths=[70, 90, 140, 240])
        issue_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#334155")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(issue_table)
    else:
        story.append(Paragraph("No quality issues detected.", body_style))

    story.append(Spacer(1, 14))

    # AI Section if available
    if ai_analysis:
        story.append(Paragraph("AI Executive Reasoning & Remediation", heading2_style))
        story.append(Paragraph(f"<b>Summary:</b> {ai_analysis.health_summary}", body_style))
        story.append(Spacer(1, 6))

        if ai_analysis.python_code:
            story.append(Paragraph("<b>Generated Python Cleaning Script Snippet:</b>", body_style))
            code_style = ParagraphStyle(
                'CodeStyle',
                parent=styles['Code'],
                fontSize=7,
                leading=9,
                textColor=colors.HexColor("#0f172a"),
                backColor=colors.HexColor("#f1f5f9"),
                borderColor=colors.HexColor("#cbd5e1"),
                borderWidth=1,
                borderPadding=6,
                spaceAfter=10
            )
            # Truncate long code for PDF print
            code_preview = ai_analysis.python_code[:1200]
            story.append(Paragraph(code_preview.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
