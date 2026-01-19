"""
Report Generator Service - Generate visual and PDF reports using Matplotlib and Plotly
"""

import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from typing import Dict, Any
from datetime import datetime
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
        """Generate PDF report using ReportLab"""
        pdf_path = os.path.join(self.reports_dir, f"{analysis_id}_report.pdf")
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        # Title
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#0ea5e9"),
            spaceAfter=30,
            alignment=TA_CENTER,
        )
        story.append(Paragraph("BiasScope Analysis Report", title_style))
        story.append(Spacer(1, 0.2 * inch))

        # Analysis Info
        info_style = ParagraphStyle(
            "InfoStyle", parent=styles["Normal"], fontSize=10, textColor=colors.grey
        )
        story.append(
            Paragraph(f"Analysis ID: {analysis_id}", info_style)
        )
        story.append(
            Paragraph(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                info_style,
            )
        )
        story.append(Spacer(1, 0.3 * inch))

        # Overall Bias Score
        bias_score = results.get("overall_bias_score", 0)
        story.append(
            Paragraph(
                f"Overall Bias Score: {bias_score:.3f}",
                styles["Heading2"],
            )
        )
        story.append(
            Paragraph(
                "Lower scores indicate less bias (0 = no bias, 1 = maximum bias)",
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 0.2 * inch))

        # Fairness Metrics Table
        if results.get("fairness_metrics"):
            story.append(Paragraph("Fairness Metrics", styles["Heading2"]))
            data = [["Metric", "Value"]]
            for metric in results["fairness_metrics"]:
                data.append([metric["metric"], f"{metric['value']:.4f}"])

            table = Table(data)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )
            story.append(table)
            story.append(Spacer(1, 0.3 * inch))

        # Feature Influence
        if results.get("feature_influence"):
            story.append(Paragraph("Feature Influence on Bias", styles["Heading2"]))
            data = [["Feature", "Influence", "Importance"]]
            for feature in results["feature_influence"]:
                data.append(
                    [
                        feature["feature"],
                        f"{feature['influence']:.4f}",
                        f"{feature['importance']:.4f}",
                    ]
                )

            table = Table(data)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )
            story.append(table)

        # Build PDF
        doc.build(story)
        return pdf_path
