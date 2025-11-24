export interface Chat {
  id: string
  firstName: string
  lastName: string
  email: string
  is2faEnabled: string
  createdAt: Date
  updatedAt: Date
}

export interface ChatResponse {
  id: string
  name: string
  isMuted: true
  isArchived: true
  createdAt: Date
  updatedAt: Date
}
