<script setup>
import { ref } from 'vue'
import { jsonData2Json } from '@/utils/json_processing'

const props = defineProps({index: Number, jsonData: String});
var localJsonObject = jsonData2Json(props.jsonData);

const emit = defineEmits(['jsonUpdate']);
function onClickCombine() {
  // Combine phrase array
  localJsonObject.original_text[props.index].phrase =
    localJsonObject.original_text[props.index].phrase.concat(
      localJsonObject.original_text[props.index+1].phrase);
  // Set meaning.word
  localJsonObject.original_text[props.index].meaning.word = '';
  localJsonObject.original_text[props.index].phrase.forEach((word_obj) => {
    localJsonObject.original_text[props.index].meaning.word += word_obj.word;
  });
  // Delete the index+1 phrase_obj
  localJsonObject.original_text.splice(props.index+1, 1);
  // Emit an event to notify parent component to update localJsonData
  emit('jsonUpdate', JSON.stringify(localJsonObject, null, 2));
}

</script>

<template>
  <div class="combine-box">
  <div v-if="props.index == localJsonObject.original_text.length-1">
    {{ $t("editPhrase.cantCombine") }}
  </div>
  <div v-else>
    <div>
      {{ $t("editPhrase.previewCombine") }}
    </div>
    <span v-for="word_obj in localJsonObject.original_text[props.index].phrase"
    style="background-color: lightpink;">
      <span v-if="word_obj.word=='\n'">
        ↩️
      </span>
      <span v-else-if="word_obj.word==' '">
        &nbsp;
      </span>
      <span v-else>
        {{ word_obj.word }}
      </span>
    </span>
    <span v-for="word_obj in localJsonObject.original_text[props.index+1].phrase"
    style="background-color: lightblue;">
      <span v-if="word_obj.word=='\n'">
        ↩️
      </span>
      <span v-else-if="word_obj.word==' '">
        &nbsp;
      </span>
      <span v-else>
        {{ word_obj.word }}
      </span>
    </span>
    <div>
      {{ $t("editPhrase.confirmCombine") }}
    </div>
    <button class="combineBtn" @click="onClickCombine">
      {{ $t("editPhrase.combine") }}
    </button>
  </div>
  </div>
</template>

<style scoped>
.combine-box {
  font-size: 22px;
  line-height: 150%;
}

.combineBtn {
  font-size: 22px;
  padding: 10px 20px;
  margin: 10px;
}
.combineBtn:hover {
  cursor: pointer;
}
</style>