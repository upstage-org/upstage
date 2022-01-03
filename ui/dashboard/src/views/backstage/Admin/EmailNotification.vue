<template>
  <SaveButton :loading="loading" @click="send">
    <span class="icon is-small">
      <i class="fas fa-paper-plane"></i>
    </span>
    Send
  </SaveButton>
  <HorizontalField title="Subject" class="mt-4">
    <Field placeholder="Provide a subject for your email" v-model="subject" />
  </HorizontalField>
  <HorizontalField title="To" class="recipients">
    <MultiSelectList
      :loading="loadingUsers"
      :titles="['Available players:', 'Selected players:']"
      :data="(users ?? []).filter(u => !!u.email)"
      :column-class="() => 'is-12 p-1'"
      v-model="selectedPlayers"
    >
      <template #render="{ item }">
        <div class="p-2">
          <b>{{ item.displayName || item.username }}</b>
          &lt;{{ item.email }}&gt;
        </div>
      </template>
    </MultiSelectList>
    <Field
      label="Additional receivers"
      placeholder="someone@gmail.com,another@gmail.com"
      help="You can send this notification to email addresses that haven't registered UpStage!"
      v-model="additionalReceivers"
    />
  </HorizontalField>
  <HorizontalField title="Body">
    <RichTextEditor v-model="body" />
  </HorizontalField>
</template>

<script setup>
import { configGraph, userGraph } from '@/services/graphql';
import { useMutation, useQuery } from '@/services/graphql/composable';
import { ref } from 'vue';
import MultiSelectList from '@/components/MultiSelectList.vue';
import Field from '@/components/form/Field.vue';
import HorizontalField from '@/components/form/HorizontalField.vue';
import SaveButton from '@/components/form/SaveButton.vue';
import { notification } from '@/utils/notification';
import RichTextEditor from '@/components/form/RichTextEditor.vue';

const { nodes: users, loading: loadingUsers } = useQuery(userGraph.userList);
const selectedPlayers = ref([])


const subject = ref('');
const body = ref(`<div>
<p>&nbsp;</p>
<p>Thank you and best regards,</p>
</div>
<div><img class="avatar flex-shrink-0 mb-3 mr-3 mb-md-0 mr-md-4" src="https://avatars.githubusercontent.com/u/14158792?s=200&amp;v=4" alt="@upstage-org" width="100" height="100" />
</div>`);
const additionalReceivers = ref('');

const { save, loading } = useMutation(configGraph.sendEmail);
const send = async () => {
  console.log(selectedPlayers.value);
  if (!subject.value) {
    return notification.error('Please provide a subject for your email');
  }
  if (!body.value) {
    return notification.error('Please provide a body for your email');
  }
  if (!selectedPlayers.value.length && !additionalReceivers.value.trim()) {
    return notification.error('Please select at least one player or provide an email address');
  }
  await save(`Notification has been successfully sent to ${selectedPlayers.value.map(u => u.displayName || u.username).concat(additionalReceivers.value.trim() || []).join(', ')} !`, {
    subject: subject.value,
    body: body.value,
    recipients: selectedPlayers.value.map(p => p.email).join(',').concat(additionalReceivers.value)
  })
}
</script>

<style lang="scss">
.recipients {
  .container-fluid {
    overflow: visible;
  }
  .columns.is-multiline {
    max-height: 30vh;
    overflow-y: auto;
  }
}
</style>