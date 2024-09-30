<script setup>
import { ref, inject, watch } from 'vue'
import { useRouter } from 'vue-router'

const groupSize = ref(2);
const textIndex = ref(0);
const translationIndex = ref(1);
const text_translation = inject('input_text_translation');

watch(groupSize, (newGroupSize) => {
  if (textIndex.value >= newGroupSize) {
    textIndex.value = newGroupSize - 1;
  }
  if (translationIndex.value >= newGroupSize) {
    translationIndex.value = newGroupSize - 1;
  }
  if (textIndex.value == translationIndex.value) {
    if (textIndex.value > 0) {
      textIndex.value--;
    } else {
      translationIndex.value++;
    }
  }

  document.getElementById("textIndex").style.width = (3*newGroupSize).toString() + "%";
  document.getElementById("translationIndex").style.width = (3*newGroupSize).toString() + "%";
});

const { globalJsonData, setGlobalJsonData } = inject('globalJsonData');
const router = useRouter();
const showError = ref(false);
function onClick() {
  var lines = text_translation.value.split('\n');
  var text = "";
  var translation = "";
  for (var i = 0; i < lines.length; i++) {
    if (i % groupSize.value == textIndex.value) {
      text += "\n" + lines[i];
    }
    if (i % groupSize.value == translationIndex.value) {
      translation += "\n" + lines[i];
    }
  }
  text = text.substring(1);
  translation = translation.substring(1);
  if (text.length > 0) {
    fetch(import.meta.env.VITE_API_URL, {
      method: "POST",
      cache: "no-cache",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({"string": text})
    })
    .then(response => response.json())
    .then((data) => {
      data["translation"] = translation;
      setGlobalJsonData(JSON.stringify(data));
      router.push('/preview');
    })
    .catch(error => {
      console.error('Error:', error);
      showError.value = true;
    });
  }
}

</script>

<template>
  <div class="selectContainer">
    <label for="groupSize">{{ $t("home.group_size") }}</label>
    <input type="range" id="groupSize" v-model.number="groupSize" min="2" max="10" step="1" list="groupSizeList">
    <span>{{ groupSize }}</span>
  </div>
  <datalist id="groupSizeList">
    <option v-for="i in 9" :value="i+1"></option>
  </datalist>

  <div class="selectContainer">
    <label for="textIndex" style="background-color: #cfc;">{{ $t("home.text_lineNo") }}</label>
    <input type="range" id="textIndex" v-model.number="textIndex" min="0" :max="groupSize-1" step="1" list="indexList">
    <span>{{ textIndex+1 }}</span>
  </div>

  <div class="selectContainer">
    <label for="translationIndex" style="background-color: #fcc;">{{ $t("home.translation_lineNo") }}</label>
    <input type="range" id="translationIndex" v-model.number="translationIndex" min="0" :max="groupSize-1" step="1" list="indexList">
    <span>{{ translationIndex+1 }}</span>
  </div>

  <datalist id="indexList">
    <option v-for="i in groupSize" :value="i-1"></option>
  </datalist>
  
  <div style="height: calc(75vh - 100px); max-width: 90vw;">
    <textarea class="input_textarea" v-model="text_translation" :placeholder="$t('home.text_translation_textarea')"></textarea>
    <div id="preview">
      <div v-for="(line, index) in text_translation.split('\n')"
      :class="{ 
        'text': index % groupSize == textIndex,
        'translation': index % groupSize == translationIndex
      }">{{ line }}<br></div>
    </div>
  </div>

  <button class="btn" @click="onClick">{{ $t("btn.uploadtext_translation") }}</button>

  <div class="errorMsg" v-if="showError">{{ $t('home.error_msg') }}</div>

</template>

<style scoped>
label {
  width: 30px;
}

.selectContainer {
  margin-bottom: 5px;
  font-family: inherit;
  font-size: 18px;
}
.selectContainer #groupSize {
  width: 30%;
}
.selectContainer #textIndex {
  width: 6%;
}
.selectContainer #translationIndex {
  width: 6%;
}

.input_textarea {
  width: 50%;
  height: 100%;
  float: left;
  resize: none;
  display: block;
  padding: 5px;
  box-sizing: border-box;
  font-family: inherit;
  font-size: 16px;
  line-height: 120%;
}

#preview {
  width: 50%;
  height: 100%;
  float: right;
  resize: none;
  display: block;
  overflow: scroll;
}

#preview>div {
  font-size: 16px;
  line-height: 150%;
}

#preview .text {
  background-color: #cfc;
}

#preview .translation {
  background-color: #fcc;
}

#preview .text.translation {
  background-color: #daa;
}

.btn {
  border: 1px solid #000;
  display: inline-block;
  padding: 10px 30px;
  margin-top: 10px;
  cursor: pointer;
  font-size: 24px;
  color: #fff;
  background-color: #333;
}
.btn:hover {
  background-color: #555;
}

.errorMsg {
  white-space: pre-line;
  font-size: 16px;
  background-color: #fcc;
  margin-top: 10px;
  padding: 5px;
  line-height: 160%;
}
</style>