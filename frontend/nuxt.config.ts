// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',

  ssr: false,

  devtools: {
    enabled: false
  },

  modules: ['@pinia/nuxt', '@vueuse/nuxt', '@nuxt/ui', '@nuxt/eslint'],

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
  },

  runtimeConfig: {
    public: {
      apiBaseURL: process.env.NUXT_API_BASE_URL || 'https://api.meizuno.com'
    }
  }
})
