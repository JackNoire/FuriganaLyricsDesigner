<script setup>
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'

const { globalJsonData, setGlobalJsonData } = inject('globalJsonData');
const router = useRouter();

function onFileChanged(event) {
  const target = event.target;
  if (target && target.files && target.files[0]) {
    var reader = new FileReader();
    reader.readAsText(target.files[0], "UTF-8");
    reader.onload = function (evt) {
      if (evt.target.result.length < 8192000) {
        setGlobalJsonData(evt.target.result);
        router.push('/preview');
      } else {
        alert("文件过大。file too large.");
      }
    }
    reader.onerror = function (evt) {
      alert("读取文件发生错误。error reading file.");
    }
  }
}

</script>

<template>
  <label class="custom-file-upload">
    <input type="file" @change="onFileChanged" accept="application/json" />
    ☁️&nbsp;{{ $t("btn.uploadjson") }}
  </label>
</template>

<style scoped>
input[type="file"] {
  display: none;
}
.custom-file-upload {
  border: 1px solid #000;
  display: inline-block;
  padding: 10px 30px;
  margin-top: 20px;
  cursor: pointer;
  font-size: 24px;
  color: #fff;
  background-color: #333;
}
.custom-file-upload:hover {
  background-color: #555;
}
</style>