import { useState, useEffect } from 'react'
import { ChevronLeft, ChevronRight, Plus } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'

// Types for our data
interface ToDoWriteItem {
  id: number
  layer: string
  title: string
  description?: string
  status: string
  progress: number
  created_at: string
  updated_at: string
}

// API service
const API_BASE_URL = 'http://localhost:8000/api'

const fetchItems = async (): Promise<ToDoWriteItem[]> => {
  const response = await fetch(`${API_BASE_URL}/items?limit=100`)
  if (!response.ok) {
    throw new Error('Failed to fetch items')
  }
  return response.json()
}

export function Calendar() {
  const [currentDate, setCurrentDate] = useState(new Date())

  const { data: items = [], isLoading, error } = useQuery({
    queryKey: ['items'],
    queryFn: fetchItems,
  })

  // Calendar navigation
  const navigateMonth = (direction: 'prev' | 'next') => {
    setCurrentDate(prev => {
      const newDate = new Date(prev)
      if (direction === 'prev') {
        newDate.setMonth(newDate.getMonth() - 1)
      } else {
        newDate.setMonth(newDate.getMonth() + 1)
      }
      return newDate
    })
  }

  // Get days in month
  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear()
    const month = date.getMonth()
    const firstDay = new Date(year, month, 1)
    const lastDay = new Date(year, month + 1, 0)
    const daysInMonth = lastDay.getDate()
    const startingDayOfWeek = firstDay.getDay()

    const days = []

    // Add empty cells for days before month starts
    for (let i = 0; i < startingDayOfWeek; i++) {
      days.push(null)
    }

    // Add days of month
    for (let i = 1; i <= daysInMonth; i++) {
      days.push(i)
    }

    return days
  }

  // Get tasks for a specific day
  const getTasksForDay = (day: number | null) => {
    if (!day || !items.length) return []

    const dateStr = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`

    return items.filter(item => {
      // For now, show all items as if they're due today
      // In a real app, you'd have due_date fields
      return item.layer !== 'label' // Don't show labels in calendar
    }).slice(0, 3) // Limit to 3 items per day for UI
  }

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ]

  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

  const today = new Date()
  const isToday = (day: number | null) => {
    return day === today.getDate() &&
           currentDate.getMonth() === today.getMonth() &&
           currentDate.getFullYear() === today.getFullYear()
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg text-gray-500">Loading calendar...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg text-red-600">Error loading calendar data</div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Calendar</h1>
          <button className="btn btn-primary">
            <Plus className="h-4 w-4 mr-2" />
            New Task
          </button>
        </div>

        {/* Month navigation */}
        <div className="flex items-center justify-between">
          <button
            onClick={() => navigateMonth('prev')}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ChevronLeft className="h-5 w-5" />
          </button>

          <h2 className="text-xl font-semibold text-gray-900">
            {monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}
          </h2>

          <button
            onClick={() => navigateMonth('next')}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ChevronRight className="h-5 w-5" />
          </button>
        </div>
      </div>

      {/* Calendar Grid */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        {/* Day headers */}
        <div className="grid grid-cols-7 bg-gray-50">
          {dayNames.map(day => (
            <div key={day} className="p-3 text-center text-sm font-medium text-gray-700 border-r border-gray-200 last:border-r-0">
              {day}
            </div>
          ))}
        </div>

        {/* Calendar days */}
        <div className="calendar-grid">
          {getDaysInMonth(currentDate).map((day, index) => {
            const dayTasks = getTasksForDay(day)

            return (
              <div
                key={index}
                className={`calendar-day ${isToday(day) ? 'today' : ''} ${!day ? 'bg-gray-50' : ''}`}
              >
                {day && (
                  <>
                    <div className="calendar-day-number">{day}</div>
                    <div className="space-y-1">
                      {dayTasks.map(task => (
                        <div
                          key={task.id}
                          className={`task-item ${task.layer} priority-${task.severity || 'medium'}`}
                          title={task.title}
                        >
                          {task.title}
                        </div>
                      ))}
                    </div>
                  </>
                )}
              </div>
            )
          })}
        </div>
      </div>

      {/* Summary Stats */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Total Items</h3>
          <div className="text-3xl font-bold text-blue-600">{items.length}</div>
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">In Progress</h3>
          <div className="text-3xl font-bold text-yellow-600">
            {items.filter(item => item.status === 'in_progress').length}
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Completed</h3>
          <div className="text-3xl font-bold text-green-600">
            {items.filter(item => item.status === 'completed').length}
          </div>
        </div>
      </div>
    </div>
  )
}