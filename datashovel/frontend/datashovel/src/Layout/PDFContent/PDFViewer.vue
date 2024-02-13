<script setup>
import { watch,onMounted, ref } from 'vue';
const props = defineProps(['url', 'pageNumber']); // 新增pageNumber属性
const pdfUrl = ref(''); // pdf文件地址
const fileUrl = '/pdfjs-4.0.379-dist/web/viewer.html?file='; // pdfjs文件地址

onMounted(() => {
  // 构建包含页数参数的 pdfUrl
  const encodedUrl = encodeURIComponent(props.url);
  const pageParam = props.pageNumber ? `#page=${props.pageNumber}` : ''; // 如果有pageNumber属性，则构建页数参数
  pdfUrl.value = `${fileUrl}${encodedUrl}${pageParam}`;
});
watch(() => props.pageNumber, (newValue, oldValue) => {
  // Handle the prop change here\
  const encodedUrl = encodeURIComponent(props.url);
  const pageParam = `#page=${newValue}`;
  pdfUrl.value = `${fileUrl}${encodedUrl}${pageParam}`;
});
</script>

<template>
  <div class="container">
    <iframe :src="pdfUrl" width="100%" height="100%"></iframe>
  </div>
</template>

<style scoped lang="scss">
.container {
  width: 100%;
  height: 100%;
}
</style>
