import { useMutation } from "@vue/apollo-composable";
import { message } from "ant-design-vue";
import gql from "graphql-tag";
import { ref, computed } from "vue";
import { Media, UploadFile } from "../../../models/studio";

interface SaveMediaPayload {
  files: UploadFile[];
  media: SaveMediaMutationVariables;
}

interface SaveMediaMutationVariables {
  id?: string
  name: string
  urls?: string[]
  mediaType: string
  playerAccess?: string
  copyrightLevel: 0 | 1 | 2 | 3
  stageIds: number[]
  tags: string[]
}

const getBase64 = (file: File) => new Promise<string>((resolve) => {
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = function () {
    resolve(reader.result as string);
  };
  reader.onerror = function (error) {
    resolve('')
  };
});

export const useSaveMedia = (collectData: () => SaveMediaPayload, handleSuccess: (id: string) => any) => {
  const { mutate: uploadFile } = useMutation<{ uploadFile: { url: string } }, { base64: string, filename: string }>(gql`
    mutation Upload($base64: String!, $filename: String!) {
      uploadFile(base64: $base64, filename: $filename) {
        url
      }
    }
  `)
  const { mutate } = useMutation<{ saveMedia: { asset: Media } }, SaveMediaMutationVariables>(gql`
    mutation SaveMedia($id: ID, $name: String!, $urls: [String], $mediaType: String, $playerAccess: String, $copyrightLevel: Int, $stageIds: [Int], $tags: [String]) {
      saveMedia(id: $id, name: $name, urls: $urls, mediaType: $mediaType, playerAccess: $playerAccess, copyrightLevel: $copyrightLevel, stageIds: $stageIds, tags: $tags) {
        asset {
          id
        }
      }
    }
  `)
  const progress = ref(100)

  const saveMedia = async () => {
    try {
      progress.value = 0
      const payload = collectData()
      const totalSteps = payload.files.length + 1;
      let finishedSteps = 0;
      const increaseProgress = () => {
        finishedSteps++
        progress.value = Math.round(finishedSteps * 100 / totalSteps)
      }
      for (const file of payload.files) {
        if (file.status === 'local') {
          const base64 = await getBase64(file.file)
          const result = await uploadFile({ base64, filename: file.file.name })
          const uploadedUrl = result?.data?.uploadFile.url
          if (uploadedUrl) {
            file.url = uploadedUrl
            file.status = 'uploaded'
            increaseProgress()
          } else {
            message.error(`File ${file.file.name} upload failed!`)
          }
        }
      }
      payload.media.urls = payload.files.filter(file => file.status === 'uploaded').map(file => file.url!)
      const result = await mutate(payload.media)
      const mediaId = result?.data?.saveMedia.asset.id
      if (mediaId) {
        message.success("Media saved successfully")
        handleSuccess(mediaId)
      }
    } catch (error) {
      message.error("Error saving media. Detail: " + error)
    } finally {
      progress.value = 100
    }
  }

  const saving = computed(() => progress.value < 100)

  return { progress, saveMedia, saving }
}