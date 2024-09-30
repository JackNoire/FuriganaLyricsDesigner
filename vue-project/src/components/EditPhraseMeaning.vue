<script setup>
import { ref, watch } from 'vue'
import { jsonData2Json } from '@/utils/json_processing'

const props = defineProps({index: Number, jsonData: String});
var localJsonObject = jsonData2Json(props.jsonData);
var meaning_obj = ref(localJsonObject.original_text[props.index].meaning);

function onClickDelBtn(index, event) {
  event.preventDefault();

  meaning_obj.value.list.splice(index, 1);
  if (meaning_obj.value.list.length == 0) {
    // If length is 0 after deletion
    meaning_obj.value.index = -1;
  } else if (meaning_obj.value.index == index) {
    // If the deleted meaning is the currently selected one
    meaning_obj.value.index = 0;
  } else if (meaning_obj.value.index > index) {
    // If the deleted index is lower than the currently selected one
    meaning_obj.value.index--;
  }
}

var newMeaning = ref('');
function onClickAddMeaning() {
  if (newMeaning.value.length > 0) {
    meaning_obj.value.list.push(newMeaning.value);
    newMeaning.value = '';
    meaning_obj.value.index = meaning_obj.value.list.length - 1;
  }
}

const emit = defineEmits(['jsonUpdate']);
// Emit an event to notify parent component to update localJsonData
watch(meaning_obj, () => {
  emit('jsonUpdate', JSON.stringify(localJsonObject, null, 2));
}, { deep: true });

</script>

<template>
  <input class="word-input" type="text" v-model="meaning_obj.word" />
  <div v-for="(meaning, index) in meaning_obj.list">
    <input type="radio" :id="'id'+index"
    v-model="meaning_obj.index"
    name="meaning_index" :value="index" />
    <label class="custom-radio" :for="'id'+index">
      {{ meaning }}
      <svg class="delBtn" fill="#000" height="30px" width="30px" @click="onClickDelBtn(index, $event)"
        version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
        viewBox="0 0 290 290" xml:space="preserve">
        <g id="XMLID_24_">
          <g id="XMLID_29_">
            <path d="M265,60h-30h-15V15c0-8.284-6.716-15-15-15H85c-8.284,0-15,6.716-15,15v45H55H25c-8.284,0-15,6.716-15,15s6.716,15,15,15
              h5.215H40h210h9.166H265c8.284,0,15-6.716,15-15S273.284,60,265,60z M190,60h-15h-60h-15V30h90V60z"/>
          </g>
          <g id="XMLID_86_">
            <path d="M40,275c0,8.284,6.716,15,15,15h180c8.284,0,15-6.716,15-15V120H40V275z"/>
          </g>
        </g>
      </svg>
    </label>
  </div>
  <div>
    <textarea class="new-meaning-input" v-model="newMeaning" :placeholder="$t('editPhrase.newMeaning')"></textarea>
    <button class="addMeaningBtn" @click="onClickAddMeaning">{{ $t('editPhrase.add') }}</button>
  </div>
</template>

<style scoped>
.word-input {
  width: calc(100% - 20px);
  font-size: 30px;
  padding: 20px 10px;
}

input[type="radio"] {
  display: none;
}
.custom-radio {
  display: inline-block;
  padding: 10px 30px;
  margin: 5px 10px;
  width: calc(100% - 80px);
  font-size: 22px;
  border: 2px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
  cursor: pointer;
}
input[type="radio"]:checked + .custom-radio {
  background-color: #4CAF50;
  border-color: #4CAF50;
  color: white;
}
.delBtn {
  float: right;
  padding: 5px;
  border-radius: 10px;
  background-color: #fff;
  margin-left: auto;
  margin-right: 0;
  opacity: 0.3;
}
.delBtn:hover {
  opacity: 1;
  cursor: pointer;
}

.new-meaning-input {
  box-sizing: border-box;
  font-size: 22px;
  height: 80px;
  width: 80%;
  padding: 5px 15px;
}
.addMeaningBtn {
  box-sizing: border-box;
  width: 20%;
  height: 80px;
  float: right;
  font-size: 28px;
}
.addMeaningBtn:hover {
  cursor: pointer;
}
</style>