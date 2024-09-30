<script setup>
import { ref, inject, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { jsonData2Json, getOriginalText } from '@/utils/json_processing';

const translation_text = defineModel();
const { globalJsonData, setGlobalJsonData } = inject('globalJsonData');
const jsonObject = ref(jsonData2Json(globalJsonData.value));
if (jsonObject.value && jsonObject.value.hasOwnProperty("translation") && 
jsonObject.value.translation) {
  translation_text.value = jsonObject.value.translation;
}

const original_text = ref(getOriginalText(globalJsonData.value));

const router = useRouter();

function onClick(event) {
  jsonObject.value.translation = translation_text.value;
  setGlobalJsonData(JSON.stringify(jsonObject.value, null, 2));
  router.push('/preview');
}

function onSkip(event) {
  router.push('/preview');
}
</script>

<template>
<div style="height: calc(95vh - 70px); max-width: 90vw;">
  <div class="original_div">{{ original_text }}</div>
  <div class="translation_div">
    <textarea v-model="translation_text"></textarea>
    <div>
      <button class="button" @click="onClick">{{ $t("btn.uploadtranslation") }}</button>
      <button class="button skip" @click="onSkip">{{ $t("btn.skip") }}</button>
    </div>
  </div>
</div>
</template>

<style scoped>
.original_div {
  width: 50%;
  float: left;
  box-sizing: border-box;
  padding: 20px;
  padding-bottom: 227px;
  border: solid 1px black;
  background: #f2f2f2;
  height: 100%;
  overflow: scroll;
  white-space: pre-wrap;
  font-size: 18px;
  line-height: 240%;
  text-align: right;
}
.translation_div {
  width: 50%;
  height: 100%;
  float: right;
  background: white;
}
.translation_div>textarea {
  resize: none;
  display: block;
  padding: 5px;
  padding-bottom: 200px;
  margin: 0;
  box-sizing: border-box;
  width: 100%;
  height: calc(100% - 50px);
  font-family: inherit;
  font-size: 18px;
  line-height: 180%;
}
.button {
  background-color: #166aeb;
  display: inline-block;
  border: none;
  color: white;
  margin-left: 30%;
  text-align: center;
  font-size: 18px;
  height: 50px;
  width: 30%;
}
.button:hover {
  background-color: #2e79ed;
  cursor: pointer;
}
.button.skip {
  background-color: transparent;
  padding: 0;
  width: fit-content;
  margin-left: 5%;
  color: #555;
  font-size: 18px;
}
.button.skip:hover {
  color: #000;
}
</style>