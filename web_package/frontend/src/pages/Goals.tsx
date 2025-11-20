import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Plus, Search, Target, Trophy, Zap } from 'lucide-react'

// Types for our data
interface ToDoWriteItem {
  id: number
  layer: string
  title: string
  description?: string
  status: string
  progress: number
  owner?: string
  severity?: string
  created_at: string
  updated_at: string
}

// API service
const API_BASE_URL = 'http://localhost:8000/api'

const fetchGoals = async (filters?: {
  search?: string
  status?: string
  owner?: string
}): Promise<ToDoWriteItem[]> => {
  const params = new URLSearchParams()
  if (filters?.status) params.append('status', filters.status)
  if (filters?.owner) params.append('owner', filters.owner)
  params.append('limit', '100')

  const response = await fetch(`${API_BASE_URL}/items?layer=goal&${params}`)
  if (!response.ok) {
    throw new Error('Failed to fetch goals')
  }
  const goals = await response.json()

  if (filters?.search) {
    const searchLower = filters.search.toLowerCase()
    return goals.filter((goal: ToDoWriteItem) =>
      goal.title.toLowerCase().includes(searchLower) ||
      (goal.description && goal.description.toLowerCase().includes(searchLower))
    )
  }

  return goals
}

export function Goals() {
  const [filters, setFilters] = useState({
    search: '',
    status: '',
    owner: ''
  })

  const { data: goals = [], isLoading, error } = useQuery({
    queryKey: ['goals', filters],
    queryFn: () => fetchGoals(filters),
  })

  const handleFilterChange = (key: string, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }))
  }

  const clearFilters = () => {
    setFilters({
      search: '',
      status: '',
      owner: ''
    })
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-50 border-green-200'
      case 'in_progress': return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      case 'blocked': return 'text-red-600 bg-red-50 border-red-200'
      case 'planned': return 'text-gray-600 bg-gray-50 border-gray-200'
      default: return 'text-gray-600 bg-gray-50 border-gray-200'
    }
  }

  const getGoalIcon = (progress: number) => {
    if (progress >= 80) return Trophy
    if (progress >= 40) return Target
    return Zap
  }

  const getProgressColor = (progress: number) => {
    if (progress >= 80) return 'bg-green-500'
    if (progress >= 40) return 'bg-yellow-500'
    return 'bg-gray-400'
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Goals</h1>
            <p className="text-gray-600 mt-2">Track your high-level objectives and strategic initiatives.</p>
          </div>
          <button className="btn btn-primary">
            <Plus className="h-4 w-4 mr-2" />
            New Goal
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Total Goals</p>
              <p className="text-2xl font-bold text-gray-900">{goals.length}</p>
            </div>
            <Target className="h-8 w-8 text-blue-500" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Completed</p>
              <p className="text-2xl font-bold text-green-600">
                {goals.filter(goal => goal.status === 'completed').length}
              </p>
            </div>
            <Trophy className="h-8 w-8 text-green-500" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">In Progress</p>
              <p className="text-2xl font-bold text-yellow-600">
                {goals.filter(goal => goal.status === 'in_progress').length}
              </p>
            </div>
            <Zap className="h-8 w-8 text-yellow-500" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Avg Progress</p>
              <p className="text-2xl font-bold text-gray-900">
                {goals.length > 0
                  ? Math.round(goals.reduce((sum, goal) => sum + goal.progress, 0) / goals.length)
                  : 0}%
              </p>
            </div>
            <div className="h-8 w-8 bg-gray-200 rounded-full flex items-center justify-center">
              <div
                className="h-8 w-8 bg-blue-500 rounded-full flex items-center justify-center"
                style={{
                  clipPath: `polygon(0 0, 100% 0, 100% 100%, 0 100%)`,
                  width: `${(goals.length > 0
                    ? Math.round(goals.reduce((sum, goal) => sum + goal.progress, 0) / goals.length)
                    : 0)}%`
                }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="card mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="form-label">Search Goals</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                className="form-input pl-10"
                placeholder="Search goals..."
                value={filters.search}
                onChange={(e) => handleFilterChange('search', e.target.value)}
              />
            </div>
          </div>

          <div>
            <label className="form-label">Status</label>
            <select
              className="form-input"
              value={filters.status}
              onChange={(e) => handleFilterChange('status', e.target.value)}
            >
              <option value="">All Status</option>
              <option value="planned">Planned</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
              <option value="blocked">Blocked</option>
            </select>
          </div>

          <div>
            <label className="form-label">Owner</label>
            <input
              type="text"
              className="form-input"
              placeholder="Filter by owner..."
              value={filters.owner}
              onChange={(e) => handleFilterChange('owner', e.target.value)}
            />
          </div>

          <div className="flex items-end">
            <button
              onClick={clearFilters}
              className="btn btn-outline w-full"
            >
              Clear Filters
            </button>
          </div>
        </div>
      </div>

      {/* Goals Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {isLoading ? (
          Array.from({ length: 6 }).map((_, index) => (
            <div key={index} className="card">
              <div className="animate-pulse">
                <div className="h-6 bg-gray-200 rounded mb-4"></div>
                <div className="h-4 bg-gray-200 rounded mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              </div>
            </div>
          ))
        ) : error ? (
          <div className="col-span-full text-center py-8">
            <div className="text-red-600">Error loading goals</div>
          </div>
        ) : goals.length === 0 ? (
          <div className="col-span-full text-center py-8">
            <Target className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <div className="text-gray-500 mb-4">No goals found matching your criteria.</div>
            <button className="btn btn-primary">Create Your First Goal</button>
          </div>
        ) : (
          goals.map((goal) => {
            const Icon = getGoalIcon(goal.progress)
            return (
              <div key={goal.id} className="card hover:shadow-md transition-shadow cursor-pointer">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center">
                    <Icon className="h-6 w-6 text-blue-600 mr-3" />
                    <span className={`px-3 py-1 text-xs font-semibold rounded-full border ${getStatusColor(goal.status)}`}>
                      {goal.status}
                    </span>
                  </div>
                  {goal.severity && (
                    <span className="text-xs text-gray-500 capitalize">{goal.severity}</span>
                  )}
                </div>

                <h3 className="text-lg font-semibold text-gray-900 mb-2">{goal.title}</h3>

                {goal.description && (
                  <p className="text-gray-600 text-sm mb-4 line-clamp-3">{goal.description}</p>
                )}

                <div className="mb-4">
                  <div className="flex items-center justify-between text-sm mb-1">
                    <span className="text-gray-500">Progress</span>
                    <span className="font-medium">{goal.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(goal.progress)}`}
                      style={{ width: `${goal.progress}%` }}
                    />
                  </div>
                </div>

                <div className="flex items-center justify-between text-sm text-gray-500">
                  <span>{goal.owner || 'Unassigned'}</span>
                  <span>{new Date(goal.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            )
          })
        )}
      </div>
    </div>
  )
}