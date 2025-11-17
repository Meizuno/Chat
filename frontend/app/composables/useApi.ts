import type { UseFetchOptions } from '#app'
import { defu } from 'defu'

export function useApiFetch<T>(url: string, options: UseFetchOptions<T> = {}) {
  const config = useRuntimeConfig()
  const { displayError } = useDisplayMessages()

  const authStore = useAuthStore()
  const { token } = storeToRefs(authStore)

  const defaults: UseFetchOptions<T> = {
    baseURL: config.public.apiBaseURL,
    onRequest({ options }) {
      if (token) {
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${token}`
        }
      }
    },
    onResponseError({ response }) {
      const status = response.status
      const message =
        (response._data as any)?.detail || 'Unexpected server error'

      if (status === 401) {
        navigateTo('/auth/login')
      }
      displayError({
        description: message || 'An error occurred'
      })
    }
  }

  const params = defu(options, defaults)

  return useFetch<T>(url, params)
}
