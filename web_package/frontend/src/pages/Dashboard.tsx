import { useQuery } from '@tanstack/react-query'
import { Target, CheckSquare, Calendar, TrendingUp, Plus } from 'lucide-react'

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

interface Stats {
  goals: number
  tasks: number
  concepts: number
  contexts: number
  constraints: number
  requirements: number
  acceptance_criteria: number
  interface_contracts: number
  phases: number
  steps: number
  sub_tasks: number
  commands: number
  labels: number
  total: number
}

// API service
const API_BASE_URL = 'http://localhost:8000/api'

const fetchItems = async (): Promise<ToDoWriteItem[]> => {
  const response = await fetch(`${API_BASE_URL}/items?limit=20`)
  if (!response.ok) {
    throw new Error('Failed to fetch items')
  }
  return response.json()
}

const fetchStats = async (): Promise<Stats> => {
  const response = await fetch(`${API_BASE_URL}/stats`)
  if (!response.ok) {
    throw new Error('Failed to fetch stats')
  }
  return response.json()
}

export function Dashboard() {
  const { data: items = [], isLoading: itemsLoading } = useQuery({
    queryKey: ['items'],
    queryFn: fetchItems,
  })

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['stats'],
    queryFn: fetchStats,
  })

  const recentItems = items.slice(0, 5)

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-600 mt-2">Welcome back! Here's your task management overview.</p>
          </div>
          <button className="btn btn-primary">
            <Plus className="h-4 w-4 mr-2" />
            New Task
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-blue-100 rounded-lg p-3">
              <Target className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-500">Goals</h3>
              <div className="text-2xl font-bold text-gray-900">
                {statsLoading ? '...' : stats?.goals || 0}
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-yellow-100 rounded-lg p-3">
              <CheckSquare className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-500">Tasks</h3>
              <div className="text-2xl font-bold text-gray-900">
                {statsLoading ? '...' : stats?.tasks || 0}
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-green-100 rounded-lg p-3">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-500">In Progress</h3>
              <div className="text-2xl font-bold text-gray-900">
                {itemsLoading ? '...' : items.filter(item => item.status === 'in_progress').length}
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-purple-100 rounded-lg p-3">
              <Calendar className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-500">Total Items</h3>
              <div className="text-2xl font-bold text-gray-900">
                {statsLoading ? '...' : stats?.total || 0}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Items */}
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Recent Items</h2>

            {itemsLoading ? (
              <div className="flex items-center justify-center h-32">
                <div className="text-gray-500">Loading items...</div>
              </div>
            ) : recentItems.length === 0 ? (
              <div className="text-center py-8">
                <div className="text-gray-500 mb-4">No items yet. Create your first task!</div>
                <button className="btn btn-primary">Create Task</button>
              </div>
            ) : (
              <div className="space-y-4">
                {recentItems.map((item) => (
                  <div key={item.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <span className={`status-badge status-${item.status}`}>
                          {item.status}
                        </span>
                        <h3 className="text-lg font-medium text-gray-900">{item.title}</h3>
                      </div>
                      <div className="mt-1 flex items-center space-x-4 text-sm text-gray-500">
                        <span className="capitalize">{item.layer}</span>
                        {item.owner && <span>Owner: {item.owner}</span>}
                        <span>Progress: {item.progress}%</span>
                      </div>
                      {item.description && (
                        <p className="mt-2 text-gray-600 line-clamp-2">{item.description}</p>
                      )}
                    </div>
                    <div className="ml-4">
                      {item.severity && (
                        <span className={`priority-${item.severity} text-xs px-2 py-1 rounded`}>
                          {item.severity}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Quick Stats */}
        <div className="space-y-6">
          {/* Status Breakdown */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Status Breakdown</h3>
            {!itemsLoading && items.length > 0 && (
              <div className="space-y-3">
                {['planned', 'in_progress', 'completed', 'blocked'].map(status => {
                  const count = items.filter(item => item.status === status).length
                  const percentage = (count / items.length) * 100
                  return (
                    <div key={status} className="flex items-center justify-between">
                      <div className="flex items-center">
                        <span className={`status-badge status-${status} mr-3`}>
                          {status}
                        </span>
                        <span className="text-sm text-gray-600">{count}</span>
                      </div>
                      <div className="w-24 bg-gray-200 rounded-full h-2">
                        <div
                          className={`bg-${status === 'completed' ? 'green' : status === 'in_progress' ? 'yellow' : status === 'blocked' ? 'red' : 'gray'}-500 h-2 rounded-full`}
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>

          {/* Quick Actions */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <button className="w-full btn btn-outline justify-start">
                <Plus className="h-4 w-4 mr-2" />
                Create New Goal
              </button>
              <button className="w-full btn btn-outline justify-start">
                <Plus className="h-4 w-4 mr-2" />
                Create New Task
              </button>
              <button className="w-full btn btn-outline justify-start">
                <Calendar className="h-4 w-4 mr-2" />
                View Calendar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}