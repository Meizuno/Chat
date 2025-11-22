<template>
  <UAuthForm
    :fields="fields"
    :schema="schema"
    title="Reset your password"
    icon="i-lucide-key-round"
    :submit="{ label: 'Reset password' }"
    :validate-on="['change']"
    :loading="loading"
    @submit="onSubmit"
  >
    <template #description>
      Remember your password?
      <ULink
        to="/auth/login"
        class="text-primary font-medium"
      >
        Sign in
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
  title: 'Reset Password',
  description: 'Create a new password'
})

const route = useRoute()

const fields = [
  {
    name: 'password',
    label: 'New Password',
    type: 'password' as const,
    placeholder: 'Enter your new password',
    required: true
  },
  {
    name: 'confirmPassword',
    label: 'Confirm Password',
    type: 'password' as const,
    placeholder: 'Confirm your new password',
    required: true
  }
]

const schema = z
  .object({
    password: z.string().min(8, 'Password must be at least 8 characters'),
    confirmPassword: z.string()
  })
  .refine(data => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ['confirmPassword']
  })

type Schema = z.output<typeof schema>

const userStore = useUserStore()
const { forgotPassword } = userStore
const { displayError, displaySuccess } = useDisplayMessages()

const loading = ref(false)

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  const token = route.query.token as string

  if (!token) {
    displayError({
      title: 'Invalid reset link',
      description: 'The password reset link is invalid or expired.'
    })
    return
  }

  loading.value = true
  await forgotPassword(payload.data)
  loading.value = false
}
</script>
