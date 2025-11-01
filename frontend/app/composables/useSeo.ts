export const useSeo = () => {
  const title = 'Super Chat'
  const description = 'A full-featured Super Chat made with Nuxt UI.'

  const setSeoMeta = () => {
    useSeoMeta({
      title,
      description,
      viewport: 'width=device-width, initial-scale=1.0, user-scalable=no'
    })
  }

  const setSeoHead = () => {
    useHead({
      title,
      link: [
        {
          rel: 'icon',
          type: 'image/svg+xml',
          href: '/favicon.svg'
        }
      ]
    })
  }

  const setSeo = () => {
    setSeoMeta()
    setSeoHead()
  }

  return { setSeoMeta, setSeoHead, setSeo }
}
