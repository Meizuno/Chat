<template>
  <UApp>
    <NuxtLoadingIndicator />

    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>

<script setup lang="ts">
const { setSeo } = useSeo()
const { authCheck } = useAuthCheck()

setSeo()
authCheck()
</script>
