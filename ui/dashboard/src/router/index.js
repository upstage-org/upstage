import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import store from "@/store";
import config from '../../vue.config';

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
      },
      {
        path: '/dashboard/profile',
        name: 'Player Profile',
        component: () => import('../views/dashboard/Profile.vue'),
      },
      {
        path: '/dashboard/stage-management',
        component: () => import('../views/dashboard/StageManagement/index.vue'),
        children: [
          {
            name: 'Stage Management',
            path: '/dashboard/stage-management',
            component: () => import('../views/dashboard/StageManagement/General.vue'),
          },
          {
            name: 'Stage Layout',
            path: '/dashboard/stage-management/layout',
            component: () => import('../views/dashboard/StageManagement/Layout.vue'),
          },
          {
            name: 'Scenes',
            path: '/dashboard/stage-management/scenes',
            component: () => import('../views/dashboard/StageManagement/Scenes.vue'),
          }
        ]
      }
    ]
  },

  {
    path: '/live',
    component: () => import('../views/live/Layout.vue'),
    children: [
      {
        path: '/live',
        name: 'Live',
        component: () => import('../views/live/Live.vue'),
      },
    ]
  },
]

const router = createRouter({
  history: createWebHistory(config.publicPath),
  routes
})

router.beforeEach((to, from, next) => {
  const loggedIn = store.getters["auth/loggedIn"];

  if (to.matched.some((record) => record.meta.requireAuth) && !loggedIn) {
    next("/login");
  }
  if (to.name === 'Login' && loggedIn) {
    next("/dashboard");
  }
  next();
  document.title = `UpStage ${to.name && '- ' + to.name}`;
});

export default router
