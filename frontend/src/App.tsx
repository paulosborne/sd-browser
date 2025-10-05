import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from '@/store/auth'
import Layout from '@/components/layout/Layout'
import LoginPage from '@/pages/auth/LoginPage'
import RegisterPage from '@/pages/auth/RegisterPage'
import DashboardPage from '@/pages/DashboardPage'
import OnboardingPage from '@/pages/OnboardingPage'
import GuidePage from '@/pages/GuidePage'
import SearchPage from '@/pages/SearchPage'
import FavouritesPage from '@/pages/FavouritesPage'
import RulesPage from '@/pages/RulesPage'
import CalendarPage from '@/pages/CalendarPage'
import AdminPage from '@/pages/AdminPage'

function App() {
  const { isAuthenticated, isLoading } = useAuthStore()

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return (
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    )
  }

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/onboarding" element={<OnboardingPage />} />
        <Route path="/guide" element={<GuidePage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/favourites" element={<FavouritesPage />} />
        <Route path="/rules" element={<RulesPage />} />
        <Route path="/calendar" element={<CalendarPage />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  )
}

export default App