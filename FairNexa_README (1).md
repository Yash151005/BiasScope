FairNexa – Automated AI Fairness & Explainability Auditing

Evaluate AI. Detect Bias. Build Fairer Systems.

FairNexa is an API-driven AI fairness auditing platform designed to assess machine learning models for potential algorithmic bias, evaluate fairness across demographic groups, and provide explainable audit reports.

By providing a machine learning model's API endpoint, users can initiate an automated evaluation workflow involving synthetic test-data generation, model prediction analysis, fairness assessment, explainability techniques, and visual reporting.

The platform aims to make AI fairness evaluation more accessible by reducing the need for users to manually prepare testing pipelines or integrate multiple fairness assessment libraries.

---

🎯 Key Objectives

- Automate fairness evaluation of machine learning models through API endpoints.
- Identify potential prediction disparities across demographic groups.
- Generate synthetic test data for controlled fairness experiments.
- Integrate established fairness assessment and explainability techniques.
- Provide interpretable visualizations and downloadable audit reports.
- Establish a foundation for continuous fairness monitoring across model versions.

✨ Key Features

1. Automated Model Evaluation

- Connect to an externally hosted machine learning model using its API endpoint.
- Generate synthetic test inputs.
- Submit test requests and collect model predictions.
- Analyze prediction patterns across different demographic groups.

2. Comprehensive Fairness Assessment

- Integrate Fairlearn and AI Fairness 360 (AIF360).
- Evaluate demographic parity and other applicable fairness metrics.
- Identify potential disparities between protected groups.
- Support comparative fairness analysis.

3. Explainable AI Integration

- Integrate SHAP for feature contribution analysis.
- Integrate LIME for local prediction explanations.
- Help investigate features associated with observed prediction disparities.

4. Interactive Visualization & Reporting

- Display fairness metrics through interactive charts.
- Present comparative analysis across demographic groups.
- Generate downloadable PDF audit reports.
- Provide structured results for further investigation.

5. Automated Testing Workflow

- Reduce manual test-data preparation.
- Track analysis progress through live updates.
- Maintain analysis history and generated reports.

«Important: Synthetic-data-based testing identifies potential fairness disparities under the generated test conditions. It does not independently establish whether a model is fair in real-world deployment. Conclusions depend on data representativeness, protected attributes, ground-truth labels, and the selected fairness criteria.»

---

🏗️ System Architecture

FairNexa follows a modular architecture consisting of a frontend, backend, database, synthetic data generator, fairness analysis engine, and reporting module.

                 USER
                   |
                   v
          React + Tailwind UI
                   |
                   v
             FastAPI Backend
                   |
          +--------+--------+
          |                 |
          v                 v
    API Integration    Synthetic Data
          |              Generator
          |                 |
          +--------+--------+
                   |
                   v
             Model Testing
                   |
                   v
          Prediction Collection
                   |
                   v
          Fairness Analysis Engine
                   |
          +--------+--------+
          |        |        |
          v        v        v
       Fairlearn AIF360  SHAP/LIME
          |        |        |
          +--------+--------+
                   |
                   v
          Results & Visualization
                   |
             +-----+-----+
             |           |
             v           v
          Dashboard   PDF Reports

🛠️ Technology Stack

Frontend

- React 18
- Tailwind CSS
- Vite
- Recharts
- React Router

Backend

- Python
- FastAPI
- Faker
- Fairlearn
- IBM AI Fairness 360
- SHAP
- LIME
- Matplotlib / Plotly
- ReportLab

Database

- MongoDB

Testing & Integration

- REST API integration
- Synthetic test-data generation
- Sample model API
- Automated prediction collection

---

📊 How FairNexa Works

Step 1 – Model Connection

The user provides an externally accessible machine learning model API endpoint.

Step 2 – Synthetic Data Generation

FairNexa generates test inputs using synthetic data generation techniques such as Faker. CTGAN can be explored for more advanced tabular data generation.

Step 3 – Model Evaluation

Generated inputs are submitted to the connected model API, and prediction responses are collected.

Step 4 – Fairness Analysis

Fairlearn and AIF360 are used to calculate applicable fairness metrics and identify potential disparities across demographic groups.

Step 5 – Explainability Analysis

SHAP and LIME can be used to investigate feature contributions and individual prediction explanations, subject to model and integration compatibility.

Step 6 – Visualization and Reporting

The results are presented through an interactive dashboard, with downloadable PDF reports for documentation and further analysis.

---

🔬 Research Direction & Potential Contributions

FairNexa provides a foundation for research into automated fairness assessment of externally hosted machine learning models.

The following areas represent potential research extensions and should not be interpreted as already implemented features unless supported by the actual codebase.

