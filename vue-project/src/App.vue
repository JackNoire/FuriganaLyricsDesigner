<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref, provide } from 'vue';
import { useI18n } from 'vue-i18n';
const { t, locale } = useI18n();

const globalJsonData = ref('');
function setGlobalJsonData(str) {
  globalJsonData.value=str;
}
provide('globalJsonData', {
  globalJsonData,
  setGlobalJsonData
});

const isGlobalJsonDataUnsaved = ref(false);
function set_isGlobalJsonDataUnsaved(isUnsaved) {
  isGlobalJsonDataUnsaved.value = isUnsaved;
}
provide('isGlobalJsonDataUnsaved', {
  isGlobalJsonDataUnsaved,
  set_isGlobalJsonDataUnsaved
});
window.addEventListener("beforeunload", (event) => {
  if (isGlobalJsonDataUnsaved.value) {
    // Cancel the event as stated by the standard.
    event.preventDefault();
    // Chrome requires returnValue to be set.
    event.returnValue = "";
  }
});

// Store Homepage input text
const input_text = ref('');
provide('input_text', input_text);
const input_text_translation = ref('');
provide('input_text_translation', input_text_translation);
</script>

<template>
<body>
<div>
  <nav>
    <ul>
    <li><RouterLink to="/">{{ $t("nav.home") }}</RouterLink></li>
    <span v-if="globalJsonData.length > 0">
    <li><RouterLink to="/translation">{{ $t("nav.translation") }}</RouterLink></li>
    <li><RouterLink to="/preview">{{ $t("nav.preview") }}</RouterLink></li>
    </span>
    <li style="float: right">
      <a
        @click="locale=(locale=='zh'?'en':'zh')">
        <span v-if="locale=='zh'">Switch to English</span>
        <span v-else-if="locale=='en'">切换至中文</span>
      </a>
    </li>
    </ul>
  </nav>
  <div class="routerview">
    <RouterView />
  </div>
</div>

</body>
</template>

<style scoped>
body>div {
  padding: 0;
  margin: 0;
  background-color: #eee;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

a {
  height: 30px;
}

ul {
  list-style-type: none;
  margin: 0;
  padding-left: 15%;
  padding-right: 15%;
  overflow: hidden;
  background-color: #333;
}

li {
  float: left;
}

li a {
  display: block;
  color: white;
  text-align: center;
  padding: 14px 30px;
  text-decoration: none;
}

/* Change the link color to #111 (black) on hover */
li a:hover {
  background-color: #555;
  cursor: pointer;
}

.routerview {
  margin:0 auto;
  padding-left: 50px;
  padding-right: 50px;
  padding-top: 30px;
  display: block;
  max-width: 100vw;
  width: 60%;
  flex-grow: 1;
  background-color: #fdfdfd;
}
</style>
