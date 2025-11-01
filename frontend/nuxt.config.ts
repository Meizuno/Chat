// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',

  devtools: {
    enabled: false
  },

  modules: ['@vueuse/nuxt', '@nuxt/ui', '@nuxt/eslint'],

  css: ['~/assets/css/main.css'],

  components: [
    {
      path: '@/components',
      pathPrefix: false
    }
  ],

  nitro: {
    experimental: {
      websocket: true
    }
  }
})
