<template>
  <div class="crawler-example-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>豆瓣电影 Top250</span>
          <el-button type="primary" @click="startCrawler">开始爬取</el-button>
        </div>
      </template>
      <div class="movie-list">
        <el-empty v-if="movies.length === 0 && !isLoading" description="暂无数据，请点击开始爬取"></el-empty>
        <div v-else-if="isLoading" class="loading-overlay">
          <el-icon class="is-loading" size="50px"><Loading /></el-icon>
          <p>正在爬取中，请稍候...</p>
        </div>
        <el-row :gutter="20" v-else>
          <el-col :span="6" v-for="movie in movies" :key="movie.title" class="movie-item">
            <el-card :body-style="{ padding: '10px' }" shadow="hover">
              <img :src="movie.image_path" class="image" :alt="movie.title" />
              <div style="padding: 14px;">
                <div class="movie-title">{{ movie.title }}</div>
                <div class="movie-rating">
                  <el-rate :model-value="movie.rating / 2" disabled show-score text-color="#ff9900" score-template="{value}"></el-rate>
                </div>
                <div class="movie-eval-people">评价人数: {{ movie.eval_people }}</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import axios from 'axios';
import { Loading } from '@element-plus/icons-vue'; // Import Loading icon

const movies = ref([]);
const isLoading = ref(false);

const startCrawler = async () => {
  isLoading.value = true;
  movies.value = []; // Clear previous movie data
  try {
    const response = await axios.post('/api/start_crawler');
    if (response.data.code === 200) {
      movies.value = response.data.movies;
      ElMessage.success('电影数据爬取成功！');
    } else {
      ElMessage.error(response.data.message || '爬取失败');
    }
  } catch (error) {
    console.error('Crawler request failed:', error);
    ElMessage.error('服务器错误或网络问题，请稍后再试。');
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.crawler-example-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 20px;
}

.box-card {
  width: 90%;
  max-width: 1200px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.movie-list {
  padding: 20px;
  min-height: 300px; /* Ensure minimum height */
  position: relative; /* For loading animation positioning */
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.movie-item {
  margin-bottom: 20px;
}

.image {
  width: 100%;
  height: 250px; /* Fixed image height */
  object-fit: cover; /* Crop image to fill */
  display: block;
}

.movie-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.movie-rating {
  margin-bottom: 5px;
}

.movie-eval-people {
  font-size: 13px;
  color: #606266;
}
</style>