<script setup lang="ts">
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { ref, watchEffect, PropType } from 'vue';
import { editingMediaVar } from '../../../apollo';
import configs from '../../../config';
import { Media, StudioGraph, User } from '../../../models/studio';
import { useConfirmPermission } from './composable';

const props = defineProps({
    modelValue: {
        type: Number,
        default: 0,
    },
    users: {
        type: Array as PropType<number[]>,
        default: [],
    },
    media: Object as PropType<Media>,
});
const emits = defineEmits(['update:modelValue', 'update:users']);

const copyrightLevel = ref();
const targetKeys = ref();
watchEffect(() => {
    copyrightLevel.value = props.modelValue;
    targetKeys.value = props.users;
})

watchEffect(() => {
    emits('update:modelValue', copyrightLevel.value);
    emits('update:users', targetKeys.value);
})

const { result, loading } = useQuery<StudioGraph>(gql`
{
  users {
    edges {
      node {
        dbId
        displayName
        username
      }
    }
  }
}
`, null, { fetchPolicy: "cache-only" })

const filterOption = (keyword: string, option: any) => {
    const s = keyword.toLowerCase()
    return option.value.toLowerCase().includes(s) || option.label.toLowerCase().includes(s)
}

const renderItem = (item: User) => item.displayName || item.username;

const { mutate: confirmPermission } = useConfirmPermission();
const confirm = (id: string, approved: boolean) => confirmPermission({ id, approved }).then(result => {
    if (result?.data?.confirmPermission.success) {
        const emv = editingMediaVar()
        editingMediaVar({
            ...editingMediaVar()!,
            permissions: result.data.confirmPermission.permissions,
        })
    }
})
</script>

<template>
    <a-space direction="vertical" class="w-full mb-4">
        <a-select class="w-80" placeholder="Media copyright level" v-model:value="copyrightLevel">
            <a-select-option
                v-for="level in configs.MEDIA_COPYRIGHT_LEVELS"
                :key="level.value"
                :value="level.value"
            >
                <span>{{ level.name }}</span>
                <a-tooltip placement="right">
                    <template #title>{{ level.description }}</template>
                    <QuestionCircleOutlined class="float-right" />
                </a-tooltip>
            </a-select-option>
        </a-select>
        <a-alert
            type="warning"
            show-icon
            v-for="request in media?.permissions.filter(p => !p.approved)"
            :key="request.id"
        >
            <template #icon>🔑</template>
            <template #message>
                <b>
                    <DName :user="request.user" />
                </b>
                is requesting access to this media: &quot;{{ request.note }}&quot;
                <br />
                <a-space>
                    <smart-button type="primary" :action="() => confirm(request.id, true)">Approve</smart-button>
                    <smart-button type="danger" :action="() => confirm(request.id, false)">Reject</smart-button>
                </a-space>
                <br />
                <small class="text-gray-500">
                    <d-date :value="request.createdOn" />
                </small>
            </template>
        </a-alert>
        <a-transfer
            v-if="copyrightLevel === 2"
            :locale="{
                itemUnit: 'player',
                itemsUnit: 'players',
                notFoundContent: 'No player available',
                searchPlaceholder: 'Search player name'
            }"
            :list-style="{
                flex: '1',
                height: '300px'
            }"
            :titles="[' available', ' granted']"
            v-model:target-keys="targetKeys"
            :data-source="result ? result.users.edges.map(e => ({ key: e.node.dbId, ...e.node })) : []"
            show-search
            :filter-option="filterOption"
            :render="renderItem"
        />
    </a-space>
</template>