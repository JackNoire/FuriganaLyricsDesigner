<script setup>
import { ref, watch } from 'vue'
import { jsonData2Json } from '@/utils/json_processing'

const props = defineProps({index: Number, jsonData: String});
var localJsonObject = jsonData2Json(props.jsonData);
var word_obj_list = ref(localJsonObject.original_text[props.index].phrase);

function onClickDelBtn(word_index, kana_index, event) {
  event.preventDefault();

  word_obj_list.value[word_index].kana.splice(kana_index, 1);
  if (word_obj_list.value[word_index].kana.length == 0) {
    // If kana length is 0 after deletion
    word_obj_list.value[word_index].index = -1;
  } else if (word_obj_list.value[word_index].index == kana_index) {
    // If the deleted furigana is the currently selected one
    word_obj_list.value[word_index].index = 0;
  } else if (word_obj_list.value[word_index].index > kana_index) {
    // If the deleted index is lower than the currently selected index
    word_obj_list.value[word_index].index--;
  }
}

// newKana stores the user-input furigana
// { word_index: user_input_furigana }
var newKana = ref({});
function onClickAddKana(word_index) {
  if (newKana.value.hasOwnProperty(word_index) && newKana.value[word_index].length > 0) {
    word_obj_list.value[word_index].kana.push(newKana.value[word_index]);
    newKana.value[word_index] = '';   // Clear input text
    word_obj_list.value[word_index].index = word_obj_list.value[word_index].kana.length - 1;
  }
}

const emit = defineEmits(['jsonUpdate']);
// Emit an event to notify parent component to update localJsonData
watch(word_obj_list, () => {
  emit('jsonUpdate', JSON.stringify(localJsonObject, null, 2));
}, { deep: true });

</script>

<template>
  <div class="word-obj-box" v-for="(word_obj, word_index) in word_obj_list">
    <span v-if="['\n', ' '].indexOf(word_obj.word)<0">
      <span class="word">{{ word_obj.word }}</span>
      <span v-for="(kana, kana_index) in word_obj.kana">
        <input type="radio" :id="'id'+word_index+'_'+kana_index" 
        v-model="word_obj_list[word_index].index"
        :name="word_index" :value="kana_index" />
        <label class="custom-radio" :for="'id'+word_index+'_'+kana_index">
          {{ kana }}
          <svg class="delBtn" fill="#000" height="15px" width="15px" @click="onClickDelBtn(word_index, kana_index, $event)"
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
      </span>
      <input class="new-kana-input" type="text" v-model="newKana[word_index]" :placeholder="$t('editPhrase.newKana')" />
      <button class="addKanaBtn" @click="onClickAddKana(word_index)">{{ $t('editPhrase.add') }}</button>
    </span>
  </div>
  <br>
  
</template>

<style scoped>
.word-obj-box {
  border: solid 1px #ccc;
}
.word {
  font-size: 22px;
  margin: 5px 20px;
}
input[type="radio"] {
  display: none;
}
.custom-radio {
  display: inline-block;
  padding: 10px 30px;
  margin: 5px 10px;
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
  padding: 5px;
  border-radius: 10px;
  background-color: #fff;
  margin-left: 30px;
  margin-right: -15px;
  opacity: 0.3;
}
.delBtn:hover {
  opacity: 1;
  cursor: pointer;
}
.new-kana-input {
  font-size: 22px;
  margin-left: 20px;
}
.addKanaBtn {
  height: 35px;
  width: auto;
  font-size: 18px;
  padding: 0 10px;
}
.addKanaBtn:hover {
  cursor: pointer;
}
</style>