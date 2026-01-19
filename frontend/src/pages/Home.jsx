import { Link } from 'react-router-dom'
import { Search, BarChart3, Shield, Zap } from 'lucide-react'

const Home = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          AI Bias & Fairness Analysis
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Automatically evaluate your AI models for bias and fairness. Just provide
          your model API endpoint, and we'll handle the rest.
        </p>
        <Link
          to="/analysis"
          className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 transition-colors"
        >
          Start Analysis
          <Search className="ml-2 h-5 w-5" />
        </Link>
      </div>

      {/* Features */}
      <div className="grid md:grid-cols-3 gap-8 mb-16">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <Zap className="h-10 w-10 text-primary-600 mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Automated Testing
          </h3>
          <p className="text-gray-600">
            Generate synthetic test data automatically and evaluate your model
            without manual input or training.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <BarChart3 className="h-10 w-10 text-primary-600 mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Comprehensive Analysis
          </h3>
          <p className="text-gray-600">
            Get detailed bias metrics using Fairlearn, AIF360, and explainability
            insights with SHAP/LIME.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <Shield className="h-10 w-10 text-primary-600 mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Visual Reports
          </h3>
          <p className="text-gray-600">
            View clear, visual insights and downloadable reports summarizing
            fairness metrics and feature influence.
          </p>
        </div>
      </div>

      {/* How It Works */}
      <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">How It Works</h2>
        <div className="space-y-4">
          <div className="flex items-start">
            <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center text-primary-600 font-semibold">
              1
            </div>
            <div className="ml-4">
              <h4 className="font-semibold text-gray-900">Provide Model API</h4>
              <p className="text-gray-600">
                Enter your AI model's API endpoint URL
              </p>
            </div>
          </div>
          <div className="flex items-start">
            <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center text-primary-600 font-semibold">
              2
            </div>
            <div className="ml-4">
              <h4 className="font-semibold text-gray-900">Automatic Data Generation</h4>
              <p className="text-gray-600">
                We generate controlled synthetic test data using Faker or CTGAN
              </p>
            </div>
          </div>
          <div className="flex items-start">
            <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center text-primary-600 font-semibold">
              3
            </div>
            <div className="ml-4">
              <h4 className="font-semibold text-gray-900">Bias Analysis</h4>
              <p className="text-gray-600">
                Your model is evaluated for bias and fairness across multiple metrics
              </p>
            </div>
          </div>
          <div className="flex items-start">
            <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center text-primary-600 font-semibold">
              4
            </div>
            <div className="ml-4">
              <h4 className="font-semibold text-gray-900">View Results</h4>
              <p className="text-gray-600">
                Access visual reports, bias scores, and explainability insights
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
