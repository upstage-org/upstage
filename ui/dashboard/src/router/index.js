import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import store from "@/store";

const routes = [
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    children: [
      {
        path: '/',
        name: 'Home',
        component: Home
      },
      {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue')
      },
      {
        path: '/stage',
        name: 'Stages',
        component: () => import('../views/Stage.vue')
      },
    ]
  },
  {
    path: '/dashboard',
    component: () => import('../views/dashboard/Layout.vue'),
    meta: { requireAuth: true },
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('../views/dashboard/Dashboard.vue'),
      },
      {
        path: '/dashboard/media',
        name: 'Media',
        component: () => import('../views/dashboard/Media.vue'),
      },
      {
        path: '/dashboard/my-stages',
        name: 'My Stages',
        component: () => import('../views/dashboard/MyStages.vue'),
      },
      {
        path: '/dashboard/workshop',
        name: 'Workshop',
        component: () => import('../views/dashboard/Workshop.vue'),
      }
    ]
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const loggedIn = store.getters["auth/loggedIn"] || true;

  if (to.matched.some((record) => record.meta.requireAuth) && !loggedIn) {
    next("/login");
  }
  next();
  document.title = `UpStage ${to.name && '- ' + to.name}`;
});

export default router
