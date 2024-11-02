<script setup>
import { ref, inject, computed, nextTick } from 'vue'
import JsonDownload from './JsonDownload.vue'
import HTMLDownload from './HTMLDownload.vue';
import EditPhrase from './EditPhrase.vue'
import { jsonData2TemplateList } from '@/utils/json_processing'
import { useI18n } from "vue-i18n";
const { t } = useI18n();

const { globalJsonData, setGlobalJsonData } = inject('globalJsonData');
const { isGlobalJsonDataUnsaved, set_isGlobalJsonDataUnsaved } = inject('isGlobalJsonDataUnsaved');
const template_list = computed(() => {
  return jsonData2TemplateList(globalJsonData.value);
});
const showFurigana = ref(true);
const showTranslation = ref(true);
const showMeaning = ref(true);

/**
 * get phrase element closest to screen top
 */
function getTopElement() {
  const elements = document.querySelectorAll('.phrase');
  let closestElement = null;
  let closestDistance = Infinity;

  elements.forEach(element => {
    // distance to viewport top
    const distance = element.getBoundingClientRect().top;
    if (distance > 0 && distance < closestDistance) {
      closestDistance = distance;
      closestElement = element;
    }
  });

  return closestElement;
}

/**
 * toggle Furigana/Translation, scroll after toggle
 * @param type string: "furigana" "translation"
 */
function toggleElement(type) {
  const topElement = getTopElement();
  
  var topElementTop;
  if (topElement) {
    // Element Y (relative to current window top)
    topElementTop = topElement.getBoundingClientRect().top;
  }

  switch (type) {
    case "furigana":
      showFurigana.value = !showFurigana.value;
      break;
    case "translation":
      showTranslation.value = !showTranslation.value;
      break;
  }

  if (topElement) {
    nextTick(() => {
      // New Element Y (relative to current window top)
      const newTopElementTop = topElement.getBoundingClientRect().top;
      window.scrollBy(0, newTopElementTop - topElementTop);
    });
  }
}

const showEditPhrase = ref(false);
const editPhraseIndex = ref(0);
const editUnsaveChange = ref(false);
function onClickPhrase(index) {
  editPhraseIndex.value = index;
  showEditPhrase.value = true;
  editUnsaveChange.value = false;
}
function onClickClosePhrase() {
  if (editUnsaveChange.value) {
    if (confirm(t("editPhrase.confirmClose"))) {
      showEditPhrase.value = false;
    }
  } else {
    showEditPhrase.value = false;
  }
}
</script>

<template>
<div class="render-text" :class="{ furigana: showFurigana }">
  <span v-for="template_obj in template_list">
    <span v-if="template_obj.type=='phrase'" class="phrase">
      <span @click="onClickPhrase(template_obj.index)">
        <span v-for="word_kana in template_obj.content">
          <br v-if="word_kana[0]=='\n'">
          <span v-else-if="word_kana[0]==' '">&nbsp;</span>
          <span v-else>
            <ruby v-if="showFurigana">{{ word_kana[0] }}
              <rt v-if="word_kana[1]">{{ word_kana[1] }}</rt>
            </ruby>
            <span v-else>{{ word_kana[0] }}</span>
          </span>
        </span>
      </span>
      <div v-if="template_obj.meaning&&showMeaning" class="meaning-box">
        <h4>{{ template_obj.meaning[0] }}</h4>
        <p>{{ template_obj.meaning[1] }}</p>
      </div>
    </span>
    <div v-else-if="template_obj.type=='translation'" class="translation" :class="{ furigana: showFurigana }">
      <span v-if="showTranslation">{{ template_obj.content }}</span>
    </div>
  </span>
