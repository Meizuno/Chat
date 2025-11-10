export const useDisplayMessages = () => {
  const toast = useToast()

  const displayError = ({
    title = 'Error',
    description
  }: {
    title?: string
    description: string
  }): void => {
    toast.add({
      title,
      description,
      icon: 'i-lucide-triangle-alert',
      color: 'error'
    })
  }

  const displaySuccess = ({
    title = 'Success',
    description
  }: {
    title?: string
    description: string
  }): void => {
    toast.add({
      title,
      description,
      icon: 'i-lucide-check-circle',
      color: 'success'
    })
  }

  const displayWarning = ({
    title = 'Warning',
    description
  }: {
    title?: string
    description: string
  }): void => {
    toast.add({
      title,
      description,
      icon: 'i-lucide-octagon-alert',
      color: 'warning'
    })
  }

  return { displayError, displaySuccess, displayWarning }
}
