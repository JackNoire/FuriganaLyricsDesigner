export default {
  nav: {
    home: "Home",
    translation: "Translation",
    preview: "Preview"
  },
  home: {
    uploadtext: "To view a previously saved JSON file, click the button below to upload:",
    uploadtext_translation: "If the text format is a line of Japanese + a line of translation, you can use the tool below:",
    text_textarea: "Input Japanese text",
    group_size: "Lines per group: ",
    text_lineNo: "Japanese line number: ",
    translation_lineNo: "Translation line number: ",
    text_translation_textarea: "Input Japanese + Translation",
    error_msg: "Failed to request the backend interface! This may be due to the following reasons:\n1. Accessing the static webpage (e.g., the webpage deployed on github.io); static webpages cannot Add Furigana and can only Upload JSON File.\n2. The backend server is not running properly. Please check if the uvicorn server is running correctly."
  },
  btn: {
    uploadtext: "Add Furigana",
    uploadjson: "Upload JSON File",
    uploadtext_translation: "Upload Japanese + Translation",
    uploadtranslation: "Upload Translation",
    skip: "Skip",
    furiganaToggle: "Furigana",
    translationToggle: "Translation",
    meaningToggle: "MouseDict",
    export: "Export",
    unsave_warning: "Warning: Changes not saved! Export JSON to save your changes."
  },
  editPhrase: {
    newKana: "Add New Furigana",
    newMeaning: "Add New Meaning",
    add: "ADD",
    submitChanges: "Submit Changes",
    cantCombine: "Cannot combine because it is the last word.",
    previewCombine: "The current word and the next word:",
    confirmCombine: "To combine, click the button below:",
    combine: "COMBINE!!!",
    confirmClose: "There are unsubmitted changes in the editor. Are you sure you want to exit the editor?"
  },
  editTab: {
    editKana: "Edit Furigana",
    editMeaning: "Edit Meaning",
    combine: "Combine Words",
    json: "Edit JSON"
  }
};
  