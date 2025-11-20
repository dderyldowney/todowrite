import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Search, Filter } from 'lucide-react'

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

const fetchTasks = async (filters?: {
  layer?: string
  owner?: string
  status?: string
  search?: string
}): Promise<ToDoWriteItem[]> => {
  const params = new URLSearchParams()
  if (filters?.layer) params.append('layer', filters.layer)
  if (filters?.owner) params.append('owner', filters.owner)
  if (filters?.status) params.append('status', filters.status)
  params.append('limit', '100')

  const response = await fetch(`${API_BASE_URL}/items?${params}`)
  if (!response.ok) {
    throw new Error('Failed to fetch tasks')
  }
  const items = await response.json()

  // Filter for task-related layers and search
  return items.filter((item: ToDoWriteItem) => {
    const taskLayers = ['task', 'subtask', 'step', 'command']
    const isTaskLayer = taskLayers.includes(item.layer.toLowerCase())

    if (!isTaskLayer) return false

    if (filters?.search) {
      const searchLower = filters.search.toLowerCase()
      return (
        item.title.toLowerCase().includes(searchLower) ||
        (item.description && item.description.toLowerCase().includes(searchLower)) ||
        (item.owner && item.owner.toLowerCase().includes(searchLower))
      )
    }

    return true
  })
}

export function Tasks() {
  const [filters, setFilters] = useState({
    layer: '',
    status: '',
    owner: '',
    search: ''
  })

  const queryClient = useQueryClient()

  const { data: tasks = [], isLoading, error } = useQuery({
    queryKey: ['tasks', filters],
    queryFn: () => fetchTasks(filters),
  })

  const handleFilterChange = (key: string, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }))
  }

  const clearFilters = () => {
    setFilters({
      layer: '',
      status: '',
      owner: '',
      search: ''
    })
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-50'
      case 'in_progress': return 'text-yellow-600 bg-yellow-50'
      case 'blocked': return 'text-red-600 bg-red-50'
      case 'planned': return 'text-gray-600 bg-gray-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'text-red-600 bg-red-50'
      case 'high': return 'text-orange-600 bg-orange-50'
      case 'medium': return 'text-yellow-600 bg-yellow-50'
      case 'low': return 'text-green-600 bg-green-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Tasks</h1>
            <p className="text-gray-600 mt-2">Manage and track all your tasks and action items.</p>
          </div>
          <button className="btn btn-primary">
            <Plus className="h-4 w-4 mr-2" />
            New Task
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="card mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          <div>
            <label className="form-label">Search</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                className="form-input pl-10"
                placeholder="Search tasks..."
                value={filters.search}
                onChange={(e) => handleFilterChange('search', e.target.value)}
              />
            </div>
          </div>

          <div>
            <label className="form-label">Layer</label>
            <select
              className="form-input"
              value={filters.layer}
              onChange={(e) => handleFilterChange('layer', e.target.value)}
            >
              <option value="">All Layers</option>
              <option value="task">Task</option>
              <option value="subtask">Subtask</option>
              <option value="step">Step</option>
              <option value="command">Command</option>
            </select>
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
              <Filter className="h-4 w-4 mr-2" />
              Clear Filters
            </button>
          </div>
        </div>
      </div>

      {/* Tasks List */}
      <div className="card">
        {isLoading ? (
          <div className="flex items-center justify-center h-32">
            <div className="text-gray-500">Loading tasks...</div>
          </div>
        ) : error ? (
          <div className="flex items-center justify-center h-32">
            <div className="text-red-600">Error loading tasks</div>
          </div>
        ) : tasks.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-gray-500 mb-4">No tasks found matching your criteria.</div>
            <button className="btn btn-primary">Create Your First Task</button>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Task
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Layer
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Owner
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Severity
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Progress
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {tasks.map((task) => (
                  <tr key={task.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {task.title}
                        </div>
                        {task.description && (
                          <div className="text-sm text-gray-500 line-clamp-2">
                            {task.description}
                          </div>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-gray-900 capitalize">
                        {task.layer}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-gray-900">
                        {task.owner || 'Unassigned'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(task.status)}`}>
                        {task.status}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      {task.severity && (
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getSeverityColor(task.severity)}`}>
                          {task.severity}
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center">
                        <div className="flex-1 mr-3">
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full"
                              style={{ width: `${task.progress}%` }}
                            />
                          </div>
                        </div>
                        <span className="text-sm text-gray-900">
                          {task.progress}%
                        </span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}