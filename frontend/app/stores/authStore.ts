import type { RegisterRequest, LoginRequest } from '@/types/auth'

export const useAuthStore = defineStore('authStore', () => {
  const userStore = useUserStore()
  const { setUser } = userStore
  const token = ref<string | null>(null)
  const { displaySuccess } = useDisplayMessages()

  const register = async (userData: RegisterRequest) => {
    const { data } = await useApiFetch('/messenger/auth/register', {
      method: 'POST',
      body: userData
    })
    if (data.value) {
      setUser(data.value)
      displaySuccess({
        description: 'Registration successful'
      })
    }
    navigateTo('/')
  }

  const login = async (userData: LoginRequest) => {
    const { data } = await useApiFetch('/messenger/auth/login', {
      method: 'POST',
      body: userData
    })
    if (data.value) {
      setUser(data.value)
      displaySuccess({
        description: 'Login successful'
      })
    }
    navigateTo('/')
  }

  const logout = async () => {
    const { data } = await useApiFetch('/messenger/auth/logout', {
      method: 'POST'
    })
    if (data.value) {
      setUser(null)
      displaySuccess({
        description: 'Logout successful'
      })
    }
    navigateTo('/auth/login')
  }

  const refresh = async () => {
    const { data } = await useApiFetch('/messenger/auth/refresh', {
      method: 'POST'
    })
    if (data.value) {
      displaySuccess({
        description: 'Logout successful'
      })
    }
    navigateTo('/auth/login')
  }

  return {
    token,
    register,
    login,
    logout,
    refresh
  }
})
