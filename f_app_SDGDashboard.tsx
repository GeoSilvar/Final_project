'use client'

import { useEffect, useState } from 'react'

export function SDGDashboard() {
  const [metrics, setMetrics] = useState({
    enrollment: 0,
    attendance: 0,
    literacy: 0,
    completion: 0
  })

  useEffect(() => {
    // Simulate loading metrics
    const timer = setTimeout(() => {
      setMetrics({
        enrollment: 95,
        attendance: 88,
        literacy: 76,
        completion: 82
      })
    }, 1000)

    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8">
      <div className="flex items-center mb-8">
        <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mr-4">
          <span className="text-white text-2xl font-bold">4</span>
        </div>
        <div>
          <h2 className="text-2xl font-bold text-slate-800">
            SDG 4 Dashboard
          </h2>
          <p className="text-slate-600">Quality Education Indicators</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6 mb-8">
        <div className="bg-blue-50 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-blue-700 mb-1">
            {metrics.enrollment}%
          </div>
          <div className="text-sm text-blue-600">Enrollment Rate</div>
        </div>
        <div className="bg-green-50 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-green-700 mb-1">
            {metrics.attendance}%
          </div>
          <div className="text-sm text-green-600">Attendance</div>
        </div>
        <div className="bg-purple-50 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-purple-700 mb-1">
            {metrics.literacy}%
          </div>
          <div className="text-sm text-purple-600">Literacy Rate</div>
        </div>
        <div className="bg-orange-50 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-orange-700 mb-1">
            {metrics.completion}%
          </div>
          <div className="text-sm text-orange-600">Completion Rate</div>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="font-semibold text-slate-800">Key Features</h3>
        <div className="space-y-3">
          {[
            '📊 CBC Competency Tracking',
            '👨‍🏫 Teacher CPD Management',
            '💰 M-Pesa Fee Integration',
            '📱 Offline-First Design',
            '🔐 Data Protection Compliant',
            '🌍 SDG 4 Analytics'
          ].map((feature, index) => (
            <div key={index} className="flex items-center text-slate-700">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
              {feature}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}