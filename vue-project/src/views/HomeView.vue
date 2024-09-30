<script setup>
import UploadText from '../components/UploadText.vue';
import UploadFile from '../components/UploadFile.vue';
import UploadTextTranslation from '@/components/UploadTextTranslation.vue';
</script>

<template>
<div>
  <UploadText /><br>
  <hr>
  {{ $t("home.uploadtext") }}<br>
  <UploadFile />
  <br><br>
  <hr>
  {{ $t("home.uploadtext_translation") }}
  <br><br>
  <UploadTextTranslation />
  <br><br>
</div>
</template>

<style scoped>
div {
  font-size: 20px;
}
</style>
