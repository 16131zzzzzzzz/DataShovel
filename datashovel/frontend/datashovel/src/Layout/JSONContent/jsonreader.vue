<script setup>
import { ref,onMounted } from 'vue';

const boxesData = ref([]);
onMounted(async () => {
  await fetchJsonData('/text.json')
  .then(function(){
    boxesData.value.sort((a, b) => {
      // Sort by page number
      if (a.page !== b.page) {
        return a.page - b.page;
      }
      
    });
    
  }).then(()=>{
    const renderContext = {
      canvasContext: canvas.getContext('2d'),
      viewport: viewport,
    };

    const rectRenderContext = {
      canvasContext: rectCanvas.getContext('2d'),
    };

    const tempRenderContext = {
      canvasContext: tempCanvas.getContext('2d'),
    };

    // Clear previous boxes
    renderContext.canvasContext.clearRect(0, 0, canvas.width, canvas.height);
    tempRenderContext.canvasContext.clearRect(0, 0, tempCanvas.width, tempCanvas.height);
    rectRenderContext.canvasContext.clearRect(0, 0, rectCanvas.width, rectCanvas.height);
    console.log(boxesData.value);
    boxesData.forEach((box, index) => {
            drawRect(rectRenderContext, box, '#3498db', 2);
          })
  });
});

let scale = 1.3;
async function fetchJsonData(filePath) {
  try {
    const response = await fetch(filePath);
    const jsonData = await response.json();
    for (const key in jsonData) {
        if (jsonData.hasOwnProperty(key)) {
          const entry = jsonData[key];
          for (let i = 0; i < entry.bbox.length; i++) {
            const bbox = entry.bbox[i];
            const [left, top, width, height] = bbox;
            boxesData.value.push({
              left: left / 2.08 * scale,
              top: top / 2.08 * scale,
              width: width / 2.08 * scale,
              height: height / 2.08 * scale,
              page: entry.pageNum,
              content: entry.text[i],
            });
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
    <div class ='DS-json__items' v-for="(item,i) in boxesData">
    <div class="DS-json__items--head">Box {{ i }} on Page {{ item.page }} ({{ item.left}},{{ item.top }},{{ item.width }},{{ item.height }})</div>
      {{ item.content }}
    </div>
  </div>
</template>

<style scoped lang="scss">
@include b(json){
  border: 1px solid #000;
  height: 100vh;
  display: flex;
  flex-direction: column;
  flex :0.35;
  overflow-y: auto;
  @include e(items){
    border: 1px solid #000;
    margin: 20px;
    padding: 20px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
    @include m(head){
      font-size: 9px;
      font-weight: normal;
      margin-bottom: 10px;
    }
  }
}
</style>