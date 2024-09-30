<script setup>
import { inject } from 'vue'
import RenderText from '../components/RenderText.vue'

const { globalJsonData, setGlobalJsonData } = inject('globalJsonData');

</script>

<template>
  <RenderText />
</template>