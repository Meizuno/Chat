import type {
  User,
  ResetPasswordRequest,
  ForgotPasswordRequest
} from '@/types/user'

export const useUserStore = defineStore('userStore', () => {
  const user = ref<User | null>(null)
  const { displaySuccess } = useDisplayMessages()

  const setUser = (currentUser: User | null) => {
    user.value = currentUser
  }

  const isUserAuthenticated = computed(() => !!user.value)

  const forgotPassword = async (userData: ForgotPasswordRequest) => {
    const { data } = await useApiFetch('/messenger/user/forgot-password', {
      method: 'POST',
      body: {
        ...userData,
        redirectTo: '/auth/reset'
      }
    })
    if (data.value) {
      displaySuccess({
        title: 'Password reset email sent',
        description: 'Please check your email for the password reset link.'
      })
    }
    navigateTo('/auth/login')
  }

  const resetPassword = async (userData: ResetPasswordRequest) => {
    const { data } = await useApiFetch('/messenger/user/reset-password', {
      method: 'POST',
      body: userData
    })
    if (data.value) {
      displaySuccess({
        title: 'Password reset successful',
        description:
          'Your password has been reset. Please sign in with your new password.'
      })
    }
    navigateTo('/auth/login')
  }

  return {
    user,
    setUser,
    isUserAuthenticated,
    forgotPassword,
    resetPassword
  }
})