| Research Area | Proposed Enhancement |
|---|---|
| Automated Schema Discovery | Identify model input fields and data types from API specifications
| Intelligent Synthetic Testing | Investigate statistically controlled generation of demographic test populations
| Multi-Metric Fairness Evaluation | Compare multiple fairness definitions and metrics
| Fairness-Aware Explainability | Investigate explanations associated with observed group disparities
| Continuous Fairness Monitoring | Compare fairness results across successive model versions
| Audit Reproducibility | Record test configurations, assumptions, metrics and evaluation results

Potential Research Questions

1. How effectively can API-driven testing identify prediction disparities without access to original training data?
2. How do synthetic-data generation assumptions influence measured fairness metrics?
3. Can explainability techniques help investigate the features associated with demographic disparities?
4. How consistently do different fairness assessment frameworks evaluate the same model?
5. How can fairness changes be monitored across different model versions?

---

📁 Project Structure

FairNexa/
│
├── frontend/              # React + Tailwind CSS interface
├── backend/               # FastAPI backend
├── database/              # MongoDB schemas and utilities
├── sample_model_api/      # Sample prediction API
├── reports/               # Generated analysis reports
├── docs/                  # Project documentation
│
└── README.md

---

🚀 Getting Started

Prerequisites

- Node.js 18+
- Python 3.9+
- MongoDB
- Git

1. Clone Repository

git clone https://github.com/Yash151005/FairNexa.git
cd FairNexa

2. Frontend Setup

cd frontend
npm install

3. Backend Setup

cd ../backend
python -m venv venv

Activate the environment:

Windows

venv\Scripts\activate

Linux / macOS

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Configure environment variables:

cp .env.example .env

Update the MongoDB connection settings in ".env".

4. Start MongoDB

Ensure your MongoDB service is running.

5. Run Backend

uvicorn main:app --reload --host 0.0.0.0 --port 8000

6. Run Frontend

cd frontend
npm run dev

7. Access Application

| Service | URL |
|---|---|
| Frontend | http://localhost:3000
| Backend | http://localhost:8000
| API Documentation | http://localhost:8000/docs

Use the actual Vite development port configured in your project if it differs from 3000.

---

🧪 Test with Sample Model API

FairNexa includes a sample model API to demonstrate the evaluation workflow without requiring an external machine learning deployment.

cd sample_model_api
python -m venv venv

Activate the virtual environment and install dependencies:

pip install -r requirements.txt

Start the sample API:

uvicorn app:app --reload --host 0.0.0.0 --port 5000

Sample prediction endpoint:

http://localhost:5000/predict

Use this endpoint in the FairNexa frontend to test the integration.

---

🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/analysis/start` | Start a fairness analysis
| `GET` | `/api/analysis/{analysis_id}` | Retrieve analysis results
| `GET` | `/api/analysis/{analysis_id}/report` | Download PDF report
| `GET` | `/api/analyses` | Retrieve analysis history

Refer to "docs/api-documentation.md" for additional details.

---

⚖️ Fairness Evaluation Considerations

Fairness is context-dependent. Different applications may require different fairness definitions and evaluation criteria.

FairNexa is designed around the following considerations:

- Demographic Parity: Compare positive prediction rates across demographic groups.
- Equalized Odds: Compare true-positive and false-positive rates across groups when ground-truth labels are available.
- Disparate Impact: Examine relative differences in favorable outcomes.
- Explainability: Investigate feature contributions associated with model predictions.

A fairness metric should not be interpreted independently of the application's context, dataset assumptions, and applicable ethical or legal requirements.

---

👥 Team

| Member | Responsibility |
|---|---|
| Rushikesh | Frontend Development Lead
| Sandip | UI Styling and Responsiveness
| Tejas | Database Schema Design and Data Consistency
| Yash | Documentation and Training Materials

---

📚 Documentation

Additional documentation is available in the "docs/" directory:

- Getting Started
- User Interface Guide
- Interpreting Results
- System Architecture
- Bias and Fairness Concepts
- How to Use FairNexa
- Best Practices

---

🔮 Future Scope

- Automated model API schema discovery.
- Advanced synthetic data generation using CTGAN.
- Support for additional fairness metrics and assessment frameworks.
- Improved explainability and fairness correlation analysis.
- Fairness monitoring across model versions.
- Reproducible benchmarking using public fairness datasets.
- Expanded support for different model API formats.
- Security enhancements for externally supplied API endpoints.

---

📄 License

License information will be added once the project license is finalized.

🤝 Contributing

Contribution guidelines will be published as the project develops.

🙏 Acknowledgments

We acknowledge the developers and research communities behind:

- Microsoft Fairlearn
- IBM AI Fairness 360
- SHAP
- LIME
- FastAPI
- React

---

FairNexa – Making AI Fairness Measurable, Explainable, and Accessible.
