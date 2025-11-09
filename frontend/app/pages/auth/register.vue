<template>
  <UAuthForm
    :fields="fields"
    :schema="schema"
    title="Create account"
    icon="i-lucide-user-plus"
    :submit="{ label: 'Register' }"
    :validate-on="['change']"
    :loading="loading"
    @submit="onSubmit"
  >
    <template #description>
      Already have an account?
      <ULink
        to="/auth/login"
        class="text-primary font-medium"
      >
        Login
      </ULink>
      .
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
  title: 'Register',
  description: 'Create a new account'
})

const fields = [
  {
    name: 'firstName',
    type: 'text' as const,
    label: 'First name',
    placeholder: 'Enter your first name',
    required: true
  },
  {
    name: 'lastName',
    type: 'text' as const,
    label: 'Last name',
    placeholder: 'Enter your last name',
    required: true
  },
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
  firstName: z.string().min(1, { message: 'Please enter your first name' }),
  lastName: z.string().min(1, { message: 'Please enter your last name' }),
  email: z.email('Please enter a valid email address'),
  password: z
    .string()
    .min(6, { message: 'Password must be at least 6 characters long' })
})

type Schema = z.output<typeof schema>

const authStore = useAuthStore()
const { signUp } = authStore
const { displayError } = useDisplayMessages()

const loading = ref(false)

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  const { firstName, lastName, email, password } = payload.data
  loading.value = true
  const { success, error } = await signUp({
    firstName,
    lastName,
    email,
    password
  })

  if (success) {
    await navigateTo('/')
  } else {
    const errorMessage =
      (error as Error)?.message ||
      'An unknown error occurred. Please try again later.'
    displayError({
      title: 'Registration failed',
      description: errorMessage
    })
  }
  loading.value = false
}
</script>
