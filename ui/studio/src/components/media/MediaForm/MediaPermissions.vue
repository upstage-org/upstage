<script setup>import configs from '../../../config';

</script>

<template>
    <a-space>
        <a-select class="w-full" placeholder="Media copyright level">
            <a-select-option
                v-for="level in configs.MEDIA_COPYRIGHT_LEVELS"
                :key="level.value"
                :value="level.value"
            >{{ level.name }}</a-select-option>
        </a-select>Users has permissions
    </a-space>
</template>