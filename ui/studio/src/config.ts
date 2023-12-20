const configs = {
  MODE: import.meta.env.MODE as 'development' | 'production',
  UPSTAGE_URL: import.meta.env.VITE_APP_UPSTAGE_URL ?? window.location.origin,
  GRAPHQL_ENDPOINT: import.meta.env.VITE_APP_GRAPHQL_ENDPOINT as string,
  ALLOWED_EXTENSIONS: {
    IMAGE: '.svg,.jpg,.jpeg,.png,.gif',
    AUDIO: '.wav,.mpeg,.mp3,.aac,.aacp,.ogg,.webm,.flac,.m4a',
    VIDEO: '.mp4,.webm,.opgg,.3gp,.flv'
  }
}

export default configs