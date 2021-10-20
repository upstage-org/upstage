const STATIC_ASSETS_ENDPOINT = `https://dev-app1.upstage.org.nz/V4.0/static/assets/`

export function absolutePath(path: string) {
  return `${STATIC_ASSETS_ENDPOINT}${path}`
}

interface SharedAuth {
  refresh_token: string
  token: string
}

export function getSharedAuth(): SharedAuth | undefined {
  try {
    const sharedStateJSON = localStorage.getItem('vuex')
    if (sharedStateJSON) {
      const sharedState = JSON.parse(sharedStateJSON)
      return sharedState
    }
  } catch (error) {
    console.log('No shared auth found. Try login using dashboard first!')
  }
}