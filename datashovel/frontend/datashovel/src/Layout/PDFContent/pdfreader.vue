<template>
  <div class="DS-pdf" ref="pdfContainer" @scroll="handleScroll">
    <PDFV :url="pdfUrl" :page-number="pageNumber" @page-change="handlePageChange"/>
    <div v-for="(box, index) in filteredBoxesData" :key="index" class="box" :style="{ left: box.left + 'px', top: box.top + 'px', width: box.width + 'px', height: box.height + 'px' }"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch,computed } from 'vue';
import PDFV from './PDFViewer.vue';
const boxesData = ref([]);
const pageNumber = ref(2); // 默认渲染第一页

const pdfUrl = "/test.pdf"; // PDF 文件的路径

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
    console.log(boxesData.value);
  });
});

let scale = 0.8;
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
              left: left / 2.08 * scale+450,
              top: top / 2.08 * scale+120,
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

watch(pageNumber, (newPage) => {
  console.log('Page number changed:', newPage);
});

// 计算属性，根据页面过滤框的数据
const filteredBoxesData = computed(() => {
  return boxesData.value.filter(box => box.page === pageNumber.value);
});
 
// 监听页面变化事件
function handlePageChange(newPage) {
  pageNumber.value = newPage;
}
</script>

<style scoped lang="scss">
@include b(pdf){
  border: 1px solid #000;
  flex :0.35;
  height: 100vh;
  width: 100vh;
}

.box {
  position: absolute;
  border: 2px solid red; /* 设置框的边框样式 */
}
</style>
