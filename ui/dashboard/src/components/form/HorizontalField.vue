<template>
  <div class="field is-horizontal">
    <div class="field-label is-normal">
      <label class="label">{{ title }} <span style="color: #ff0000" data-tooltip="Required" v-if="required">*</span></label>
    </div>
    <div class="field-body">
      <div class="field">
        <slot />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["title" , "required"],
};
</script>

<style>
</style>