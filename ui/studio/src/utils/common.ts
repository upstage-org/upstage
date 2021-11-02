import configs from "../config"

export function absolutePath(path: string) {
  return `${configs.STATIC_ASSETS_ENDPOINT}${path}`
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

export function humanFileSize(bytes: number, si = false, dp = 1) {
  const thresh = si ? 1000 : 1024;

  if (Math.abs(bytes) < thresh) {
    return bytes + ' B';
  }

  const units = ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
  let u = -1;
  const r = 10 ** dp;

  do {
    bytes /= thresh;
    ++u;
  } while (Math.round(Math.abs(bytes) * r) / r >= thresh && u < units.length - 1);


  return bytes.toFixed(dp) + ' ' + units[u];
}