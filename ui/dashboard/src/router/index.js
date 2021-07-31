import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import store from "@/store";
import config from '../../vue.config';
import PleaseRotate from '@/utils/pleaserotate';

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
      {
        path: '/stage',
        name: 'Stages',
        component: () => import('../views/Stage.vue')
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
            redirect: '/backstage/admin/approval',
          },
          {
            path: 'approval',
            name: 'Registration Approval',
            component: () => import('../views/backstage/Admin/RegistrationApproval.vue'),
          },
          {
            path: 'reset-password',
            name: 'Reset Password',
            component: () => import('../views/backstage/Admin/ResetPassword.vue'),
          },
          {
            path: 'switch-role',
            name: 'Switch Role',
            component: () => import('../views/backstage/Admin/SwitchRole.vue'),
          },
          {
            path: 'delete-user',
            name: 'Delete User',
            component: () => import('../views/backstage/Admin/DeleteUser.vue'),
          },
          {
            path: 'profile-management',
            name: 'Profile Management',
            component: () => import('../views/backstage/Admin/ProfileManagement.vue'),
          },
          {
            path: 'upload-limit',
            name: 'Upload Limit',
            component: () => import('../views/backstage/Admin/UploadLimit.vue'),
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
            name: 'Replays and Chat',
            path: 'replays-chat',
            component: () => import('../views/backstage/StageManagement/Chat.vue'),
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
    path: '/live/:url?',
    name: 'Live',
    component: () => import('../views/live/Layout.vue'),
  },
  {
    path: '/replay/:url/:id',
    name: 'Replay Record',
    component: () => import('../views/replay/Layout.vue'),
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
    PleaseRotate.start();
  } else {
    document.querySelector("meta[name=viewport]").setAttribute("content", "width=device-width,initial-scale=1.0");
    PleaseRotate.stop();
  }
  next();
  document.title = `UpStage ${to.name && '- ' + to.name}`;
});

router.afterEach(() => {
  document.body.classList.remove('waiting');
});

export default router
