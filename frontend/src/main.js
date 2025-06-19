import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css' // Element Plus 样式
import * as ElementPlusIconsVue from '@element-plus/icons-vue' // 导入 Element Plus 图标 (新增)

const app = createApp(App)

// 注册所有 Element Plus 图标 (新增)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(router)
app.use(ElementPlus)

app.mount('#app')