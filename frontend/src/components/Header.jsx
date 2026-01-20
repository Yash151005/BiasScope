import { Link, useLocation } from 'react-router-dom'
import { Scale, LogOut } from 'lucide-react'
import { useState, useEffect } from 'react'

const Header = () => {
  const [user, setUser] = useState(null)

  const location = useLocation()

  useEffect(() => {
    // Re-check localStorage when route changes (e.g. after login)
    const userData = localStorage.getItem('user')
    if (userData) {
      setUser(JSON.parse(userData))
    } else {
      setUser(null)
    }
  }, [location])

  const handleLogout = () => {
    localStorage.removeItem('user')
    localStorage.removeItem('userId')
    setUser(null)
    window.location.href = '/'
  }

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <Scale className="h-8 w-8 text-primary-600" />
            <span className="text-xl font-bold text-gray-900">BiasScope</span>
          </Link>
          <nav className="flex space-x-2 items-center">
            <Link
              to="/"
              className="text-gray-600 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Home
            </Link>
            {user && (
              <Link
                to="/analysis"
                className="text-gray-600 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                New Analysis
              </Link>
            )}
            <Link
              to="/contact"
              className="text-gray-600 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Contact
            </Link>

            {user ? (
              <div className="flex items-center space-x-3 ml-4 pl-4 border-l border-gray-200">
                <div className="flex flex-col items-end">
                  <p className="text-sm font-medium text-gray-900">{user.username}</p>
                  <p className="text-xs text-gray-500">{user.profession}</p>
                </div>
                {user.profile_photo ? (
                  <img
                    src={user.profile_photo}
                    alt={user.username}
                    className="w-8 h-8 rounded-full object-cover border border-primary-200"
                  />
                ) : (
                  <div className="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center text-white text-sm font-bold">
                    {user && user.username && typeof user.username === 'string' && user.username.length > 0
                      ? user.username.charAt(0).toUpperCase()
                      : '?'}
                  </div>
                )}
                <Link
                  to="/profile"
                  className="text-gray-600 hover:text-primary-600 p-2 rounded-md text-sm transition-colors"
                  title="Profile"
                >
                  <span className="text-sm font-medium">Profile</span>
                </Link>
                <button
                  onClick={handleLogout}
                  className="text-gray-600 hover:text-red-600 p-2 rounded-md text-sm transition-colors"
                  title="Logout"
                >
                  <LogOut className="h-5 w-5" />
                </button>
              </div>
            ) : (
              <div className="flex space-x-2 ml-4 pl-4 border-l border-gray-200">
                <Link
                  to="/login"
                  className="text-gray-600 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Sign In
                </Link>
                <Link
                  to="/signup"
                  className="bg-primary-600 hover:bg-primary-700 text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header
