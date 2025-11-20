'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { SDGDashboard } from './components/SDGDashboard'
import { LoginForm } from './components/LoginForm'

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const router = useRouter()

  const handleLogin = (token: string, role: string) => {
    localStorage.setItem('token', token)
    localStorage.setItem('userRole', role)
    setIsAuthenticated(true)
    router.push('/dashboard')
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-emerald-50">
      {!isAuthenticated ? (
        <div className="container mx-auto px-4 py-8">
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-slate-800 mb-4">
              Asili SSMS
            </h1>
            <p className="text-xl text-slate-600 max-w-2xl mx-auto">
              Smart School Management System aligned with UN SDG 4 - Quality Education
            </p>
            <div className="mt-6 flex justify-center space-x-4">
              <span className="px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm">
                🇰🇪 Kenyan CBC Aligned
              </span>
              <span className="px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm">
                 Data Protection Compliant
              </span>
              <span className="px-4 py-2 bg-purple-100 text-purple-800 rounded-full text-sm">
                📱 Offline-First PWA
              </span>
            </div>
          </div>
          
          <div className="grid md:grid-cols-2 gap-12 max-w-6xl mx-auto">
            <LoginForm onLogin={handleLogin} />
            <SDGDashboard />
          </div>
        </div>
      ) : (
        <div>Redirecting to dashboard...</div>
      )}
    </main>
  )
}