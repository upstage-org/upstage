const STATIC_ASSETS_ENDPOINT = `https://dev-app1.upstage.org.nz/V4.0/static/assets/`

export function absolutePath(path: string) {
  return `${STATIC_ASSETS_ENDPOINT}${path}`
}