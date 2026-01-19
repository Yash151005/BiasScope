# BiasScope - AI Bias & Fairness Analysis Tool

BiasScope is an automated tool for evaluating AI models for bias and fairness. Simply provide your model's API endpoint, and BiasScope will automatically generate synthetic test data, evaluate your model, and present comprehensive bias analysis results with visual reports.

## 🎯 Key Features

- **Automated Testing**: Generate synthetic data and evaluate models without manual input
- **Comprehensive Analysis**: Uses Fairlearn, AIF360, SHAP, and LIME for thorough bias assessment
- **Visual Reports**: Interactive charts and downloadable PDF reports
- **Easy to Use**: Just provide your model API URL - no training or data preparation needed
- **Real-time Progress**: Track analysis progress with live updates

## 🏗️ Project Structure

```
BiasScope/
├── frontend/          # React + Tailwind CSS UI
├── backend/           # FastAPI Python backend
├── database/          # MongoDB schemas and utilities
├── sample_model_api/  # Local dummy model API for testing BiasScope
├── reports/           # Generated analysis reports
└── docs/              # Documentation and training materials
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm/yarn
- **Python** 3.9+
- **MongoDB** (local or remote)
- **Git**

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd BiasScope
```

2. **Set up Frontend**
```bash
cd frontend
npm install
```

3. **Set up Backend**
```bash
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your MongoDB URL and settings
```

4. **Start MongoDB**
```bash
# On Windows (if MongoDB is installed)
mongod
```

5. **Run the Application**

Terminal 1 - Backend:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

6. **Access BiasScope**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📖 Usage

1. **Start Analysis**: Enter your AI model's API URL in the frontend
2. **Monitor Progress**: Watch real-time progress updates
3. **View Results**: Explore bias scores, fairness metrics, and visualizations
4. **Download Report**: Get comprehensive PDF report with all findings

## 🛠️ Technology Stack

### Frontend
- **React 18** - UI framework
- **Tailwind CSS** - Styling
- **Vite** - Build tool
- **Recharts** - Data visualization
- **React Router** - Routing

### Backend
- **FastAPI** - Web framework
- **MongoDB** - Database
- **Faker** - Synthetic data generation
- **Fairlearn** - Fairness assessment
- **AIF360** - AI Fairness toolkit
- **SHAP/LIME** - Explainability
- **Matplotlib/Plotly** - Visualization
- **ReportLab** - PDF generation

## 👥 Team

- **Rushikesh** - Frontend development lead
- **Sandip** - UI styling and responsiveness
- **Tejas** - Database schema design, data consistency, data-driven components
- **Yash** - Documentation and training materials

## 📚 Documentation

Comprehensive documentation is available in the `docs/` folder:

- [Getting Started](./docs/getting-started.md)
- [User Interface Guide](./docs/user-interface.md)
- [Interpreting Results](./docs/interpreting-results.md)
- [System Architecture](./docs/architecture.md)
- [Bias and Fairness Concepts](./docs/bias-fairness-concepts.md)
- [How to Use BiasScope](./docs/how-to-use-biasscope.md)
- [Best Practices](./docs/best-practices.md)

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env`:
```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=biasscope
SYNTHETIC_DATA_SIZE=1000
SYNTHETIC_DATA_GENERATOR=faker
```

### Frontend Configuration

Frontend configuration is in `frontend/vite.config.js`. The API proxy is configured to forward `/api` requests to the backend.

## 📊 How It Works

1. **User Input**: User provides AI model API URL
2. **Data Generation**: System generates synthetic test data using Faker or CTGAN
3. **Model Testing**: Sends requests to user's model API and collects responses
4. **Bias Analysis**: Analyzes responses using Fairlearn, AIF360, SHAP/LIME
5. **Report Generation**: Creates visual charts and PDF reports
6. **Results Display**: Presents findings through interactive frontend

## 🧪 Test quickly with the included sample model API

If you don't have a real model API yet, run the included sample API:

```bash
cd sample_model_api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 5000
```

Then paste this URL into BiasScope:

`http://localhost:5000/predict`

## 🧪 API Endpoints

- `POST /api/analysis/start` - Start new analysis
- `GET /api/analysis/{analysis_id}` - Get analysis results
- `GET /api/analysis/{analysis_id}/report` - Download PDF report
- `GET /api/analyses` - List all analyses

See [API Documentation](./docs/api-documentation.md) for details.

## 📝 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📧 Contact

[Add contact information here]

## 🙏 Acknowledgments

- Fairlearn team for fairness assessment tools
- AIF360 team for comprehensive fairness toolkit
- SHAP and LIME teams for explainability tools
