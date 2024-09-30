<script setup>
import { ref, inject } from 'vue'
import { jsonData2TemplateList } from '@/utils/json_processing'
import { saveBlob } from '@/utils/file'

const props = defineProps(['filename']);
const { globalJsonData, setGlobalJsonData } = inject('globalJsonData');

function onClick() {
  const template_list = jsonData2TemplateList(globalJsonData.value);
  var iframe = document.getElementById('ifrm');
  var iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
  if (!iframeDocument) {
    return;
  }
  var render_text = iframeDocument.getElementById('render-text');
  render_text.innerHTML = '';

  template_list.forEach(template_obj => {
    if (template_obj.type == 'phrase') {
      var phrase_span = document.createElement('span');
      phrase_span.className = 'phrase';

      // Children of <span class="phrase">
      // Word and Kana
      template_obj.content.forEach(word_kana => {
        if (word_kana[0] == '\n') {
          phrase_span.innerHTML = '<br>';
          return;
        }
        if (word_kana[0] == ' ') {
          phrase_span.innerHTML = '&nbsp;';
          return;
        }

        var ruby = document.createElement('ruby');
        ruby.textContent = word_kana[0];
        if (word_kana[1]) {
          var rt = document.createElement('rt');
          rt.textContent = word_kana[1];
          ruby.appendChild(rt);
        }
        phrase_span.appendChild(ruby);

        var span = document.createElement('span');
        span.textContent = word_kana[0];
        phrase_span.appendChild(span);
      });
      // Meaning
      if (template_obj.meaning) {
        var meaning_div = document.createElement('div');
        meaning_div.className = 'meaning-box';
        
        var h4 = document.createElement('h4');
        h4.textContent = template_obj.meaning[0];
        meaning_div.appendChild(h4);
        var p = document.createElement('p');
        p.textContent = template_obj.meaning[1];
        meaning_div.appendChild(p);

        phrase_span.appendChild(meaning_div);
      }
      
      render_text.appendChild(phrase_span);
    // endif type == 'phrase'
    } else if (template_obj.type == 'translation') {
      var translation_div = document.createElement('div');
      translation_div.className = 'translation';
      translation_div.textContent = template_obj.content;

      render_text.appendChild(translation_div);
    }
  }); // end template_list.forEach

  // Save the html data
  const blob = new Blob(["<!doctype html>\n" + iframeDocument.documentElement.outerHTML], { type: 'text/html;charset=utf-8' });
  saveBlob(blob, props.filename);
}
</script>

<template>
<button @click="onClick">
  {{ $t("btn.export") }}<br>HTML
  <iframe id="ifrm" src="./html-templates/template.html" style="display: none;"></iframe>
</button>
</template>

<style scoped>
</style>