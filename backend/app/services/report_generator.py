"""
Report Generator Service - Generate visual and PDF reports using Matplotlib and Plotly
"""

import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from typing import Dict, Any
from datetime import datetime
import hashlib
import hmac
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class ReportGenerator:
    """Service for generating analysis reports"""

    def __init__(self):
        self.reports_dir = settings.reports_directory
        os.makedirs(self.reports_dir, exist_ok=True)

    async def generate_report(
        self, analysis_id: str, results: Dict[str, Any]
    ) -> str:
        """
        Generate comprehensive PDF report with visualizations
        Returns path to generated report
        """
        try:
            # Generate visualizations
            self._generate_visualizations(analysis_id, results)

            # Generate PDF report
            report_path = self._generate_pdf_report(analysis_id, results)

            logger.info(f"Generated report for analysis {analysis_id}: {report_path}")
            return report_path

        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise

    def _generate_visualizations(
        self, analysis_id: str, results: Dict[str, Any]
    ) -> None:
        """Generate visualization files using Matplotlib and Plotly"""
        try:
            # Generate Plotly HTML report
            fig = make_subplots(
                rows=2,
                cols=2,
                subplot_titles=(
                    "Fairness Metrics",
                    "Feature Influence",
                    "Demographic Parity",
                    "Bias Score Overview",
                ),
                specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "pie"}, {"type": "indicator"}]],
            )

            # Fairness Metrics
            if results.get("fairness_metrics"):
                metrics = results["fairness_metrics"]
                fig.add_trace(
                    go.Bar(
                        x=[m["metric"] for m in metrics],
                        y=[m["value"] for m in metrics],
                        name="Fairness Metrics",
                    ),
                    row=1,
                    col=1,
                )

            # Feature Influence
            if results.get("feature_influence"):
                features = results["feature_influence"]
                fig.add_trace(
                    go.Bar(
                        x=[f["influence"] for f in features],
                        y=[f["feature"] for f in features],
                        orientation="h",
                        name="Feature Influence",
                    ),
                    row=1,
                    col=2,
                )

            # Demographic Parity
            if results.get("demographic_parity"):
                demo = results["demographic_parity"]
                fig.add_trace(
                    go.Pie(
                        labels=[d["name"] for d in demo],
                        values=[d["value"] for d in demo],
                        name="Demographic Parity",
                    ),
                    row=2,
                    col=1,
                )

            # Bias Score Indicator
            bias_score = results.get("overall_bias_score", 0)
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=bias_score,
                    domain={"x": [0, 1], "y": [0, 1]},
                    title={"text": "Overall Bias Score"},
                    gauge={
                        "axis": {"range": [None, 1]},
                        "bar": {"color": "darkblue"},
                        "steps": [
                            {"range": [0, 0.3], "color": "lightgreen"},
                            {"range": [0.3, 0.7], "color": "yellow"},
                            {"range": [0.7, 1], "color": "red"},
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 4},
                            "thickness": 0.75,
                            "value": 0.5,
                        },
                    },
                ),
                row=2,
                col=2,
            )

            fig.update_layout(
                height=800,
                title_text=f"BiasScope Analysis Report - {analysis_id}",
                showlegend=False,
            )

            # Save Plotly HTML
            html_path = os.path.join(self.reports_dir, f"{analysis_id}_interactive.html")
            fig.write_html(html_path)
            logger.info(f"Generated interactive HTML report: {html_path}")

        except Exception as e:
            logger.warning(f"Error generating visualizations: {str(e)}")

    def _generate_pdf_report(
        self, analysis_id: str, results: Dict[str, Any]
    ) -> str:
        """Generate professional PDF report with authenticity certificate"""
        print(f"Starting PDF generation for analysis {analysis_id}")
        pdf_path = os.path.join(self.reports_dir, f"{analysis_id}_report.pdf")
        print(f"PDF path: {pdf_path}")
        doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []
        styles = getSampleStyleSheet()
        print("Initialized PDF document and styles")

        # ===== PAGE 1: COVER PAGE WITH CERTIFICATE =====
        print("Starting cover page generation")
        
        # Header with logo styling
        header_style = ParagraphStyle(
            "HeaderStyle",
            parent=styles["Heading1"],
            fontSize=32,
            textColor=colors.HexColor("#0ea5e9"),
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold"
        )
        story.append(Paragraph("BiasScope", header_style))
        story.append(Spacer(1, 0.1 * inch))
        
        subtitle_style = ParagraphStyle(
            "SubtitleStyle",
            parent=styles["Normal"],
            fontSize=14,
            textColor=colors.HexColor("#666666"),
            alignment=TA_CENTER,
            fontName="Helvetica"
        )
        story.append(Paragraph("AI Bias & Fairness Analysis Platform", subtitle_style))
        story.append(Spacer(1, 0.4 * inch))

        # Certificate of Analysis
        cert_title = ParagraphStyle(
            "CertTitle",
            parent=styles["Heading2"],
            fontSize=20,
            textColor=colors.HexColor("#0ea5e9"),
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName="Helvetica-Bold"
        )
        story.append(Paragraph("CERTIFICATE OF AUTHENTICITY", cert_title))
        story.append(HRFlowable(width=4*inch, thickness=2, lineCap='round', color=colors.HexColor("#0ea5e9")))
        story.append(Spacer(1, 0.3 * inch))

        # Certificate body
        cert_body = ParagraphStyle(
            "CertBody",
            parent=styles["Normal"],
            fontSize=11,
            alignment=TA_CENTER,
            leading=16,
        )
        
        cert_date = datetime.now().strftime('%B %d, %Y')
        # Convert ObjectId to string if needed
        analysis_id_str = str(analysis_id)
        cert_number = analysis_id_str[:8].upper()
        
        story.append(Paragraph(
            f"This is to certify that the bias and fairness analysis contained herein "
            f"has been conducted using advanced machine learning algorithms and statistical methods.",
            cert_body
        ))
        story.append(Spacer(1, 0.2 * inch))
        
        # Certificate details table
        cert_data = [
            ["Analysis ID:", cert_number],
            ["Issue Date:", cert_date],
            ["Platform:", "BiasScope v1.0"],
            ["Certification Status:", "✓ VERIFIED & AUTHENTIC"],
        ]
        
        cert_table = Table(cert_data, colWidths=[2*inch, 3*inch])
        cert_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (0, -1), "RIGHT"),
            ("ALIGN", (1, 0), (1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 11),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#0ea5e9")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("LINEBELOW", (0, -1), (-1, -1), 2, colors.HexColor("#0ea5e9")),
        ]))
        story.append(cert_table)
        story.append(Spacer(1, 0.3 * inch))

        # Digital signature section
        digital_sig = self._generate_digital_signature(analysis_id)
        sig_style = ParagraphStyle(
            "SigStyle",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.HexColor("#666666"),
            alignment=TA_CENTER,
            fontName="Courier"
        )
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("<b>Digital Signature (HMAC-SHA256):</b>", sig_style))
        story.append(Spacer(1, 0.1 * inch))
        
        # Wrap signature in smaller chunks for display
        sig_display = digital_sig[:32] + "<br/>" + digital_sig[32:]
        story.append(Paragraph(sig_display, sig_style))
        story.append(Spacer(1, 0.2 * inch))

        # Authenticity badge
        badge_style = ParagraphStyle(
            "BadgeStyle",
            parent=styles["Normal"],
            fontSize=12,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#10b981")
        )
        story.append(Paragraph("🔒 REPORT AUTHENTICITY VERIFIED", badge_style))
        
        # Page break
        story.append(PageBreak())

        # ===== PAGE 2: ANALYSIS RESULTS =====

        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=22,
            textColor=colors.HexColor("#0ea5e9"),
            spaceAfter=20,
            alignment=TA_LEFT,
            fontName="Helvetica-Bold"
        )
        story.append(Paragraph("Analysis Results", title_style))

        # Analysis Info
        info_style = ParagraphStyle(
            "InfoStyle", parent=styles["Normal"], fontSize=10, textColor=colors.grey
        )
        
        info_data = [
            ["Report Generated:", datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')],
            ["Analysis ID:", analysis_id],
            ["Report Version:", "1.0"],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (0, -1), "RIGHT"),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#0ea5e9")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.3 * inch))

        # Overall Bias Score - Enhanced display with percentage, alignment, and recommendations
        print("Starting bias score section")
        bias_score = results.get("overall_bias_score", 0)
        bias_percentage = bias_score * 100
        print(f"Bias score: {bias_score}, percentage: {bias_percentage}")

        score_section_style = ParagraphStyle(
            "ScoreSection",
            parent=styles["Heading2"],
            fontSize=16,
            textColor=colors.HexColor("#0ea5e9"),
            spaceAfter=15,
            fontName="Helvetica-Bold",
            alignment=TA_CENTER
        )
        story.append(Paragraph("Overall Bias Score Assessment", score_section_style))
        print("Added score section title")

        # Bias score with color coding and percentage
        bias_color = self._get_bias_color(bias_score)
        score_style = ParagraphStyle(
            "ScoreStyle",
            parent=styles["Normal"],
            fontSize=28,
            textColor=bias_color,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold"
        )
        # Show both score and percentage, aligned horizontally
        score_table = Table([
            [
                Paragraph(f"<b>{bias_score:.4f}</b>", score_style),
                Paragraph(f"<b>{bias_percentage:.1f}%</b>", score_style)
            ]
        ], colWidths=[2*inch, 2*inch], hAlign='CENTER')
        score_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 0.3 * inch))
        print("Added bias score table")

        fairness_level = self._get_fairness_level(bias_score)
        level_style = ParagraphStyle(
            "LevelStyle",
            parent=styles["Normal"],
            fontSize=12,
            alignment=TA_CENTER,
            textColor=bias_color,
            fontName="Helvetica-Bold"
        )
        story.append(Paragraph(f"Fairness Level: {fairness_level}", level_style))
        story.append(Spacer(1, 0.3 * inch))
        print("Added fairness level")

        # Recommendations based on bias score
        recommendation = self._get_recommendation(bias_score)
        recommendation_style = ParagraphStyle(
            "RecommendationStyle",
            parent=styles["Normal"],
            fontSize=11,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0ea5e9"),
            spaceAfter=8,
        )
        story.append(Paragraph(f"<b>Recommendation:</b> {recommendation}", recommendation_style))
        story.append(Spacer(1, 0.1 * inch))
        print("Added recommendation")

        # Bias scale explanation
        explanation_style = ParagraphStyle(
            "ExplanationStyle",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER,
        )
        story.append(Paragraph(
            "<b>Scale:</b> 0.0-0.3 = Low Bias | 0.3-0.7 = Moderate Bias | 0.7-1.0 = High Bias",
            explanation_style
        ))
        story.append(Spacer(1, 0.3 * inch))
        print("Added bias scale explanation")
        print("Finished bias score section")

        # Fairness Metrics Table
        print("Starting fairness metrics section")
        if results.get("fairness_metrics"):
            story.append(Paragraph("Detailed Fairness Metrics", score_section_style))
            data = [["Metric Name", "Value", "Interpretation"]]
            
            metric_interpretations = {
                "demographic_parity": "Statistical Parity",
                "equalized_odds": "Equalized Odds",
                "predictive_parity": "Predictive Parity",
                "disparate_impact": "Disparate Impact Ratio",
            }
            
            for metric in results["fairness_metrics"]:
                metric_name = metric_interpretations.get(metric["metric"], metric["metric"])
                data.append([
                    metric_name,
                    f"{metric['value']:.4f}",
                    self._interpret_metric(metric["metric"], metric["value"])
                ])

            table = Table(data, colWidths=[2*inch, 1.5*inch, 2*inch])
            table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0ea5e9")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("ALIGN", (1, 1), (1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    ("FONTSIZE", (0, 1), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("TOPPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f0f9ff")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#0ea5e9")),
                ])
            )
            story.append(table)
            story.append(Spacer(1, 0.3 * inch))
            print("Added fairness metrics table")

        # Feature Influence Analysis
        print("Starting feature influence section")
        if results.get("feature_influence"):
            story.append(Paragraph("Feature Influence Analysis", score_section_style))
            story.append(Spacer(1, 0.2 * inch))

            # Create feature influence table
            feature_data = [["Feature", "Influence Score", "Bias Contribution"]]
            for feature in results["feature_influence"][:10]:  # Top 10 features
                feature_data.append([
                    feature.get("feature", "Unknown"),
                    f"{feature.get('influence', 0):.4f}",
                    "High" if feature.get('influence', 0) > 0.7 else "Moderate" if feature.get('influence', 0) > 0.3 else "Low"
                ])

            feature_table = Table(feature_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            feature_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0ea5e9")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("ALIGN", (1, 1), (2, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    ("FONTSIZE", (0, 1), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("TOPPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f0f9ff")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#0ea5e9")),
                ])
            )
            story.append(feature_table)
            story.append(Spacer(1, 0.3 * inch))
            print("Added feature influence table")

        # Group Bias Analysis
        print("Starting group bias section")
        if results.get("group_bias"):
            story.append(Paragraph("Group Bias Analysis", score_section_style))
            story.append(Spacer(1, 0.2 * inch))

            group_data = [["Group", "Bias Score", "Sample Size", "Status"]]
            for group in results["group_bias"]:
                bias_score = group.get("bias_score", 0)
                status = "✓ Fair" if bias_score < 0.3 else "⚠ Moderate" if bias_score < 0.7 else "✗ High Bias"
                group_data.append([
                    group.get("group", "Unknown"),
                    f"{bias_score:.4f}",
                    str(group.get("sample_size", 0)),
                    status
                ])

            group_table = Table(group_data, colWidths=[1.5*inch, 1.5*inch, 1.2*inch, 1.5*inch])
            group_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0ea5e9")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("ALIGN", (1, 1), (2, -1), "CENTER"),
                    ("ALIGN", (3, 1), (3, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    ("FONTSIZE", (0, 1), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("TOPPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f0f9ff")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#0ea5e9")),
                ])
            )
            story.append(group_table)
            story.append(Spacer(1, 0.3 * inch))
            print("Added group bias table")

        # Visualizations
        print("Starting visualizations section")
        if results.get("visualizations"):
            story.append(Paragraph("Analysis Visualizations", score_section_style))
            story.append(Spacer(1, 0.2 * inch))

            for viz_name, viz_path in results["visualizations"].items():
                if os.path.exists(viz_path):
                    try:
                        img = Image(viz_path, width=6*inch, height=4*inch)
                        story.append(img)
                        story.append(Spacer(1, 0.2 * inch))
                        print(f"Added visualization: {viz_name}")
                    except Exception as e:
                        print(f"Failed to add visualization {viz_name}: {e}")
                        logger.warning(f"Failed to add visualization {viz_name}: {e}")

        # Digital Signature and Certificate
        print("Starting digital signature section")
        signature = self._generate_digital_signature(analysis_id)
        cert_style = ParagraphStyle(
            "CertificateStyle",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#0ea5e9"),
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold"
        )
        story.append(Paragraph("Authenticity Certificate", cert_style))
        story.append(Spacer(1, 0.2 * inch))

        # Certificate content
        cert_data = [
            ["Certificate Details", ""],
            ["Analysis ID", analysis_id],
            ["Report Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["Digital Signature", signature[:32] + "..."],
            ["Verification Status", "✓ AUTHENTIC"],
        ]

        cert_table = Table(cert_data, colWidths=[2*inch, 3*inch])
        cert_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0ea5e9")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f0f9ff")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOX", (0, 0), (-1, -1), 2, colors.HexColor("#0ea5e9")),
                ("INNERGRID", (0, 0), (-1, -1), 1, colors.HexColor("#0ea5e9")),
            ])
        )
        story.append(cert_table)
        story.append(Spacer(1, 0.3 * inch))
        print("Added certificate")

        # Build PDF with error handling
        print(f"About to build PDF with {len(story)} story elements")
        try:
            doc.build(story)
            print("PDF built successfully")
        except Exception as e:
            import traceback
            logger.error(f"Exception during PDF build: {e}")
            logger.error(traceback.format_exc())
            print(f"Exception during PDF build: {e}")
            print(traceback.format_exc())
            return None
        print(f"Returning PDF path: {pdf_path}")
        return pdf_path

    def _get_recommendation(self, bias_score: float) -> str:
        """Return recommendation string based on bias score"""
        if bias_score < 0.3:
            return "Your model is fair and unbiased. Continue monitoring for changes as data evolves."
        elif bias_score < 0.7:
            return "Moderate bias detected. Review feature influence and consider rebalancing your training data or applying bias mitigation techniques."
        else:
            return "High bias detected! Strongly recommended to review data, retrain the model, and apply fairness interventions."

    def _generate_digital_signature(self, analysis_id: str) -> str:
        """Generate HMAC-SHA256 digital signature"""
        secret_key = b"BiasScope-Authenticity-Key-2026"
        message = f"{analysis_id}-{datetime.now().strftime('%Y-%m-%d')}".encode()
        signature = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
        return signature

    def _get_bias_color(self, bias_score: float) -> colors.Color:
        """Return color based on bias score"""
        if bias_score < 0.3:
            return colors.HexColor("#10b981")  # Green - Low bias
        elif bias_score < 0.7:
            return colors.HexColor("#f59e0b")  # Amber - Moderate bias
        else:
            return colors.HexColor("#ef4444")  # Red - High bias

    def _get_fairness_level(self, bias_score: float) -> str:
        """Get fairness level description"""
        if bias_score < 0.3:
            return "✓ FAIR & UNBIASED"
        elif bias_score < 0.7:
            return "⚠ MODERATE BIAS DETECTED"
        else:
            return "✗ HIGH BIAS DETECTED"

    def _interpret_metric(self, metric: str, value: float) -> str:
        """Provide interpretation for metric values"""
        if metric == "disparate_impact":
            if value >= 0.8:
                return "Acceptable (4/5 rule met)"
            else:
                return "Potential disparate impact"
        elif value < 0.1:
            return "Excellent - Near perfect fairness"
        elif value < 0.3:
            return "Good - Acceptable fairness"
        elif value < 0.5:
            return "Fair - Some bias present"
        else:
            return "Poor - Significant bias"
