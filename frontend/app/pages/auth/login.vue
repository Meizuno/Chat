<template>
  <UAuthForm
    :fields="fields"
    :schema="schema"
    title="Login"
    icon="i-lucide-lock"
    :submit="{ label: 'Login' }"
    :validate-on="['change']"
    :loading="loading"
    @submit="onSubmit"
  >
    <template #description>
      Don't have an account?
      <ULink
        to="/auth/register"
        class="text-primary font-medium"
      >
        Sign up
      </ULink>
      .
    </template>
    <template #password-hint>
      <ULink
        to="/auth/forgot"
        class="text-primary font-medium"
        tabindex="-1"
      >
        Forgot password?
      </ULink>
    </template>
  </UAuthForm>
</template>

<script setup lang="ts">
import type { FormSubmitEvent } from '#ui/types'
import * as z from 'zod'
import { useDisplayMessages } from '~/composables/useDisplayMessages'

definePageMeta({
  layout: 'auth'
})

useSeoMeta({
  title: 'Login',
  description: 'Sign in to your account'
})

const fields = [
  {
    name: 'email',
    type: 'text' as const,
    label: 'Email',
    placeholder: 'Enter your email address',
    required: true,
    defaultValue: 'user@gmail.com'
  },
  {
    name: 'password',
    label: 'Password',
    type: 'password' as const,
    placeholder: 'Enter your password',
    required: true,
    defaultValue: '12345678'
  }
]

const schema = z.object({
  email: z.email('Please enter a valid email address'),
  password: z
    .string('Password is required')
    .min(8, 'Must be at least 8 characters')
})

type Schema = z.output<typeof schema>

const authStore = useAuthStore()
const { signInWithEmailAndPassword } = authStore
const { displayError } = useDisplayMessages()

const loading = ref(false)
async function onSubmit(payload: FormSubmitEvent<Schema>) {
  const { email, password } = payload.data
  loading.value = true
  const { success, error } = await signInWithEmailAndPassword({
    email,
    password
  })

  if (success) {
    await navigateTo('/')
  } else {
    const errorMessage = (error as Error)?.message
    displayError({
      title: 'Login failed',
      description: errorMessage
    })
  }
  loading.value = false
}
</script>
