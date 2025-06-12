import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import AppLayout from '../App.vue' // App.vue now acts as layout component
import HomeContent from '../components/Home.vue' // Home.vue is now HomeContent
import Register from '../components/Register.vue'
import PersonalInformation from '../components/PersonalInformation.vue'
import CrawlerExample from '../components/CrawlerExample.vue' // Import crawler example component

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/main', // New main layout route, all pages needing sidebar navigation are its children
    name: 'MainLayout',
    component: AppLayout, // Use App.vue as the layout component
    redirect: '/main/home', // Default redirect to /main/home
    children: [
      {
        path: 'home', // Access path is /main/home
        name: 'Home',
        component: HomeContent, // Use HomeContent as the home page content component
        meta: { requiresAuth: true, title: '主页' } // Route meta information
      },
      {
        path: 'crawler-example', // Access path is /main/crawler-example
        name: 'CrawlerExample',
        component: CrawlerExample,
        meta: { requiresAuth: true, title: '爬虫示例' }
      },
      {
        path: 'personal-information', // Access path is /main/personal-information
        name: 'PersonalInformation',
        component: PersonalInformation,
        meta: { requiresAuth: true, title: '个人信息' } // New personal information route
      }
    ]
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  // Redirect any unmatched routes back to login or home, depending on requirements
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('isLoggedIn') === 'true';

  // If target route requires authentication but user is not logged in, redirect to login page
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/');
  } else {
    next();
  }
});

export default router