</div>
<div v-if="isGlobalJsonDataUnsaved" class="unsave-warning">{{ $t("btn.unsave_warning") }}</div>
<button @click="toggleElement('furigana')" class="btn furiganaBtn">{{ $t("btn.furiganaToggle") }}<br>{{ showFurigana?"ON":"OFF" }}</button>
<button @click="toggleElement('translation')" class="btn translationBtn">{{ $t("btn.translationToggle") }}<br>{{ showTranslation?"ON":"OFF" }}</button>
<button @click="showMeaning=!showMeaning" class="btn meaningBtn">{{ $t("btn.meaningToggle") }}<br>{{ showMeaning?"ON":"OFF" }}</button>
<JsonDownload class="btn jsondownloadBtn" filename="export.json" />
<HTMLDownload class="btn htmldownloadBtn" filename="export.html" />

<div v-if="showEditPhrase">
<EditPhrase :index="editPhraseIndex" id="EditPhrase" @unsave-change="(x)=>{editUnsaveChange=x}" />
<button id="btnCloseEditPhrase" @click="onClickClosePhrase">
  <svg viewBox="0 0 145.8244 144.63728" xmlns="http://www.w3.org/2000/svg">
    <defs>
    <linearGradient id="a" x1="-344.15" x2="-395.85" y1="274.71" y2="425.4" gradientTransform="matrix(-.65718 0 0 .65718 -16.966 114.63)" gradientUnits="userSpaceOnUse">
      <stop stop-color="#fff" offset="0"/>
      <stop stop-color="#fff" stop-opacity="0" offset="1"/>
    </linearGradient>
    </defs>
    <g transform="matrix(.9 0 0 .9 -148.35 -279.28)">
    <path transform="scale(-1,1)" d="m-279.33 318.34h66.963a39.431 39.431 0 0 1 39.431 39.431v65.776a39.431 39.431 0 0 1 -39.431 39.431h-66.963a39.431 39.431 0 0 1 -39.431 -39.431v-65.776a39.431 39.431 0 0 1 39.431 -39.431" fill="#f00a10" fill-rule="evenodd"/>
    <g transform="matrix(.65718 0 0 .65718 -102.64 -95.387)">
      <path d="m554.13 739.6 35.778-35.778c3.7481-3.7483 5.6222-7.894 5.6222-12.437-0.22723-4.089-2.1013-7.8939-5.6222-11.415-3.1803-3.1803-6.9284-4.9976-11.244-5.4518-4.4297-0.34085-8.6321 1.4764-12.607 5.4518l-35.778 35.778-35.778-35.778c-3.6345-3.6347-7.7234-5.452-12.267-5.4518-4.4296 0.34063-8.2913 2.1579-11.585 5.4518-2.8394 2.8394-4.4864 6.5307-4.9408 11.074-0.45425 4.7702 1.1927 9.0295 4.9408 12.778l35.778 35.778-35.778 35.778c-3.1802 3.18-4.9407 7.3257-5.2815 12.437 0.34082 4.4294 2.1013 8.2343 5.2815 11.415 2.9531 2.9529 6.7013 4.7701 11.244 5.4519 4.4297 0.34051 8.6321-1.4768 12.607-5.4519l35.778-35.778 35.778 35.778c3.7481 3.7479 7.8938 5.3948 12.437 4.9407 4.6567-0.34096 8.4617-1.9879 11.415-4.9407 2.7259-2.7262 4.3728-6.4175 4.9407-11.074 0.68142-4.5434-0.96549-8.8027-4.9407-12.778l-35.778-35.778" fill="#cb1e0e"/>
      <path d="m552.28 739.6 32.987-32.987c3.4557-3.4559 5.1836-7.2782 5.1837-11.467-0.2095-3.7701-1.9374-7.2782-5.1837-10.524-2.9322-2.9323-6.388-4.6078-10.367-5.0266-4.0842-0.31426-7.9588 1.3613-11.624 5.0266l-32.987 32.987-32.987-32.987c-3.351-3.3512-7.121-5.0267-11.31-5.0266-4.0841 0.31406-7.6446 1.9896-10.682 5.0266-2.618 2.6179-4.1364 6.0214-4.5554 10.21-0.41882 4.3982 1.0996 8.3252 4.5554 11.781l32.987 32.987-32.987 32.987c-2.9321 2.932-4.5553 6.7543-4.8695 11.467 0.31423 4.0839 1.9374 7.5921 4.8695 10.524 2.7228 2.7226 6.1786 4.3981 10.367 5.0266 4.0842 0.31395 7.9588-1.3616 11.624-5.0266l32.987-32.987 32.987 32.987c3.4558 3.4556 7.2781 4.974 11.467 4.5554 4.2935-0.31437 7.8017-1.8328 10.524-4.5554 2.5132-2.5135 4.0317-5.917 4.5554-10.21 0.62827-4.189-0.89018-8.1161-4.5554-11.781l-32.987-32.987" fill="#fff"/>
    </g>
    <path d="m280.23 324.53h-68.771c-18.204 0-32.859 14.655-32.859 32.859v66.553c0.58922 14.21 2.8558 5.2266 7.17-10.51 5.014-18.289 21.343-34.273 41.229-46.253 15.178-9.1435 32.168-14.982 63.093-15.538 17.539-0.31499 15.99-22.579-9.863-27.112z" fill="url(#a)" fill-rule="evenodd"/>
    </g>
  </svg>
