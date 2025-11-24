<template>
  <div>
    <UButton
      label="Get Chats"
      @click="getChats()"
    />
  </div>
  <div class="flex flex-col items-center justify-center py-16">
    <UEmpty
      icon="i-lucide-file"
      title="No projects found"
      description="It looks like you haven't added any projects. Create one to get started."
    />
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '~/stores/userStore'

const userStore = useUserStore()
// const { isUserAuthenticated } = userStore

const { getChats } = useChatStore()

// if (!isUserAuthenticated) {
//   navigateTo('/auth/login')
// }
</script>
