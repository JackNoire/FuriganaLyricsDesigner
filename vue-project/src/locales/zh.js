export default {
  nav: {
    home: "首页",
    translation: "翻译",
    preview: "预览"
  },
  home: {
    uploadtext: "如果想查看之前保存的JSON文件，可以点击下面按钮上传：",
    uploadtext_translation: "如果文本格式为一行日语+一行翻译，可以使用下面的工具：",
    text_textarea: "输入日语原文",
    group_size: "选择每组的行数：",
    text_lineNo: "原文在组中第几行：",
    translation_lineNo: "译文在组中第几行：",
    text_translation_textarea: "输入日语原文+翻译",
    error_msg: "请求后端接口失败！可能由于以下原因：\n1. 访问的是静态网页（如github.io上部署的网页），静态网页无法标注假名，仅可上传JSON文件\n2. 后端服务器未正常运行，请检查uvicorn服务器是否正常运行"
  },
  btn: {
    uploadtext: "标注假名",
    uploadjson: "上传JSON文件",
    uploadtext_translation: "提交原文+译文",
    uploadtranslation: "上传翻译",
    skip: "跳过",
    furiganaToggle: "注音",
    translationToggle: "翻译",
    meaningToggle: "划词",
    export: "导出",
    unsave_warning: "警告：修改未保存！导出JSON文件保存修改。"
  },
  editPhrase: {
    newKana: "添加新注音",
    newMeaning: "添加新释义",
    add: "添加",
    submitChanges: "提交修改",
    cantCombine: "无法合并，因为是最后一个词语",
    previewCombine: "当前词语与下一个词语：",
    confirmCombine: "如果确定合并，请点击下面的按钮：",
    combine: "合并！！！",
    confirmClose: "编辑器中存在还未提交的修改，是否确认退出编辑器？"
  },
  editTab: {
    editKana: "编辑注音",
    editMeaning: "编辑释义",
    combine: "合并单词",
    json: "编辑JSON"
  }
};
