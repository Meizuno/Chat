import type { User } from '@/types'

export const useUserStore = defineStore('user', () => {
  const api = useApi()

  // State

  const user = ref<User | null>(null)

  // Getters

  const isUserAuthenticated = computed(() => !!user.value)

  // Actions

  const updateUser = (newUser: User | null) => {
    user.value = newUser
  }

  interface ForgotPasswordParams {
    email: string
    redirectTo: string
  }
  const forgetPassword = async ({
    email,
    redirectTo
  }: ForgotPasswordParams) => {
    try {
      await api('/chat/user/forgot-password', {
        method: 'POST',
        body: { email, redirectTo }
      })
      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error : new Error(String(error))
      }
    }
  }

  interface ResetPasswordParams {
    newPassword: string
    token: string
  }
  const resetPassword = async ({ newPassword, token }: ResetPasswordParams) => {
    try {
      await api('/chat/user/reset-password', {
        method: 'PUT',
        body: { password: newPassword, token }
      })
      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error : new Error(String(error))
      }
    }
  }

  return {
    user,
    isUserAuthenticated,
    forgetPassword,
    resetPassword,
    updateUser
  }
})
