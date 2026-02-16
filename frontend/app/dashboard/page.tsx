'use client'

import { useState, useEffect } from 'react'
import { TrendingUp, Globe, Zap, Clock, Users, BarChart3 } from 'lucide-react'
import Link from 'next/link'

export default function Dashboard() {
  const [websites, setWebsites] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchWebsites()
    const interval = setInterval(fetchWebsites, 30000)
    return () => clearInterval(interval)
  }, [])

  const fetchWebsites = async () => {
    try {
      const response = await fetch('/api/websites')
      if (!response.ok) throw new Error('Failed to fetch websites')
      const data = await response.json()
      setWebsites(data)
      setLoading(false)
    } catch (err) {
      setLoading(false)
    }
  }

  const getStats = () => {
    const total = websites.length
    const up = websites.filter(w => w.status === 'up').length
    const down = websites.filter(w => w.status === 'down').length
    const responseTimes = websites.filter(w => w.response_time > 0).map(w => w.response_time)
    const avgResponseTime = responseTimes.length > 0 ? responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length : 0

    return {
      total,
      up,
      down,
      avgResponseTime: Math.round(avgResponseTime * 100) / 100
    }
  }

  const stats = getStats()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Globe className="w-12 h-12 mx-auto mb-4 text-blue-600 animate-spin" />
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <TrendingUp className="w-8 h-8 mr-3 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
            </div>
            <nav className="flex space-x-4">
              <Link href="/" className="text-gray-600 hover:text-gray-900">
                <Globe className="w-6 h-6" />
              </Link>
              <Link href="/settings/telegram" className="text-gray-600 hover:text-gray-900">
                <Users className="w-6 h-6" />
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Website Monitoring Dashboard</h2>
          <p className="text-gray-600 mt-1">Real-time insights and analytics</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <Globe className="w-8 h-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-sm text-gray-600">Total Websites</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <CheckCircle className="w-8 h-8 text-green-600" />
              <div className="ml-4">
                <p className="text-sm text-gray-600">Up</p>
                <p className="text-2xl font-bold text-green-600">{stats.up}</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <XCircle className="w-8 h-8 text-red-600" />
              <div className="ml-4">
                <p className="text-sm text-gray-600">Down</p>
                <p className="text-2xl font-bold text-red-600">{stats.down}</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <Zap className="w-8 h-8 text-purple-600" />
              <div className="ml-4">
                <p className="text-sm text-gray-600">Avg Response Time</p>
                <p className="text-2xl font-bold text-gray-900">{stats.avgResponseTime}ms</p>
              </div>
            </div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold mb-4">Response Time Distribution</h3>
            <div className="space-y-4">
              {websites.map((website) => (
                <div key={website.id} className="flex justify-between items-center py-2">
                  <span className="text-sm font-medium text-gray-700">{website.name}</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-32 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${website.response_time > 0 ? (website.response_time / 1000) * 100 : 0}%` }}
                      />
                    </div>
                    <span className="text-sm text-gray-600">{website.response_time > 0 ? `${website.response_time}ms` : '—'}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold mb-4">Status Overview</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">Up</span>
                <div className="flex items-center space-x-2">
                  <div className="w-20 bg-green-100 rounded-full h-2">
                    <div
                      className="bg-green-600 h-2 rounded-full"
                      style={{ width: `${(stats.up / stats.total) * 100}%` }}
                    />
                  </div>
                  <span className="text-sm text-gray-600">{(stats.up / stats.total * 100).toFixed(1)}%</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">Down</span>
                <div className="flex items-center space-x-2">
                  <div className="w-20 bg-red-100 rounded-full h-2">
                    <div
                      className="bg-red-600 h-2 rounded-full"
                      style={{ width: `${(stats.down / stats.total) * 100}%` }}
                    />
                  </div>
                  <span className="text-sm text-gray-600">{(stats.down / stats.total * 100).toFixed(1)}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
          <div className="space-y-3">
            {websites.map((website) => (
              <div key={website.id} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-b-0">
                <div className="flex items-center space-x-3">
                  {website.status === 'up' && <CheckCircle className="w-5 h-5 text-green-600" />}
                  {website.status === 'down' && <XCircle className="w-5 h-5 text-red-600" />}
                  {website.status !== 'up' && website.status !== 'down' && <XCircle className="w-5 h-5 text-yellow-600" />}
                  <div>
                    <p className="text-sm font-medium text-gray-700">{website.name}</p>
                    <p className="text-xs text-gray-500">
                      {website.status === 'up' ? 'Website is up' : 
                       website.status === 'down' ? 'Website is down' : 
                       `Error: ${website.status}`}
                    </p>
                  </div>
                </div>
                <p className="text-xs text-gray-500">
                  {website.last_checked > 0 
                    ? `Checked ${new Date(website.last_checked * 1000).toLocaleTimeString()}` 
                    : 'Never checked'
                  }
                </p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}