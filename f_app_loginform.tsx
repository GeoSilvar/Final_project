'use client'

import { useState } from 'react'
import axios from 'axios'

interface LoginFormProps {
  onLogin: (token: string, role: string) => void
}

export function LoginForm({ onLogin }: LoginFormProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('username', email)
      formData.append('password', password)

      const response = await axios.post(
        'http://localhost:8000/api/v1/auth/token',
        formData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      )

      const { access_token } = response.data
      
      // Decode token to get role (in production, use proper JWT decoding)
      const tokenData = JSON.parse(atob(access_token.split('.')[1]))
      onLogin(access_token, tokenData.role)
    } catch (err) {
      setError('Invalid credentials. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8">
      <h2 className="text-3xl font-bold text-slate-800 mb-6 text-center">
        Welcome Back
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-2">
            Email Address
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            placeholder="Enter your email"
            required
          />
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-slate-700 mb-2">
            Password
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            placeholder="Enter your password"
            required
          />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 focus:ring-4 focus:ring-blue-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-semibold"
        >
          {isLoading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>

      <div className="mt-8 pt-6 border-t border-slate-200">
        <div className="grid grid-cols-3 gap-4 text-center text-sm text-slate-600">
          <div>
            <div className="font-semibold">Admin</div>
            <div className="text-xs">Full System Access</div>
          </div>
          <div>
            <div className="font-semibold">Teacher</div>
            <div className="text-xs">CBC Assessments</div>
          </div>
          <div>
            <div className="font-semibold">Parent</div>
            <div className="text-xs">Student Tracking</div>
          </div>
        </div>
      </div>
    </div>
  )
}