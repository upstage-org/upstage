import { useMutation } from "@vue/apollo-composable";
import { message } from "ant-design-vue";
import gql from "graphql-tag";
import { ref, computed } from "vue";
import { permissionFragment } from "../../../models/fragment";
import { CopyrightLevel, Media, Permission, UploadFile } from "../../../models/studio";

interface SaveMediaPayload {
  files: UploadFile[];
  media: SaveMediaMutationVariables;
}

interface SaveMediaMutationVariables {
  id?: string
  name: string
  urls: string[]
  mediaType: string
  copyrightLevel: CopyrightLevel
  stageIds: number[]
  userIds: number[]
  tags: string[],
  w: number,
  h: number,
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
  const { mutate } = useMutation<{ saveMedia: { asset: Media } }, { input: SaveMediaMutationVariables }>(gql`
    mutation SaveMedia($input: SaveStageInput!) {
      saveMedia(input: $input) {
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
      payload.media.urls = payload.files.filter(file => file.status !== 'local').map(file => file.url!)
      const result = await mutate({ input: payload.media })
      const mediaId = result?.data?.saveMedia.asset.id
      if (mediaId) {
        message.success("Media saved successfully")
        handleSuccess(mediaId)
      }
    } catch (error) {
      message.error('' + error)
    } finally {
      progress.value = 100
    }
  }

  const saving = computed(() => progress.value < 100)

  return { progress, saveMedia, saving }
}

export const useConfirmPermission = () => {
  return useMutation<{ confirmPermission: { success: boolean, message: string, permissions: Permission[] } }, { id: string, approved: boolean }>(gql`
    mutation ConfirmPermission($id: ID, $approved: Boolean) {
      confirmPermission(id: $id, approved: $approved) {
        success
        message
        permissions {
          ...permissionFragment
        }
      }
    }
    ${permissionFragment}
  `)
}

export const useRequestPermission = () => {
  return useMutation<{ requestPermission: { success: boolean, message: string } }, { assetId: string, note?: string }>(gql`
    mutation RequestPermission($assetId: ID, $note: String) {
      requestPermission(assetId: $assetId, note: $note) {
        success
      }
    }
  `)
}