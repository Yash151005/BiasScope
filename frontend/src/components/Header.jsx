import { Link } from 'react-router-dom'
import { Scale } from 'lucide-react'

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <Scale className="h-8 w-8 text-primary-600" />
            <span className="text-xl font-bold text-gray-900">BiasScope</span>
          </Link>
          <nav className="flex space-x-4">
            <Link
              to="/"
              className="text-gray-600 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Home
            </Link>
            <Link
              to="/analysis"
              className="text-gray-600 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              New Analysis
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header
