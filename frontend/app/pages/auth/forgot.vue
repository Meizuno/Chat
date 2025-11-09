<template>
  <UAuthForm
    :fields="fields"
    :schema="schema"
    title="Forgot your password?"
    icon="i-lucide-key"
    :submit="{ label: 'Send reset email' }"
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
  title: 'Forgot Password',
  description: 'Reset your password'
})

const fields = [
  {
    name: 'email',
    type: 'text' as const,
    label: 'Email',
    placeholder: 'Enter your email address',
    required: true
  }
]

const schema = z.object({
  email: z.email('Please enter a valid email address')
})

type Schema = z.output<typeof schema>

const authStore = useAuthStore()
const { forgetPassword } = authStore
const { displayError, displaySuccess } = useDisplayMessages()

const loading = ref(false)

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  const { email } = payload.data
  loading.value = true

  const { success, error } = await forgetPassword({
    email,
    redirectTo: `/auth/reset`
  })

  if (success) {
    displaySuccess({
      title: 'Password reset email sent',
      description: 'Please check your email for the password reset link.'
    })
  } else {
    const errorMessage =
      (error as Error)?.message ||
      'An unknown error occurred. Please try again later.'

    displayError({
      title: 'Password reset failed',
      description: errorMessage
    })
  }
  loading.value = false
}
</script>
