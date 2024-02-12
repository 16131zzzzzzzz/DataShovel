<template>
  <div class="DS-box">
    <div><Head></Head></div>
    <div class="DS-box__bottom">
      <PdfReader></PdfReader>
      <Json></Json>
    </div>
  </div>
</template>

<script setup lang="ts">
import Json from './JSONContent/jsonreader.vue';
import Head from './Head/head.vue';
import PdfReader from './PDFContent/pdfreader.vue';

</script>
<style lang="scss">
  @include b(box){
    @include bfc;
    display: flex;
    flex-direction: column;
    @include e(bottom){
      display: flex;
      flex-direction: row;
      flex:1;
    }
  }
</style>
