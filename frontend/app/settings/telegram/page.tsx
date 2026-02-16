'use client'

import { useState } from 'react'
import { Bell, CheckCircle, XCircle, AlertCircle, Settings, Mail, Phone, Globe, Link2, Zap, Clock } from 'lucide-react'

export default function TelegramSettings() {
  const [notificationsEnabled, setNotificationsEnabled] = useState(false)
  const [telegramConnected, setTelegramConnected] = useState(false)
  const [webhookUrl, setWebhookUrl] = useState('')
  const [status, setStatus] = useState('')
  const [statusType, setStatusType] = useState<'success' | 'error' | 'warning'>('success')

  const notificationTypes = [
    { id: 'up', name: 'Website Up', icon: CheckCircle, enabled: true },
    { id: 'down', name: 'Website Down', icon: XCircle, enabled: true },
    { id: 'error', name: 'Error Alerts', icon: AlertCircle, enabled: true },
    { id: 'daily', name: 'Daily Summary', icon: Bell, enabled: false },
  ]

  const saveSettings = async () => {
    try {
      // Simulate saving settings
      await new Promise(resolve => setTimeout(resolve, 1000))
      setStatus('Settings saved successfully!')
      setStatusType('success')
    } catch (error) {
      setStatus('Failed to save settings')
      setStatusType('error')
    }
  }

  const testNotification = async () => {
    try {
      // Simulate test notification
      await new Promise(resolve => setTimeout(resolve, 500))
      setStatus('Test notification sent!')
      setStatusType('success')
    } catch (error) {
      setStatus('Failed to send test notification')
      setStatusType('error')
    }
  }

  const getIcon = (type: string) => {
    switch (type) {
      case 'up': return <CheckCircle className="w-5 h-5 text-green-600" />
      case 'down': return <XCircle className="w-5 h-5 text-red-600" />
      case 'error': return <AlertCircle className="w-5 h-5 text-yellow-600" />
      case 'daily': return <Bell className="w-5 h-5 text-blue-600" />
      default: return <Bell className="w-5 h-5 text-gray-600" />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Bell className="w-8 h-8 mr-3 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">Notifications</h1>
            </div>
            <nav className="flex space-x-4">
              <a href="/" className="text-gray-600 hover:text-gray-900">
                <Globe className="w-6 h-6" />
              </a>
              <a href="/dashboard" className="text-gray-600 hover:text-gray-900">
                <Settings className="w-6 h-6" />
              </a>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h2 className="text-3xl font-bold text-gray-900">Telegram Notifications</h2>
          <p className="text-gray-600 mt-1">Configure how you receive alerts about your websites</p>
        </div>

        {/* Status Alert */}
        {status && (
          <div className={`mb-6 p-4 rounded-lg border ${statusType === 'success' ? 'bg-green-50 border-green-200' : statusType === 'error' ? 'bg-red-50 border-red-200' : 'bg-yellow-50 border-yellow-200'}`}>
            <div className="flex items-center">
              {statusType === 'success' && <CheckCircle className="w-5 h-5 text-green-600 mr-3" />}
              {statusType === 'error' && <XCircle className="w-5 h-5 text-red-600 mr-3" />}
              {statusType === 'warning' && <AlertCircle className="w-5 h-5 text-yellow-600 mr-3" />}
              <p className={`text-sm ${statusType === 'success' ? 'text-green-800' : statusType === 'error' ? 'text-red-800' : 'text-yellow-800'}`}>
                {status}
              </p>
            </div>
          </div>
        )}

        {/* Connection Section */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Link2 className="w-5 h-5 mr-2 text-blue-600" />
            Connection Status
          </h3>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">Telegram Integration</span>
              <div className="flex items-center space-x-2">
                {telegramConnected ? (
                  <>
                    <CheckCircle className="w-5 h-5 text-green-600" />
                    <span className="text-sm text-green-600">Connected</span>
                  </>
                ) : (
                  <>
                    <XCircle className="w-5 h-5 text-red-600" />
                    <span className="text-sm text-red-600">Disconnected</span>
                  </>
                )}
              </div>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">Notifications</span>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setNotificationsEnabled(!notificationsEnabled)}
                  className={`px-3 py-1 rounded-full text-sm font-medium ${
                    notificationsEnabled
                      ? 'bg-green-100 text-green-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  {notificationsEnabled ? 'Enabled' : 'Disabled'}
                </button>
              </div>
            </div>

            <div className="mt-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Webhook URL
              </label>
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={webhookUrl}
                  onChange={(e) => setWebhookUrl(e.target.value)}
                  placeholder="https://your-webhook-url.com"
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={!notificationsEnabled}
                />
                <button
                  onClick={() => {
                    if (webhookUrl) {
                      navigator.clipboard.writeText(webhookUrl)
                      setStatus('Webhook URL copied to clipboard!')
                      setStatusType('success')
                    }
                  }}
                  className="px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-300"
                  disabled={!webhookUrl || !notificationsEnabled}
                >
                  Copy
                </button>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                This URL is used to send notifications to your Telegram bot
              </p>
            </div>
          </div>
        </div>

        {/* Notification Types */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Bell className="w-5 h-5 mr-2 text-blue-600" />
            Notification Types
          </h3>
          
          <div className="space-y-3">
            {notificationTypes.map((type) => (
              <div key={type.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  {getIcon(type.id)}
                  <div>
                    <p className="text-sm font-medium text-gray-700">{type.name}</p>
                    <p className="text-xs text-gray-500">Get notified when a website {type.name.toLowerCase()}</p>
                  </div>
                </div>
                <button
                  onClick={() => {
                    const updatedTypes = notificationTypes.map(t => 
                      t.id === type.id ? { ...t, enabled: !t.enabled } : t
                    )
                    // Update state (simplified for this example)
                    console.log('Updated types:', updatedTypes)
                  }}
                  className={`px-3 py-1 rounded-full text-sm font-medium ${
                    type.enabled
                      ? 'bg-green-100 text-green-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  {type.enabled ? 'Enabled' : 'Disabled'}
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Test Section */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Zap className="w-5 h-5 mr-2 text-blue-600" />
            Test Notifications
          </h3>
          
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-700 mb-2">Send a test notification to verify your settings:</p>
              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={testNotification}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  <Bell className="w-5 h-5 mr-2" />
                  Test Notification
                </button>
                <button
                  onClick={() => {
                    // Simulate connection test
                    setTelegramConnected(!telegramConnected)
                    setStatus(
                      telegramConnected 
                        ? 'Disconnected from Telegram'
                        : 'Connected to Telegram successfully!'
                    )
                    setStatusType(telegramConnected ? 'error' : 'success')
                  }}
                  className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
                >
                  <Globe className="w-5 h-5 mr-2" />
                  Test Connection
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Save Section */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold mb-1 flex items-center">
                <Clock className="w-5 h-5 mr-2 text-blue-600" />
                Auto-Save
              </h3>
              <p className="text-sm text-gray-500">
                Changes are automatically saved every 30 seconds
              </p>
            </div>
            <button
              onClick={saveSettings}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              <CheckCircle className="w-5 h-5 mr-2" />
              Save Now
            </button>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-8 flex space-x-4">
          <button
            onClick={() => {
              setStatus('Settings reset to defaults')
              setStatusType('warning')
              // Reset settings logic here
            }}
            className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
          >
            <XCircle className="w-5 h-5 mr-2" />
            Reset All
          </button>
          <button
            onClick={() => {
              setStatus('Settings exported successfully')
              setStatusType('success')
              // Export logic here
            }}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
          >
            <Save className="w-5 h-5 mr-2" />
            Export Settings
          </button>
        </div>
      </main>
    </div>
  )
}