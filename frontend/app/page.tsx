'use client'

import { useState, useEffect } from 'react'
import { Globe, Zap, CheckCircle, XCircle, Clock, Settings } from 'lucide-react'
import Link from 'next/link'

export default function Home() {
  const [websites, setWebsites] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

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
      setError('')
    } catch (err) {
      setError('Failed to load websites')
      setLoading(false)
    }
  }

  const getStatusIcon = (status: string) => {
    if (status === 'up') return <CheckCircle className="text-green-600" />
    if (status === 'down') return <XCircle className="text-red-600" />
    return <XCircle className="text-yellow-600" />
  }

  const getStatusColor = (status: string) => {
    if (status === 'up') return 'bg-green-100 text-green-800'
    if (status === 'down') return 'bg-red-100 text-red-800'
    return 'bg-yellow-100 text-yellow-800'
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Globe className="w-12 h-12 mx-auto mb-4 text-blue-600 animate-spin" />
          <p className="text-gray-600">Loading websites...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <XCircle className="w-12 h-12 mx-auto mb-4 text-red-600" />
          <p className="text-gray-600">{error}</p>
          <button 
            onClick={fetchWebsites}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
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
              <Globe className="w-8 h-8 mr-3 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">Website Monitor</h1>
            </div>
            <nav className="flex space-x-4">
              <Link href="/settings/telegram" className="text-gray-600 hover:text-gray-900">
                <Settings className="w-6 h-6" />
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Website Status</h2>
          <p className="text-gray-600 mt-1">Last updated: {new Date().toLocaleTimeString()}</p>
        </div>

        <div className="grid gap-6 mb-6">
          {websites.map((website) => (
            <div
              key={website.id}
              className={`p-6 rounded-lg border ${getStatusColor(website.status)} border-opacity-20`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(website.status)}
                  <div>
                    <h3 className="text-lg font-semibold">{website.name}</h3>
                    <p className="text-sm text-gray-600">{website.url}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-600">
                    {website.response_time > 0 ? `${website.response_time}ms` : '—'}
                  </p>
                  <p className="text-xs text-gray-500">
                    {website.last_checked > 0 
                      ? `Last checked: ${new Date(website.last_checked * 1000).toLocaleTimeString()}` 
                      : 'Never checked'
                    }
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Actions */}
        <div className="flex space-x-4">
          <button
            onClick={fetchWebsites}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 flex items-center space-x-2"
          >
            <Zap className="w-5 h-5" />
            <span>Check Now</span>
          </button>
          <button
            onClick={() => {
              const updatedWebsites = websites.map(w => ({ ...w, status: 'up', response_time: 0, last_checked: 0 }))
              setWebsites(updatedWebsites)
            }}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 flex items-center space-x-2"
          >
            <Clock className="w-5 h-5" />
            <span>Reset</span>
          </button>
        </div>
      </main>
    </div>
  )
}