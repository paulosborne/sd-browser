import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  email: string
  timezone: string
  isAdmin: boolean
}

interface AuthState {
  user: User | null
  accessToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  setUser: (user: User) => void
  setToken: (token: string) => void
}

export const useAuthStore = create<AuthState>()()
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      isAuthenticated: false,
      isLoading: false,
      login: async (email: string, password: string) => {
        set({ isLoading: true })
        try {
          // TODO: Implement login API call
          console.log('Login:', email, password)
          set({ isLoading: false })
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },
      logout: () => {
        set({ 
          user: null, 
          accessToken: null, 
          isAuthenticated: false 
        })
      },
      setUser: (user: User) => {
        set({ user, isAuthenticated: true })
      },
      setToken: (token: string) => {
        set({ accessToken: token })
      },
    }),
    {
      name: 'auth-storage',
    }
  )
