<template>
  <UButton
    :label="collapsed ? '' : 'Login'"
    icon="i-lucide-log-in"
    color="neutral"
    variant="ghost"
    class="w-full"
    @click="open = true"
  />
  <UModal
    v-model:open="open"
    class="max-w-sm p-6"
  >
    <template #content>
      <UAuthForm
        :schema="schema"
        title="Login"
        description="Enter your credentials to access your account."
        icon="i-lucide-user"
        :fields="fields"
        :providers="providers"
        @submit="onSubmit"
      >
        <template #description>
          Don't have an account?
          <ULink
            to="#"
            class="text-primary font-medium"
          >
            Sign up
          </ULink>
          .
        </template>
        <template #password-hint>
          <ULink
            to="#"
            class="text-primary font-medium"
            tabindex="-1"
          >
            Forgot password?
          </ULink>
        </template>
        <template #footer>
          By signing in, you agree to our
          <ULink
            to="#"
            class="text-primary font-medium"
          >
            Terms of Service
          </ULink>
          .
        </template>
      </UAuthForm>
    </template>
  </UModal>
</template>

<script setup lang="ts">
const open = ref<boolean>(false)

import * as z from 'zod'
import type { FormSubmitEvent, AuthFormField } from '@nuxt/ui'

const toast = useToast()

const fields: AuthFormField[] = [
  {
    name: 'email',
    type: 'email',
    label: 'Email',
    placeholder: 'Enter your email',
    required: true
  },
  {
    name: 'password',
    label: 'Password',
    type: 'password',
    placeholder: 'Enter your password',
    required: true
  },
  {
    name: 'remember',
    label: 'Remember me',
    type: 'checkbox'
  }
]

const providers = [
  {
    label: 'Google',
    icon: 'i-simple-icons-google',
    onClick: () => {
      toast.add({
        title: 'Google',
        description: 'Login with Google'
      })
    }
  },
  {
    label: 'GitHub',
    icon: 'i-simple-icons-github',
    onClick: () => {
      toast.add({
        title: 'GitHub',
        description: 'Login with GitHub'
      })
    }
  }
]

const schema = z.object({
  email: z.email('Invalid email'),
  password: z
    .string('Password is required')
    .min(8, 'Must be at least 8 characters')
})

type Schema = z.output<typeof schema>

function onSubmit(payload: FormSubmitEvent<Schema>) {
  console.log('Submitted', payload)
}
</script>
