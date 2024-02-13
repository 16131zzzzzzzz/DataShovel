<template>
  <div class="DS-box">
    <div class="DS-box__left">
      <Logo></Logo>
      <Workspace></Workspace>
    </div>
    <div class="DS-box__right">
      <div class="DS-box__right--top">empty</div>
      <div class="DS-box__right--bottom">
        <PdfReader></PdfReader>
        <Json></Json>
        <ConfigContent></ConfigContent>
      </div>
    </div>
    <div></div>

  </div>
</template>

<script setup>
import Json from './JSONContent/jsonreader.vue';
import Workspace from './Workspace/Workspace.vue';
import PdfReader from './PDFContent/pdfreader.vue';
import ConfigContent from './ConfigContent/config.vue';
import Logo from './logo/logo.vue';

</script>
<style lang="scss">
  @include b(box){
    @include bfc;
    display: flex;
    flex-direction: row;
    @include e(left){
      flex:0.2;
 
      display: flex;
      flex-direction: column;
    }
    @include e(right){
      display: flex;
      flex-direction: column;
      @include m(top){
        min-height: 60px;
        border: black 1px solid;
      }
      @include m(bottom){
        display: flex;
        flex-direction: row;
      }
    }
  }

</style>
