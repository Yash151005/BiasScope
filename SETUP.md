# BiasScope Setup Guide

Quick setup guide for getting BiasScope running locally.

## Prerequisites Checklist

- [ ] Node.js 18+ installed
- [ ] Python 3.9+ installed
- [ ] MongoDB installed and running
- [ ] Git installed
- [ ] Code editor (VS Code recommended)

## Step-by-Step Setup

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd BiasScope
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

### 3. Backend Setup

```bash
cd ../backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env file with your MongoDB URL
# Default: MONGODB_URL=mongodb://localhost:27017
```

### 4. MongoDB Setup

**Windows:**
```bash
# If MongoDB is installed, start the service:
net start MongoDB
# Or run mongod.exe directly
```

**macOS:**
```bash
brew services start mongodb-community
```

**Linux:**
```bash
sudo systemctl start mongod
```

**Verify MongoDB is running:**
```bash
mongo --eval "db.version()"
```

### 5. Initialize Database Indexes (Optional)

```bash
mongo biasscope database/init_indexes.js
```

### 6. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 7. Verify Installation

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Troubleshooting

### MongoDB Connection Issues

**Error**: `Failed to connect to MongoDB`

**Solutions**:
1. Verify MongoDB is running: `mongo --eval "db.version()"`
2. Check MongoDB URL in `backend/.env`
3. Verify MongoDB port (default: 27017)
4. Check firewall settings

### Python Dependencies Issues

**Error**: `ModuleNotFoundError` or installation fails

**Solutions**:
1. Ensure Python 3.9+ is installed: `python --version`
2. Use virtual environment: `python -m venv venv`
3. Upgrade pip: `pip install --upgrade pip`
4. Install dependencies one by one if needed

### Frontend Build Issues

**Error**: `npm install` fails

**Solutions**:
1. Clear npm cache: `npm cache clean --force`
2. Delete `node_modules` and `package-lock.json`
3. Reinstall: `npm install`
4. Check Node.js version: `node --version` (should be 18+)

### Port Already in Use

**Error**: `Address already in use`

**Solutions**:
1. Change port in `frontend/vite.config.js` (frontend)
2. Change port in `uvicorn` command (backend)
3. Kill process using the port:
   - Windows: `netstat -ano | findstr :8000` then `taskkill /PID <pid> /F`
   - macOS/Linux: `lsof -ti:8000 | xargs kill`

### API Connection Issues

**Error**: Frontend can't connect to backend

**Solutions**:
1. Verify backend is running on port 8000
2. Check `frontend/vite.config.js` proxy settings
3. Verify CORS settings in `backend/main.py`
4. Check browser console for errors

## Development Workflow

### Making Changes

1. **Frontend Changes**: Edit files in `frontend/src/`, changes auto-reload
2. **Backend Changes**: Edit files in `backend/app/`, server auto-reloads
3. **Database Changes**: Update schemas in `backend/app/database/schemas.py`

### Testing Your Model API

Create a simple test model API:

```python
# test_model_api.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Simple mock prediction
    prediction = 0.75 if data.get('income', 0) > 50000 else 0.45
    return jsonify({'prediction': prediction, 'result': 'approved'})

if __name__ == '__main__':
    app.run(port=5000)
```

Run it: `python test_model_api.py`

Test with BiasScope: `http://localhost:5000/predict`

## Next Steps

1. Read [Getting Started Guide](./docs/getting-started.md)
2. Review [User Interface Guide](./docs/user-interface.md)
3. Explore [API Documentation](./docs/api-documentation.md)
4. Check [Best Practices](./docs/best-practices.md)

## Team Roles

- **Rushikesh**: Frontend development lead
- **Sandip**: UI styling and responsiveness
- **Tejas**: Database schema, data consistency, data components
- **Yash**: Documentation and training materials

## Getting Help

- Check documentation in `docs/` folder
- Review error messages and logs
- Check backend logs for detailed errors
- Verify all prerequisites are installed

## Production Deployment

For production deployment:

1. Build frontend: `cd frontend && npm run build`
2. Use production ASGI server: `gunicorn main:app`
3. Set up MongoDB replica set
4. Configure environment variables
5. Set up reverse proxy (Nginx)
6. Enable HTTPS
7. Set up monitoring and logging
