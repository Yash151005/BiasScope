import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { Loader2, AlertCircle, CheckCircle } from 'lucide-react'

const Analysis = () => {
  const [apiUrl, setApiUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)

    try {
      const response = await axios.post('/api/analysis/start', {
        model_url: apiUrl,
      })

      if (response.data.analysis_id) {
        setSuccess('Analysis started successfully!')
        setTimeout(() => {
          navigate(`/results/${response.data.analysis_id}`)
        }, 1500)
      }
    } catch (err) {
      setError(
        err.response?.data?.detail || 'Failed to start analysis. Please try again.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="bg-white shadow-sm rounded-lg border border-gray-200 p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Start New Analysis
        </h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label
              htmlFor="apiUrl"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              AI Model API URL
            </label>
            <input
              type="text"
              id="apiUrl"
              value={apiUrl}
              onChange={(e) => setApiUrl(e.target.value)}
              placeholder="https://your-model-api.com/predict  (or: http://..., localhost:5000/predict)"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
              disabled={loading}
            />
            <p className="mt-2 text-sm text-gray-500">
              Enter the endpoint URL where your AI model accepts prediction requests
            </p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-md p-4 flex items-start">
              <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 mr-3" />
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          {success && (
            <div className="bg-green-50 border border-green-200 rounded-md p-4 flex items-start">
              <CheckCircle className="h-5 w-5 text-green-600 mt-0.5 mr-3" />
              <p className="text-sm text-green-800">{success}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={loading || !apiUrl}
            className="w-full flex justify-center items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin h-5 w-5 mr-2" />
                Starting Analysis...
              </>
            ) : (
              'Start Analysis'
            )}
          </button>
        </form>
      </div>
    </div>
  )
}

export default Analysis
