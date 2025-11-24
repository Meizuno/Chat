import type { Chat } from '@/types/chat'

export const useChatStore = defineStore('chatStore', () => {
  const chat = ref<Chat | null>(null)

  const setChat = (currentChat: Chat | null) => {
    chat.value = currentChat
  }

  const getChats = async () => {
    const { data } = await useApiFetch('/messenger/chat', {
      method: 'GET'
    })
    if (data.value) {
      console.log('data', data)
      setChat(data.value)
    }
  }

  return {
    chat,
    setChat,
    getChats
  }
})
