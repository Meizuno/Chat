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

const userStore = useUserStore()
const { forgotPassword } = userStore

const loading = ref(false)

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  loading.value = true
  await forgotPassword(payload.data)
  loading.value = false
}
</script>
