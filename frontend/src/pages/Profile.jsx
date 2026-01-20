import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { Loader2, AlertCircle, FileText, User, Briefcase, Calendar, Edit2, Save, X, CheckCircle, Upload, Camera } from 'lucide-react'

const Profile = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [updating, setUpdating] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [user, setUser] = useState(null)
  const [analyses, setAnalyses] = useState([])
  const [isEditing, setIsEditing] = useState(false)
  const [editData, setEditData] = useState({
    full_name: '',
    email: '',
    profession: '',
  })
  const [profilePhotoFile, setProfilePhotoFile] = useState(null)
  const [profilePhotoPreview, setProfilePhotoPreview] = useState(null)

  const professions = [
    'Student',
    'Data Scientist',
    'Machine Learning Engineer',
    'Software Engineer',
    'Product Manager',
    'AI Researcher',
    'Data Engineer',
    'DevOps Engineer',
    'Business Analyst',
    'Consultant',
    'Compliance Officer',
    'Other'
  ]

  useEffect(() => {
    fetchUserData()
  }, [])

  const fetchUserData = async () => {
    try {
      const userId = localStorage.getItem('userId')
      if (!userId) {
        navigate('/login')
        return
      }

      const response = await axios.get(`/api/auth/user/${userId}`)
      setUser(response.data.data)
      setEditData({
        full_name: response.data.data.full_name,
        email: response.data.data.email,
        profession: response.data.data.profession,
      })
      if (response.data.data.profile_photo) {
        setProfilePhotoPreview(response.data.data.profile_photo)
      }

      // Fetch user's analysis history
      const analysisResponse = await axios.get(`/api/auth/user/${userId}/analyses`)
      setAnalyses(analysisResponse.data.analyses)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load profile')
    } finally {
      setLoading(false)
    }
  }

  const handleEditChange = (e) => {
    const { name, value } = e.target
    setEditData(prev => ({
      ...prev,
      [name]: value
    }))
    setError('')
  }

  const handlePhotoChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setProfilePhotoFile(file)
      // Create preview
      const reader = new FileReader()
      reader.onloadend = () => {
        setProfilePhotoPreview(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSaveProfile = async () => {
    if (!editData.full_name.trim()) {
      setError('Full name is required')
      return
    }
    if (!editData.email.trim()) {
      setError('Email is required')
      return
    }
    if (!editData.profession) {
      setError('Profession is required')
      return
    }

    setUpdating(true)
    setError('')

    try {
      const userId = localStorage.getItem('userId')
      const updateData = {
        full_name: editData.full_name,
        email: editData.email,
        profession: editData.profession
      }

      // Include profile photo if one was selected
      if (profilePhotoPreview && profilePhotoPreview.startsWith('data:')) {
        updateData.profile_photo = profilePhotoPreview
      }

      const response = await axios.post(`/api/auth/update-profile?user_id=${userId}`, updateData)

      if (response.data.success) {
        setUser(response.data.data)
        setSuccess('Profile updated successfully!')
        setIsEditing(false)
        setProfilePhotoFile(null)

        // Update localStorage
        const updatedUser = {
          ...JSON.parse(localStorage.getItem('user')),
          full_name: response.data.data.full_name,
          email: response.data.data.email,
          profession: response.data.data.profession,
          profile_photo: response.data.data.profile_photo
        }
        localStorage.setItem('user', JSON.stringify(updatedUser))

        setTimeout(() => {
          setSuccess('')
        }, 3000)
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update profile')
    } finally {
      setUpdating(false)
    }
  }

  const handleCancel = () => {
    setIsEditing(false)
    setEditData({
      full_name: user.full_name,
      email: user.email,
      profession: user.profession,
    })
    setProfilePhotoFile(null)
    setProfilePhotoPreview(user.profile_photo || null)
    setError('')
  }

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white shadow-sm rounded-lg border border-gray-200 p-8 text-center">
          <Loader2 className="animate-spin h-12 w-12 text-primary-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading profile...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
            <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 mr-3" />
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        {success && (
          <div className="mb-6 bg-green-50 border border-green-200 rounded-lg p-4 flex items-start">
            <CheckCircle className="h-5 w-5 text-green-600 mt-0.5 mr-3" />
            <p className="text-sm text-green-800">{success}</p>
          </div>
        )}

        {/* User Profile Card */}
        {user && (
          <div className="bg-white rounded-lg shadow-md p-8 mb-8">
            <div className="flex items-start justify-between mb-6">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">My Profile</h1>
                <p className="text-gray-600">Manage your account and view analysis history</p>
              </div>
              <div className="flex items-center space-x-3">
                {!isEditing && (
                  <button
                    onClick={() => setIsEditing(true)}
                    className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2"
                  >
                    <Edit2 className="h-4 w-4" />
                    <span>Edit Profile</span>
                  </button>
                )}
                <div className="bg-primary-100 rounded-full p-4">
                  <User className="h-8 w-8 text-primary-600" />
                </div>
              </div>
            </div>

            {isEditing ? (
              // Edit Mode
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Full Name
                    </label>
                    <input
                      type="text"
                      name="full_name"
                      value={editData.full_name}
                      onChange={handleEditChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email Address
                    </label>
                    <input
                      type="email"
                      name="email"
                      value={editData.email}
                      onChange={handleEditChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Profession
                  </label>
                  <select
                    name="profession"
                    value={editData.profession}
                    onChange={handleEditChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition appearance-none bg-white"
                  >
                    <option value="">Select your profession</option>
                    {professions.map(prof => (
                      <option key={prof} value={prof}>{prof}</option>
                    ))}
                  </select>
                </div>

                {/* Profile Photo Upload */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Profile Photo
                  </label>
                  <div className="flex items-center space-x-4">
                    {profilePhotoPreview ? (
                      <img
                        src={profilePhotoPreview}
                        alt="Profile preview"
                        className="w-16 h-16 rounded-full object-cover border-2 border-primary-500"
                      />
                    ) : (
                      <div className="w-16 h-16 rounded-full bg-primary-100 flex items-center justify-center border-2 border-dashed border-primary-300">
                        <Camera className="h-6 w-6 text-primary-600" />
                      </div>
                    )}
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handlePhotoChange}
                      className="hidden"
                      id="photo-input"
                    />
                    <label
                      htmlFor="photo-input"
                      className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2 cursor-pointer"
                    >
                      <Upload className="h-4 w-4" />
                      <span>Upload Photo</span>
                    </label>
                  </div>
                  {profilePhotoFile && (
                    <p className="text-sm text-gray-600 mt-2">File selected: {profilePhotoFile.name}</p>
                  )}
                </div>

                {/* Save/Cancel Buttons */}
                <div className="flex space-x-3 pt-4">
                  <button
                    onClick={handleSaveProfile}
                    disabled={updating}
                    className="bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white px-6 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2"
                  >
                    {updating ? (
                      <>
                        <Loader2 className="h-4 w-4 animate-spin" />
                        <span>Saving...</span>
                      </>
                    ) : (
                      <>
                        <Save className="h-4 w-4" />
                        <span>Save Changes</span>
                      </>
                    )}
                  </button>
                  <button
                    onClick={handleCancel}
                    disabled={updating}
                    className="bg-gray-300 hover:bg-gray-400 disabled:bg-gray-200 text-gray-800 px-6 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2"
                  >
                    <X className="h-4 w-4" />
                    <span>Cancel</span>
                  </button>
                </div>
              </div>
            ) : (
              // View Mode
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <p className="text-sm text-gray-600">Full Name</p>
                    <p className="text-lg font-semibold text-gray-900">{user.full_name}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Email Address</p>
                    <p className="text-lg font-semibold text-gray-900">{user.email}</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <p className="text-sm text-gray-600">Username</p>
                    <p className="text-lg font-semibold text-gray-900">@{user.username}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Profession</p>
                    <div className="flex items-center space-x-2 mt-1">
                      <Briefcase className="h-5 w-5 text-primary-600" />
                      <p className="text-lg font-semibold text-gray-900">{user.profession}</p>
                    </div>
                  </div>
                </div>

                {user.created_at && (
                  <div className="pt-4 border-t border-gray-200">
                    <div className="flex items-center space-x-2 text-gray-600">
                      <Calendar className="h-5 w-5" />
                      <p className="text-sm">
                        Member since {new Date(user.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Analysis History */}
        <div className="bg-white rounded-lg shadow-md p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <FileText className="h-6 w-6 mr-2 text-primary-600" />
            Your Analysis History
          </h2>

          {analyses.length === 0 ? (
            <div className="text-center py-12">
              <FileText className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-600">No analyses yet</p>
              <p className="text-gray-500 text-sm mt-2">
                Start a new analysis to see your history here
              </p>
              <button
                onClick={() => navigate('/analysis')}
                className="mt-4 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
              >
                Start New Analysis
              </button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="border-b border-gray-200">
                  <tr>
                    <th className="text-left py-3 px-4 font-semibold text-gray-900">Analysis ID</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-900">Model URL</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-900">Date</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-900">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {analyses.map((analysis, index) => (
                    <tr key={index} className="border-b border-gray-200 hover:bg-gray-50 transition">
                      <td className="py-3 px-4 text-sm text-gray-900 font-mono">
                        {analysis.analysis_id.substring(0, 8)}...
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-600 truncate max-w-xs">
                        {analysis.model_url}
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-600">
                        {new Date(analysis.saved_at).toLocaleDateString()}
                      </td>
                      <td className="py-3 px-4">
                        <button
                          onClick={() => navigate(`/results/${analysis.analysis_id}`)}
                          className="text-primary-600 hover:text-primary-700 font-medium text-sm transition-colors"
                        >
                          View Report
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Profile
