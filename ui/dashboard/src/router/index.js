import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
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
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/stage',
    name: 'Stages',
    component: () => import('../views/Stage.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  // const loggedIn = store.getters["auth/loggedIn"];

  // if (to.matched.some((record) => record.meta.requireAuth) && !loggedIn) {
  //   next("/login");
  // }
  next();
  document.title = `UpStage ${to.name && '- ' + to.name}`;
});

export default router
