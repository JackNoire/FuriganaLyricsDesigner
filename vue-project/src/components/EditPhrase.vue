<script setup>
import { ref, inject, computed } from 'vue'
import { jsonData2Json, isValidListIndex } from '@/utils/json_processing'
import EditPhraseKana from './EditPhraseKana.vue'
import EditPhraseMeaning from './EditPhraseMeaning.vue'
import EditPhraseCombine from './EditPhraseCombine.vue'
import EditPhraseJson from './EditPhraseJson.vue'

const props = defineProps({index: Number});
const { globalJsonData, setGlobalJsonData } = inject('globalJsonData');
const { isGlobalJsonDataUnsaved, set_isGlobalJsonDataUnsaved } = inject('isGlobalJsonDataUnsaved');
const localJsonData = ref(globalJsonData.value);
const jsonObject = computed(() => {
  return jsonData2Json(localJsonData.value);
});
const submitBtnDisabled = ref(true);

const activeTabContent = ref('kana');
function openTab(evt, contentId) {
  var i, tablinks;
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  evt.currentTarget.className += " active";
  activeTabContent.value = contentId;
}

// Emit an event to notify parent component that there are unsaved changes.
const emit = defineEmits(['unsaveChange']);
function onJsonUpdate(jsonData) {
  localJsonData.value = jsonData;
  submitBtnDisabled.value = false;
  emit('unsaveChange', true);
}

function onGlobalJsonUpdate() {
  setGlobalJsonData(localJsonData.value);
  submitBtnDisabled.value = true;
  emit('unsaveChange', false);
  set_isGlobalJsonDataUnsaved(true);
}

</script>

<template>
<div class="overlay">
  <div id="editbox">
    <div class="phrase-preview">
      <span v-for="word_obj in jsonObject.original_text[props.index].phrase">
        <span v-if="['\n', ' '].indexOf(word_obj.word)>=0"></span>
        <span v-else>
          <ruby>{{ word_obj.word }}
            <rt v-if="isValidListIndex(word_obj.kana, word_obj.index)">
              {{ word_obj.kana[word_obj.index] }}
            </rt>
          </ruby>
        </span>
      </span>
      <div class="meaning-preview" v-if="isValidListIndex(jsonObject.original_text[props.index].meaning.list,
        jsonObject.original_text[props.index].meaning.index)">
        {{ jsonObject.original_text[props.index].meaning.word.concat(": ",
          jsonObject.original_text[props.index].meaning.list[
          jsonObject.original_text[props.index].meaning.index]) }}
      </div>
    </div>

    <div class="tab">
      <button class="tablinks active" @click="openTab($event, 'kana')">{{ $t("editTab.editKana") }}</button>
      <button class="tablinks" @click="openTab($event, 'meaning')">{{ $t("editTab.editMeaning") }}</button>
      <button class="tablinks" @click="openTab($event, 'combine')">{{ $t("editTab.combine") }}</button>
      <button class="tablinks" @click="openTab($event, 'json')">{{ $t("editTab.json") }}</button>
    </div>

    <div v-if="activeTabContent=='kana'" class="tabcontent">
      <EditPhraseKana :index="props.index" :json-data="localJsonData" @json-update="onJsonUpdate" />
    </div>
    <div v-else-if="activeTabContent=='meaning'" class="tabcontent">
      <EditPhraseMeaning :index="props.index" :json-data="localJsonData"  @json-update="onJsonUpdate" />
    </div>
    <div v-else-if="activeTabContent=='combine'" class="tabcontent">
      <EditPhraseCombine :index="props.index" :json-data="localJsonData" @json-update="onJsonUpdate" />
    </div>
    <div v-else-if="activeTabContent=='json'" class="tabcontent">
      <EditPhraseJson :index="props.index" :json-data="localJsonData" @json-update="onJsonUpdate" />
    </div>
  </div>
  <button class="submitBtn" @click="onGlobalJsonUpdate" :disabled="submitBtnDisabled">{{ $t('editPhrase.submitChanges') }}</button>
</div>
</template>

<style scoped>
.overlay {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1.5;

  background-color: rgba(0,0,0,0.3);
  width: 100%;
  height: 100%;
}
#editbox {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;

  background-color: white;
  border: solid 1px black;
  width: 80%;
  height: 60%;
  overflow: auto;
}

.phrase-preview {
  width: 100%;
  text-align: center;
  padding-top: 30px;
  padding-bottom: 15px;
  font-size: 30px;
  letter-spacing: 8px;
}
.phrase-preview rt {
  font-size: 18px;
  color: blue;
  letter-spacing: 0px;
}
.meaning-preview {
  font-size: 18px;
  letter-spacing: 0;
  color: #555;
}

.tab {
  overflow: hidden;
  border: 1px solid #ccc;
  background-color: #f1f1f1;
}
.tab button {
  background-color: inherit;
  float: left;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  transition: 0.3s;
  font-size: 17px;
}
.tab button:hover {
  background-color: #ddd;
}
.tab button.active {
  background-color: #ccc;
}
.tabcontent {
  display: block;
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-top: none;
}
.submitBtn {
  position: fixed;
  top: 86%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;

  height: 10%;
  width: auto;
  font-size: 30px;
  padding: 0 100px;
  color: white;
  background-color: #c00;
  box-shadow: 6px 6px #500;
  border: outset 10px black;
  border-radius: 20px;
}
.submitBtn:hover {
  background-color: #f66;
  cursor: pointer;
}
.submitBtn:disabled,
.submitBtn[disabled] {
  background-color: #555;
  box-shadow: 6px 6px #999;
  opacity: 0.5;
  cursor: default;
}
</style>