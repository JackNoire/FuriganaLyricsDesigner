<script setup>
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'

const { globalJsonData, setGlobalJsonData } = inject('globalJsonData');
const router = useRouter();

const text = inject('input_text');
const showError = ref(false);
const errorMsg = ref('');
function onClick() {
  if (text.value.length > 0) {
    fetch(import.meta.env.VITE_API_URL, {
      method: "POST",
      cache: "no-cache",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({"string": text.value})
    })
    .then(response => response.json())
    .then((data) => {
      setGlobalJsonData(JSON.stringify(data));
      router.push('/translation');
    })
    .catch(error => {
      console.error('Error:', error);
      showError.value = true;
    });
  }
}
</script>

<template>
  <textarea v-model="text" rows="16" :placeholder="$t('home.text_textarea')"></textarea>
  <button class="btn" @click="onClick">{{ $t("btn.uploadtext") }}</button>
  <div class="errorMsg" v-if="showError">{{ $t('home.error_msg') }}</div>
</template>

<style scoped>
textarea {
  resize: none;
  display: block;
  padding: 5px;
  box-sizing: border-box;
  width: 80%;
  height: auto;
  font-family: inherit;
  font-size: 18px;
  line-height: 120%;
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