</button>
</div>
</template>

<style scoped>
.render-text {
  display: block;
  font-size: 22px;
  line-height: 120%;
  letter-spacing: 2.5px;
  padding: 30px;
  padding-bottom: 500px;
}

.render-text.furigana {
  line-height: 250%;
}

rt {
  font-size: 18px;
  color: blue;
  letter-spacing: 0px;
}

.meaning-box {
  display: none;

  width: 200px;
  border: 1px solid black;
  font-size: 18px;
  background-color: rgba(0, 0, 0, 0.9);
  color: white;
  
  line-height: 120%;
  letter-spacing: 0px;

  padding-top: -10px;
  padding-bottom: -5px;
  padding-left: 10px;
  padding-right: 10px;

  position: absolute;
  float: left;
  top: 120%;
  left: 0%;
  z-index: 1;
}

.phrase {
  position: relative;
}

.phrase:hover {
  background-color: #ccc;
  cursor: pointer;
}

.phrase:hover .meaning-box {
  display: inline;
}

.translation {
  font-size: 18px;
  line-height: 120%;
  letter-spacing: 2px;
  margin-top: 5px;
  margin-bottom: 20px;
  color: #f66;
}
.translation.furigana {
  margin-top: -10px;
}

.unsave-warning {
  position: fixed;
  height: auto;
  width: 120px;
  max-width: 7vw;
  padding: 20px;
  left: 0px;
  top: 100px;
  font-size: 16px;
  line-height: 160%;
  color: #b22;
  background-color: #fdd;
  border: solid 1px #b22;
  border-radius: 10px;
}
.btn {
  position: fixed;
  height: 60px;
  width: 120px;
  right: 20px;
  font-size: 20px;
  color: white;
}
.btn:hover {
  cursor: pointer;
}
.btn.furiganaBtn {
  top: 100px;
  background-color: #00c;
}
.btn.furiganaBtn:hover {
  background-color: #11d;
}
.btn.translationBtn {
  top: 180px;
  background-color: #f66;
}
.btn.translationBtn:hover {
  background-color: #f77;
}
.btn.meaningBtn {
  top: 260px;
  background-color: #333;
}
.btn.meaningBtn:hover {
  background-color: #555;
}
.btn.jsondownloadBtn {
  top: 400px;
  background-color: #f60;
}
.btn.jsondownloadBtn:hover {
  background-color: #f82;
}
.btn.htmldownloadBtn {
  top: 480px;
  background-color: #070;
}
.btn.htmldownloadBtn:hover {
  background-color: #090;
}
#btnCloseEditPhrase {
  position: fixed;
  height: 60px;
  width: 60px;
  right: 10%;
  top: calc(20% - 60px);

  background-color: rgba(0,0,0,0);
  border: none;
  cursor: pointer;

  z-index: 2;
}
#btnCloseEditPhrase svg {
  position: relative;
  height: 67px;
  width: 67px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  opacity: 0.7;
}
#btnCloseEditPhrase svg:hover {
  opacity: 1;
}
</style>