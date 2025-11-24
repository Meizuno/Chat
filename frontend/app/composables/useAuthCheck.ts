import { useUserStore } from '~/stores/userStore'
export const useAuthCheck = () => {
  const userStore = useUserStore()
  const { me } = userStore

  const authCheck = async () => {
    await me()
  }

  return { authCheck }
}
