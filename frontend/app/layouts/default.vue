<template>
  <UDashboardGroup units="rem">
    <UDashboardSidebar
      id="default"
      v-model:open="open"
      :min-size="12"
      resizable
      class="bg-elevated/50"
      :ui="{ footer: 'border-t border-default' }"
    >
      <template #header="{ collapsed }">
        <NuxtLink
          to="/"
          class="flex items-end gap-0.5 ms-auto lg:ms-0"
        >
          <Logo class="h-8 w-auto shrink-0 text-primary" />
          <span
            v-if="!collapsed"
            class="text-xl font-bold text-highlighted hidden lg:block"
          >
            Chat
          </span>
        </NuxtLink>

        <div
          v-if="!collapsed"
          class="flex items-center gap-1.5 ms-auto"
        >
          <UDashboardSearchButton collapsed />
        </div>
      </template>

      <template #default="{ collapsed }">
        <div class="flex flex-col gap-1.5">
          <UButton
            v-bind="
              collapsed ? { icon: 'i-lucide-plus' } : { label: 'New chat' }
            "
            variant="soft"
            block
            to="/"
            @click="open = false"
          />

          <template v-if="collapsed">
            <UDashboardSearchButton collapsed />
          </template>
        </div>

        <UNavigationMenu
          v-if="!collapsed"
          :items="items"
          :collapsed="collapsed"
          orientation="vertical"
          :ui="{ link: 'overflow-hidden' }"
        >
          <template #chat-trailing="{ item }">
            <div
              class="flex -mr-1.25 translate-x-full group-hover:translate-x-0 transition-transform"
            >
              <UButton
                icon="i-lucide-x"
                color="neutral"
                variant="ghost"
                size="xs"
                class="text-muted hover:text-primary hover:bg-accented/50 focus-visible:bg-accented/50 p-0.5"
              />
            </div>
          </template>
        </UNavigationMenu>
      </template>

      <template #footer="{ collapsed }">
        <UUser
          v-if="isUserAuthenticated"
          :name="`${user?.firstName} ${user?.lastName}`"
          :description="user?.email"
        >
          <template #avatar>
            <UAvatar :alt="`${user?.firstName} ${user?.lastName}`" />
          </template>
        </UUser>
        <UButton
          v-else
          to="/auth/login"
          :label="collapsed ? '' : 'Login'"
          icon="i-lucide-log-in"
          color="neutral"
          variant="ghost"
          class="w-full"
          @click="open = true"
        />
      </template>
    </UDashboardSidebar>

    <UDashboardPanel id="home">
      <template #header>
        <UDashboardNavbar
          title="Page"
          :ui="{ right: 'gap-3' }"
        >
          <template #right>
            <UColorModeButton variant="link" />
          </template>
        </UDashboardNavbar>
      </template>

      <template #body>
        <slot />
      </template>
    </UDashboardPanel>
  </UDashboardGroup>
</template>

<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'
import { useUserStore } from '~/stores/userStore'

const userStore = useUserStore()
const { isUserAuthenticated } = userStore
const { user } = storeToRefs(userStore)

const items = ref<NavigationMenuItem[][]>([
  [
    {
      label: 'Links',
      type: 'label'
    },
    {
      label: 'Guide',
      icon: 'i-lucide-book-open',
      children: [
        {
          label: 'Introduction',
          description: 'Fully styled and customizable components for Nuxt.',
          icon: 'i-lucide-house'
        }
      ]
    }
  ],
  [
    {
      label: 'Help',
      icon: 'i-lucide-circle-help',
      disabled: true
    }
  ]
])

const open = ref(false)
</script>
