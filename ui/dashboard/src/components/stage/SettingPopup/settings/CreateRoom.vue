<template>
    <div class="card-header">
        <span class="card-header-title">{{ $t("create_new_meeting_room") }}</span>
    </div>
    <div class="card-content voice-parameters">
        <HorizontalField title="Room name">
            <Field v-model="form.name" required required-message="Room name is required"></Field>
        </HorizontalField>
        <SaveButton @click="createRoom">{{ $t("create_room") }}</SaveButton>
    </div>
</template>

<script>
import Field from "@/components/form/Field";
import SaveButton from "@/components/form/SaveButton";
import { useStore } from "vuex";
import { reactive, computed } from "@vue/reactivity";
import HorizontalField from "@/components/form/HorizontalField.vue";
export default {
    components: { Field, SaveButton, HorizontalField },
    emits: ["close"],
    setup: (props, { emit }) => {
        const store = useStore();
        const stageSize = computed(() => store.getters["stage/stageSize"]);

        const form = reactive({});
        const createRoom = async () => {
            store.commit("stage/CREATE_ROOM", {
                type: 'meeting',
                name: form.name,
                description: "",
                w: stageSize.value.width / 2,
                h: stageSize.value.height / 2,
            });
            emit("close");
        };

        return { form, createRoom };
    },
};
</script>

<style>
</style>