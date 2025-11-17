export interface User {
  id: string
  firstName: string
  lastName: string
  email: string
  is2faEnabled: string
  createdAt: Date
  updatedAt: Date
}

export interface ForgotPasswordRequest {
  email: string
  redirectTo: string
}

export interface ResetPasswordRequest {
  password: string
  token: string
}
