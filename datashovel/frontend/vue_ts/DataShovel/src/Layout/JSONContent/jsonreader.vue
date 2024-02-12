<script setup lang="ts">
import { reactive,onMounted } from 'vue';
let boxesData=reactive<boxdata>([]);
onMounted(async () => {
  await fetchJsonData('/text.json');
});
interface boxdata {
  page : number ,
  content: string
}
async function fetchJsonData(filePath:string) {
  try {
    const response = await fetch(filePath);
    const jsonData = await response.json();
    for (const key in jsonData) {
        if (jsonData.hasOwnProperty(key)) {
          const entry = jsonData[key];
          for (let i = 0; i < entry.bbox.length; i++) {
            let box_data: boxdata = {
              page: 0,
              content: ''
            };
            boxesData.value.push(box_data);
          }
        }
      }
  } catch (error) {
    console.error('Error reading JSON file', error);
  }
}
</script>

<template>
  <div class="DS-json">
    <div class ='DS-json__items' v-for="item in boxesData">{{ item.content }}</div>
  </div>
</template>

<style scoped lang="scss">
@include b(json){
  border: 1px solid #000;
  display: flex;
  flex-direction: column;
  flex :0.5;
  overflow-y: auto;
  @include e(items){
    border: 1px solid #000;
    margin: 10px;
    padding: 20px;
    border-radius: 4px;
  }
}
</style>