import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import { Loader2, Download, AlertCircle } from 'lucide-react'
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

const Results = () => {
  const { analysisId } = useParams()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [analysisData, setAnalysisData] = useState(null)
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await axios.get(`/api/analysis/${analysisId}`)
        setAnalysisData(response.data)

        if (response.data.status === 'in_progress') {
          setProgress(response.data.progress || 0)
          // Poll for updates if still in progress
          const interval = setInterval(async () => {
            try {
              const update = await axios.get(`/api/analysis/${analysisId}`)
              setAnalysisData(update.data)
              setProgress(update.data.progress || 0)
              if (update.data.status !== 'in_progress') {
                clearInterval(interval)
              }
            } catch (err) {
              clearInterval(interval)
            }
          }, 3000)
          return () => clearInterval(interval)
        }
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load analysis results')
      } finally {
        setLoading(false)
      }
    }

    fetchResults()
  }, [analysisId])

  const handleDownloadReport = async () => {
    try {
      const response = await axios.get(`/api/analysis/${analysisId}/report`, {
        responseType: 'blob',
      })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `biasscope-report-${analysisId}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (err) {
      alert('Failed to download report')
    }
  }

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white shadow-sm rounded-lg border border-gray-200 p-8 text-center">
          <Loader2 className="animate-spin h-12 w-12 text-primary-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading analysis results...</p>
          {progress > 0 && (
            <div className="mt-4">
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div
                  className="bg-primary-600 h-2.5 rounded-full transition-all"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-500 mt-2">{progress}% complete</p>
            </div>
          )}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-red-50 border border-red-200 rounded-md p-4 flex items-start">
          <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 mr-3" />
          <p className="text-sm text-red-800">{error}</p>
        </div>
      </div>
    )
  }

  if (!analysisData) return null

  const COLORS = ['#0ea5e9', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6']

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Analysis Results</h1>
        {analysisData.status === 'completed' && (
          <button
            onClick={handleDownloadReport}
            className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors"
          >
            <Download className="h-4 w-4 mr-2" />
            Download Report
          </button>
        )}
      </div>

      {analysisData.status === 'in_progress' && (
        <div className="bg-white shadow-sm rounded-lg border border-gray-200 p-8 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Analysis in Progress
          </h2>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
              className="bg-primary-600 h-2.5 rounded-full transition-all"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <p className="text-sm text-gray-500 mt-2">{progress}% complete</p>
        </div>
      )}

      {analysisData.status === 'completed' && analysisData.results && (
        <>
          {/* Overall Bias Score */}
          <div className="bg-white shadow-sm rounded-lg border border-gray-200 p-8 mb-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Overall Bias Score
            </h2>
            <div className="text-4xl font-bold text-primary-600">
              {analysisData.results.overall_bias_score?.toFixed(2) || 'N/A'}
            </div>
            <p className="text-sm text-gray-500 mt-2">
              Lower scores indicate less bias (0 = no bias, 1 = maximum bias)
            </p>
          </div>

          {/* Fairness Metrics */}
          {analysisData.results.fairness_metrics && (
            <div className="bg-white shadow-sm rounded-lg border border-gray-200 p-8 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">
                Fairness Metrics
              </h2>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={analysisData.results.fairness_metrics}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="metric" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="value" fill="#0ea5e9" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Feature Influence */}
          {analysisData.results.feature_influence && (
            <div className="bg-white shadow-sm rounded-lg border border-gray-200 p-8 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">
                Feature Influence on Bias
              </h2>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart
                  data={analysisData.results.feature_influence}
                  layout="vertical"
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" />
                  <YAxis dataKey="feature" type="category" width={150} />
                  <Tooltip />
                  <Bar dataKey="influence" fill="#8b5cf6" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Demographic Parity */}
          {analysisData.results.demographic_parity && (
            <div className="bg-white shadow-sm rounded-lg border border-gray-200 p-8 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">
                Demographic Parity
              </h2>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={analysisData.results.demographic_parity}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) =>
                      `${name}: ${(percent * 100).toFixed(0)}%`
                    }
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {analysisData.results.demographic_parity.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default Results
