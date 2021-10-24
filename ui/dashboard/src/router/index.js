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
        path: '/register',
        name: 'Register',
        component: () => import('../views/Register.vue')
      },
    ]
  },
  {
    path: '/backstage',
    name: 'Backstage',
    component: () => import('../views/backstage/Layout.vue'),
    meta: { requireAuth: true },
    children: [
      {
        path: '',
        redirect: '/backstage/stages',
      },
      {
        path: '/backstage/stages',
        name: 'Stages',
        component: () => import('../views/backstage/Stages.vue'),
      },
      {
        path: '/backstage/workshop',
        name: 'Workshop',
        component: () => import('../views/backstage/Workshop.vue'),
      },
      {
        path: '/backstage/media',
        name: 'Media',
        component: () => import('../views/backstage/Media/index.vue'),
      },
      {
        path: '/backstage/profile',
        name: 'Profile',
        component: () => import('../views/backstage/Profile/index.vue'),
        children: [
          {
            path: '',
            redirect: '/backstage/profile/information',
          },
          {
            path: 'information',
            name: 'Update Information',
            component: () => import('../views/backstage/Profile/Information.vue'),
          },
          {
            path: 'change-password',
            name: 'Change Password',
            component: () => import('../views/backstage/Profile/ChangePassword.vue'),
          },
        ]
      },
      {
        path: '/backstage/admin',
        name: 'Admin',
        component: () => import('../views/backstage/Admin/index.vue'),
        children: [
          {
            path: '',
            redirect: '/backstage/admin/player-management',
          },
          {
            path: 'player-management',
            name: 'Player Management',
            component: () => import('../views/backstage/Admin/UserTable.vue'),
          },
          {
            path: 'batch-user-creation',
            name: 'Batch User Creation',
            component: () => import('../views/backstage/Admin/BatchUserCreation.vue'),
          },
          {
            path: 'system-configurations',
            name: 'System Configurations',
            component: () => import('../views/backstage/Admin/SystemConfigurations.vue'),
          },
        ]
      },
      {
        path: '/backstage/new-stage',
        component: () => import('../views/backstage/StageManagement/index.vue'),
        children: [
          {
            path: '',
            name: 'Create New Stage',
            component: () => import('../views/backstage/StageManagement/General.vue'),
          },
        ]
      },
      {
        path: '/backstage/stage-management/:id',
        component: () => import('../views/backstage/StageManagement/index.vue'),
        props: route => ({ id: route.params.id }),
        children: [
          {
            path: '',
            name: 'Stage Management',
            component: () => import('../views/backstage/StageManagement/General.vue'),
          },
          {
            name: 'Stage Customisation',
            path: 'customisation',
            component: () => import('../views/backstage/StageManagement/Customisation.vue'),
          },
          {
            name: 'Stage Media',
            path: 'media',
            component: () => import('../views/backstage/StageManagement/Media.vue'),
          },
          {
            name: 'Archive',
            path: 'archive',
            component: () => import('../views/backstage/StageManagement/Archive.vue'),
          },
          {
            name: 'Scenes',
            path: 'scenes',
            component: () => import('../views/backstage/StageManagement/Scenes.vue'),
          },
        ]
      }
    ]
  },
  {
    path: '/replay/:url/:id',
    name: 'Replay Recording',
    component: () => import('../views/replay/Layout.vue'),
  },
  {
    path: '/:url', // Keep it in the last of the route list so it won't block these other pages when conflict happens
    name: 'Live',
    component: () => import('../views/live/Layout.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(config.publicPath),
  routes
})

router.beforeEach((to, from, next) => {
  document.body.classList.add('waiting');

  const loggedIn = store.getters["auth/loggedIn"];

  if (to.matched.some((record) => record.meta.requireAuth) && !loggedIn) {
    next("/login");
  }
  if (to.name === 'Login' && loggedIn) {
    next("/backstage");
  }
  if (to.name === 'Live') {
    document.querySelector("meta[name=viewport]").setAttribute("content", "");
  } else {
    document.querySelector("meta[name=viewport]").setAttribute("content", "width=device-width,initial-scale=1.0");
  }
  next();
  document.title = `UpStage ${to.name && '- ' + to.name}`;
});

router.afterEach(() => {
  document.body.classList.remove('waiting');
});

export default router
