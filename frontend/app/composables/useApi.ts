export const useApi = () => {
  const config = useRuntimeConfig()
  const { displayError } = useDisplayMessages()

  const userStore = useUserStore()
  const { user } = storeToRefs(userStore)
  const token = user?.value.id

  return $fetch.create({
    baseURL: config.public.apiBaseURL,
    onRequest({ options }) {
      if (token) {
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${token}`
        }
      }
      if (error) {
        displayError({
          description: error.message
        })
      }
    },
    onResponseError({ response }) {
      if (response.status === 401) {
        navigateTo('/auth/login')
      }
      displayError({
        description: response._data?.message || 'An error occurred'
      })
    }
  })
}
