<script setup>
import { ref, inject } from 'vue'
import { saveBlob } from '@/utils/file'

const props = defineProps(['filename']);
const { globalJsonData, setGlobalJsonData } = inject('globalJsonData');
const { isGlobalJsonDataUnsaved, set_isGlobalJsonDataUnsaved } = inject('isGlobalJsonDataUnsaved');

function onClick() {
  const blob = new Blob([globalJsonData.value], { type: 'application/json;charset=utf-8' });
  saveBlob(blob, props.filename);
  set_isGlobalJsonDataUnsaved(false);
}

</script>

<template>
  <button @click="onClick">{{ $t("btn.export") }}<br>JSON</button>
</template>