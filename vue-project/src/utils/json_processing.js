export function jsonData2Json(jsonstr) {
  try {
    return JSON.parse(jsonstr);
  } catch (e) {
    return null;
  }
}

/**
 * convert json data string to template list, for vue template to parse
 * @param jsonstr 
 * @returns a list
 * [{"type": "phrase", "content": [["word","kana"], ["word","kana"]], "meaning": ["word","meaning"], "index": 0},
 * {"type": "translation", "content": "..."}]
 */
export function jsonData2TemplateList(jsonstr) {
  var jsonObject = jsonData2Json(jsonstr);
  if (jsonObject === null) {
    return [];
  }

  var translation = [];
  if (jsonObject && jsonObject.hasOwnProperty("translation") && 
  jsonObject.translation) {
    translation = jsonObject.translation.split('\n');
  }
  var template_list = [];
  var translation_index = 0;
  var index = 0;
  jsonObject.original_text.forEach(phrase_obj => {
    var template_obj = {
      "type": "phrase",
      "content": [],
      "meaning": null,
      "index": index
    };
    index++;
    var newlineFlag = false;
    phrase_obj.phrase.forEach(word_obj => {
      var kana = "";
      if (word_obj.index>=0 && word_obj.index<word_obj.kana.length) {
        kana = word_obj.kana[word_obj.index];
      }
      template_obj.content.push([word_obj.word, kana]);

      if (word_obj.word == "\n") {
        newlineFlag = true;
      }
    });
    if (phrase_obj.meaning.index>=0 && phrase_obj.meaning.index < phrase_obj.meaning.list.length) {
      template_obj.meaning = 
        [phrase_obj.meaning.word, phrase_obj.meaning.list[phrase_obj.meaning.index]];
    }
    template_list.push(template_obj);
    if (newlineFlag && translation_index < translation.length) {
      template_list.push({
        "type": "translation",
        "content": translation[translation_index]
      });
      translation_index++;
    }
  });
  return template_list;
}

export function getOriginalText(jsonstr) {
  var jsonObject = jsonData2Json(jsonstr);
  if (jsonObject === null) {
    return '';
  }
  var result = '';
  jsonObject.original_text.forEach(phrase_obj => {
    phrase_obj.phrase.forEach(word_obj => {
      result += word_obj.word;
    });
  });
  return result;
}

/**
 * Check if index is valid for the list
 * @param {Array} list 
 * @param {Number} index 
 * @returns true if is valid, else false
 */
export function isValidListIndex(list, index) {
  return index >= 0 && index < list.length;
}

/**
 * Check if phrase_obj_str is valid
 * @param {String} phrase_obj_str 
 * @returns {(Boolean, String)[]} [isValid, msg] true if is valid, else false
 */
export function isValidPhraseObjStr(phrase_obj_str) {
  try {
    return __isValidPhraseObjStr(phrase_obj_str);
  } catch (e) {
    return [false, "Unknown Error"];
  }
}

function __isValidPhraseObjStr(phrase_obj_str) {
  var i, j;
  var phrase_obj = jsonData2Json(phrase_obj_str);
  if (phrase_obj === null) {
    return [false, "JSON Parse Error"];
  }
  if (typeof(phrase_obj) !== 'object' || Array.isArray(phrase_obj)) {
    return [false, "Type Error: not a key-value object"];
  }
  if (!phrase_obj.hasOwnProperty("phrase")) {
    return [false, "Missing Key \"phrase\""];
  }
  if (!phrase_obj.hasOwnProperty("meaning")) {
    return [false, "Missing Key \"meaning\""];
  }
  if (!Array.isArray(phrase_obj.phrase)) {
    return [false, "Type Error: phrase is not an array"];
  }
  for (i = 0; i < phrase_obj.phrase.length; i++) {
    var word_obj = phrase_obj.phrase[i];
    if (typeof(word_obj) !== 'object' || Array.isArray(word_obj)) {
      return [false, "Type Error: phrase element is not a key-value object"];
    }
    if (!word_obj.hasOwnProperty("word") || typeof(word_obj.word) !== 'string') {
      return [false, "Error: phrase element.word"];
    }
    if (!word_obj.hasOwnProperty("kana") || !Array.isArray(word_obj.kana)) {
      return [false, "Error: phrase element.kana"];
    }
    if (!word_obj.hasOwnProperty("index") || typeof(word_obj.index) !== 'number') {
      return [false, "Error: phrase element.index"];
    }
    for (j = 0; j < word_obj.kana.length; j++) {
      if (typeof(word_obj.kana[j]) !== 'string') {
        return [false, "Type Error: phrase element.kana is not a string array"];
      }
    }
  }
  if (typeof(phrase_obj.meaning) !== 'object' || Array.isArray(phrase_obj.meaning)) {
    return [false, "Type Error: meaning is not a key-value object"];
  }
  if (!phrase_obj.meaning.hasOwnProperty("word") || typeof(phrase_obj.meaning.word) !== 'string') {
    return [false, "Error: meaning.word"];
  }
  if (!phrase_obj.meaning.hasOwnProperty("list") || !Array.isArray(phrase_obj.meaning.list)) {
    return [false, "Error: meaning.list"];
  }
  if (!phrase_obj.meaning.hasOwnProperty("index") || typeof(phrase_obj.meaning.index) !== 'number') {
    return [false, "Error: meaning.index"];
  }
  for (i = 0; i < phrase_obj.meaning.list.length; i++) {
    if (typeof(phrase_obj.meaning.list[i]) !== 'string') {
      return [false, "Type Error: meaning.list element is not a string"];
    }
  }
  return [true, ""];
}