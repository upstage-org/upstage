<template>
  <SaveButton :loading="loading" @click="send">
    <span class="icon is-small">
      <i class="fas fa-paper-plane"></i>
    </span> Send
  </SaveButton>
  <HorizontalField title="Subject" class="mt-4">
    <Field placeholder="Provide a subject for your email" v-model="subject" />
  </HorizontalField>
  <div class="field is-horizontal recipients">
    <div class="field-label is-normal">
      <label class="label">Receiver</label>
      <p class="help">
        Click on a player's name to move them to the column to the right. Use
        a right-click to move them back to the left.
      </p>
    </div>
    <div class="field-body" style="flex-wrap: wrap">
      <MultiTransferColumn style="width: 100%" :columns="[
        'Available players',
        'To',
        'BCC',
      ]" :data="(users ?? []).filter(u => !!u.email)"
        :renderLabel="(item) => `${item.displayName || item.username} <${item.email}>`"
        :renderValue="(item) => item.dbId" :renderKeywords="
          (item) =>
            `${item.firstName} ${item.lastName} ${item.username} ${item.email} ${item.displayName}`
        " v-model="selectedPlayers" />
      <div class="columns is-fullwidth">
        <div class="column">
          <Field label="Additional receivers - To" placeholder="someone@gmail.com,another@gmail.com"
            help="You can send this notification to email addresses that haven't registered UpStage!"
            v-model="additionalReceivers" />
        </div>
        <div class="column is-narrow">
          <Field label="BCC" placeholder="fyi@someone.else" v-model="additionalBcc" />
        </div>
      </div>
    </div>
  </div>
  <HorizontalField title="Body">
    <RichTextEditor v-model="body" />
  </HorizontalField>
</template>

<script setup>
import { configGraph, userGraph } from '@/services/graphql';
import { useMutation, useQuery } from '@/services/graphql/composable';
import { ref } from 'vue';
import MultiTransferColumn from '@/components/MultiTransferColumn.vue';
import Field from '@/components/form/Field.vue';
import HorizontalField from '@/components/form/HorizontalField.vue';
import SaveButton from '@/components/form/SaveButton.vue';
import { notification } from '@/utils/notification';
import RichTextEditor from '@/components/form/RichTextEditor.vue';

const { nodes: users } = useQuery(userGraph.userList);
const selectedPlayers = ref([])


const subject = ref('');
const body = ref(`<div>
<p>&nbsp;</p>
<p>Thank you and best regards,</p>
</div>
<div><img class="avatar flex-shrink-0 mb-3 mr-3 mb-md-0 mr-md-4" src="https://docs.upstage.live/wp-content/uploads/2021/12/logo-upstage-official-300px.png" alt="@upstage-org" width="100" />
</div>`);
const additionalReceivers = ref('');
const additionalBcc = ref('');

const { save, loading } = useMutation(configGraph.sendEmail);
const send = async () => {
  const selectedRecipientsIds = selectedPlayers.value[0] ?? [];
  const selectedRecipients = users.value.filter(u => selectedRecipientsIds.includes(u.dbId));
  const selectedBccIds = selectedPlayers.value[1] ?? [];
  const selectedBccs = users.value.filter(u => selectedBccIds.includes(u.dbId));
  console.log(selectedRecipients, selectedBccs);
  if (!subject.value) {
    return notification.error('Please provide a subject for your email');
  }
  if (!body.value) {
    return notification.error('Please provide a body for your email');
  }
  if (!selectedRecipients.length && !additionalReceivers.value.trim()) {
    return notification.error('Please select at least one player or provide an email address');
  }
  await save(`Notification has been successfully sent to ${selectedRecipients.map(u => u.displayName || u.username).join(', ')}${additionalReceivers.value.trim() ? ` and ${additionalReceivers.value.trim()}` : ''}!`, {
    subject: subject.value,
    body: body.value,
    recipients: selectedRecipients.map(p => p.email).join(',').concat(additionalReceivers.value ? `,${additionalReceivers.value}` : ''),
    bcc: selectedBccs.map(p => p.email).join(',').concat(additionalBcc.value ? `,${additionalBcc.value}` : ''),
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