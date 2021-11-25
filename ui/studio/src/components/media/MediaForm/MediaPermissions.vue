<script setup lang="ts">
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { ref, watchEffect, PropType } from 'vue';
import configs from '../../../config';
import { StudioGraph, User } from '../../../models/studio';

const props = defineProps({
    modelValue: {
        type: Number,
        default: 0,
    },
    users: {
        type: Array as PropType<number[]>,
        default: [],
    },
});

const emits = defineEmits(['update:modelValue', 'update:users']);

const copyrightLevel = ref(0)
const targetKeys = ref(props.users);

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
</script>

<template>
    <a-space direction="vertical" class="w-full">
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