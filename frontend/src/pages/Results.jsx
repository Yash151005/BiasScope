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
  ComposedChart,
  Line,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
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

      // Save analysis to user account if logged in
      const userId = localStorage.getItem('userId')
      if (userId && analysisData) {
        try {
          const reportUrl = `/results/${analysisId}`
          await axios.post('/api/auth/save-analysis', null, {
            params: {
              user_id: userId,
              analysis_id: analysisId,
              model_url: analysisData.model_url,
              report_url: reportUrl
            }
          })
        } catch (err) {
          console.log('Note: Could not save to account, but report downloaded')
        }
      }
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

  // Function to generate recommendation based on bias score
  const getRecommendation = (score) => {
    if (score < 0.3) {
      return {
        level: 'Low Bias',
        status: 'Safe to Use',
        color: 'green',
        icon: '✓',
        description: 'This model shows minimal bias and is generally safe to deploy.',
        actions: [
          'Continue current practices',
          'Implement regular monitoring',
          'Document fair practices for compliance',
          'Set up periodic bias checks'
        ]
      }
    } else if (score < 0.7) {
      return {
        level: 'Moderate Bias',
        status: 'Use With Caution',
        color: 'yellow',
        icon: '⚠',
        description: 'This model shows some bias. Review and mitigation recommended before production use.',
        actions: [
          'Review feature influence analysis',
          'Check demographic parity metrics',
          'Consider bias mitigation techniques',
          'Increase monitoring frequency'
        ]
      }
    } else {
      return {
        level: 'High Bias',
        status: 'Do Not Use',
        color: 'red',
        icon: '✕',
        description: 'This model exhibits significant bias and requires substantial improvements before deployment.',
        actions: [
          'Immediate review required',
          'Identify problematic features',
          'Implement bias mitigation measures',
          'Retest after modifications',
          'Consider alternative models'
        ]
      }
    }
  }

  const recommendation = getRecommendation(analysisData.results?.overall_bias_score || 0)

  // Convert score to percentage (0-1 scale to 0-100%)
  const biasPercentage = ((analysisData.results?.overall_bias_score || 0) * 100).toFixed(1)
  const fairnessPercentage = (100 - parseFloat(biasPercentage)).toFixed(1)

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
            <h2 className="text-xl font-semibold text-gray-900 mb-6">
              Overall Bias Score & Assessment
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Bias Score Display */}
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <div className="text-5xl font-bold text-primary-600 mb-2">
                      {analysisData.results.overall_bias_score?.toFixed(2) || 'N/A'}
                    </div>
                    <p className="text-sm text-gray-600 mb-4">
                      Lower scores indicate less bias (0 = no bias, 1 = maximum bias)
                    </p>
                  </div>
                </div>
                
                {/* Bias vs Fairness Percentages */}
                <div className="mt-6 space-y-3">
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className="text-sm font-medium text-red-700">Bias Level</span>
                      <span className="text-sm font-semibold text-red-600">{biasPercentage}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2.5">
                      <div
                        className="bg-red-600 h-2.5 rounded-full transition-all"
                        style={{ width: `${biasPercentage}%` }}
                      ></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className="text-sm font-medium text-green-700">Fairness Level</span>
                      <span className="text-sm font-semibold text-green-600">{fairnessPercentage}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2.5">
                      <div
                        className="bg-green-600 h-2.5 rounded-full transition-all"
                        style={{ width: `${fairnessPercentage}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recommendation Card */}
              <div
                className={`border-l-4 rounded-lg p-6 bg-${recommendation.color}-50 border-${recommendation.color}-400`}
                style={{
                  borderColor: recommendation.color === 'green' ? '#10b981' : recommendation.color === 'yellow' ? '#f59e0b' : '#ef4444',
                  backgroundColor: recommendation.color === 'green' ? '#ecfdf5' : recommendation.color === 'yellow' ? '#fffbeb' : '#fef2f2'
                }}
              >
                <div className="flex items-start mb-3">
                  <div
                    className="text-2xl mr-3"
                    style={{
                      color: recommendation.color === 'green' ? '#10b981' : recommendation.color === 'yellow' ? '#f59e0b' : '#ef4444'
                    }}
                  >
                    {recommendation.icon}
                  </div>
                  <div>
                    <h3
                      className="text-lg font-bold"
                      style={{
                        color: recommendation.color === 'green' ? '#047857' : recommendation.color === 'yellow' ? '#b45309' : '#991b1b'
                      }}
                    >
                      {recommendation.level}
                    </h3>
                    <p
                      className="text-sm font-semibold"
                      style={{
                        color: recommendation.color === 'green' ? '#059669' : recommendation.color === 'yellow' ? '#d97706' : '#dc2626'
                      }}
                    >
                      {recommendation.status}
                    </p>
                  </div>
                </div>
                
                <p
                  className="text-sm mb-4 font-medium"
                  style={{
                    color: recommendation.color === 'green' ? '#047857' : recommendation.color === 'yellow' ? '#b45309' : '#991b1b'
                  }}
                >
                  {recommendation.description}
                </p>

                <div className="mt-4">
                  <p
                    className="text-xs font-bold mb-2"
                    style={{
                      color: recommendation.color === 'green' ? '#047857' : recommendation.color === 'yellow' ? '#b45309' : '#991b1b'
                    }}
                  >
                    RECOMMENDED ACTIONS:
                  </p>
                  <ul className="space-y-1">
                    {recommendation.actions.map((action, index) => (
                      <li
                        key={index}
                        className="text-xs flex items-start"
                        style={{
                          color: recommendation.color === 'green' ? '#065f46' : recommendation.color === 'yellow' ? '#92400e' : '#7c2d12'
                        }}
                      >
                        <span className="mr-2">•</span>
                        <span>{action}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* Bias Scale Visualization */}
          <div className="bg-white shadow-sm rounded-lg border border-gray-200 p-8 mb-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Bias Scale Assessment</h2>
            
            {/* Visual Scale */}
            <div className="mb-8">
              <div className="relative h-12 bg-gradient-to-r from-green-500 via-yellow-500 to-red-500 rounded-lg overflow-hidden shadow-md">
                {/* Indicator */}
                <div
                  className="absolute top-0 bottom-0 w-1 bg-gray-900 shadow-lg transition-all"
                  style={{ left: `${biasPercentage}%` }}
                >
                  <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 text-sm font-bold text-gray-800 bg-white px-2 py-1 rounded shadow-md border border-gray-300 whitespace-nowrap">
                    {analysisData.results.overall_bias_score?.toFixed(2)}
                  </div>
                  <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 text-xs font-semibold text-gray-600">
                    {biasPercentage}%
                  </div>
                </div>
              </div>
              
              {/* Scale Labels */}
              <div className="flex justify-between mt-12 text-xs font-semibold text-gray-600">
                <span>No Bias (0.0)</span>
                <span>Moderate (0.5)</span>
                <span>Maximum (1.0)</span>
              </div>

              {/* Zone Descriptions */}
              <div className="mt-8 grid grid-cols-3 gap-4">
                <div className="text-center p-4 bg-green-50 rounded-lg border border-green-200">
                  <p className="text-sm font-semibold text-green-800">✓ Safe Zone</p>
                  <p className="text-xs text-green-700 mt-1">0.0 - 0.3</p>
                  <p className="text-xs text-green-600 mt-2">Minimal bias detected</p>
                </div>
                <div className="text-center p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                  <p className="text-sm font-semibold text-yellow-800">⚠ Caution Zone</p>
                  <p className="text-xs text-yellow-700 mt-1">0.3 - 0.7</p>
                  <p className="text-xs text-yellow-600 mt-2">Moderate bias present</p>
                </div>
                <div className="text-center p-4 bg-red-50 rounded-lg border border-red-200">
                  <p className="text-sm font-semibold text-red-800">✕ Danger Zone</p>
                  <p className="text-xs text-red-700 mt-1">0.7 - 1.0</p>
                  <p className="text-xs text-red-600 mt-2">Significant bias detected</p>
                </div>
              </div>
            </div>
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
