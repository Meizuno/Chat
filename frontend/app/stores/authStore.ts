export const useAuthStore = defineStore('authStore', () => {
  const api = useApi()

  const userStore = useUserStore()
  const { updateUser } = userStore

  // Actions

  interface SignInParams {
    email: string
    password: string
  }
  const signInWithEmailAndPassword = async ({
    email,
    password
  }: SignInParams) => {
    try {
      const response = await api('/chat/auth/login', {
        method: 'POST',
        body: {
          email,
          password
        }
      })
      updateUser(response.user)
      return { success: true }
    } catch (error) {
      const message =
        error.statusCode === 401
          ? 'Invalid email or password'
          : error.message || 'Login failed'
      error.value = message
      return { success: false, error: message }
    }
  }

  interface SignUpParams {
    firstName: string
    lastName: string
    email: string
    password: string
  }
  const signUp = async ({
    firstName,
    lastName,
    email,
    password
  }: SignUpParams) => {
    try {
      const response = await api('/chat/auth/register', {
        method: 'POST',
        body: {
          firstName,
          lastName,
          email,
          password
        },
        headers: {
          Authorization: null
        }
      })
      updateUser(response.user)
      return { success: true }
    } catch (error) {
      const message =
        error.statusCode === 401
          ? 'Invalid email or password'
          : error.message || 'Login failed'
      error.value = message
      return { success: false, error: message }
    }
  }

  const signOut = async () => {
    try {
      await api('/chat/auth/logout', {
        method: 'POST'
      })
      updateUser(null)
      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error : new Error(String(error))
      }
    }
  }

  const refreshToken = async (): Promise<{
    success: boolean
    token?: string
    error?: Error
  }> => {
    try {
      const response = await api<{ token: string }>('/chat/auth/refresh', {
        method: 'POST'
      })
      return {
        success: true,
        token: response.token
      }
    } catch (error) {
      return {
        success: false,
        error:
          error instanceof Error ? error : new Error('Failed to refresh token')
      }
    }
  }

  return {
    signInWithEmailAndPassword,
    signUp,
    signOut,
    refreshToken
  }
})
