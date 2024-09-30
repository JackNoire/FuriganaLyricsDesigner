<script setup>
import { ref, computed, watch } from 'vue'
import { jsonData2Json, isValidPhraseObjStr } from '@/utils/json_processing'

const props = defineProps({index: Number, jsonData: String});
var localJsonObject = jsonData2Json(props.jsonData);
var phrase_obj_str = ref(JSON.stringify(localJsonObject.original_text[props.index], null, 2));
var is_valid_phrase_obj = computed(() => {
  return isValidPhraseObjStr(phrase_obj_str.value)[0];
});
var is_valid_phrase_obj_msg = computed(() => {
  return isValidPhraseObjStr(phrase_obj_str.value)[1];
});

// Emit an event to notify parent component that json is updated.
const emit = defineEmits(['jsonUpdate']);
watch(phrase_obj_str, (new_phrase_obj_str) => {
  if (is_valid_phrase_obj.value) {
    localJsonObject.original_text[props.index] = JSON.parse(new_phrase_obj_str);
    emit('jsonUpdate', JSON.stringify(localJsonObject, null, 2));
  }
});
</script>

<template>
  <div class="msg" v-if="!is_valid_phrase_obj">
    {{ is_valid_phrase_obj_msg }}
  </div>
  <div class="msg success" v-else>Success</div>
  <textarea rows="16" id="json-edit" :class="{error: !is_valid_phrase_obj}" v-model="phrase_obj_str"></textarea>
</template>

<style scoped>
.msg {
  width: 100%;
  background-color: #ffaaaa;
  box-sizing: border-box;
  padding: 10px;
  border-radius: 10px;
}
.msg.success {
  background-color: #aaffaa;
}

#json-edit {
  resize: none;
  display: block;
  font-size: 18px;
  box-sizing: border-box;
  width: 80%;
  height: auto;
  background-color: #fff;
  transition: background-color 0.7s ease-in-out;
}
#json-edit.error {
  background-color: #fcc;
}
</style>