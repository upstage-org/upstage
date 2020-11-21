import Vue from "vue";
import VueRouter from "vue-router";
import store from "@/store/store";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    redirect: "/dashboard",
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/Login"),
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: () => import("@/views/Dashboard"),
    meta: { requireAuth: true, name: "Dashboard" },
  },
];

const router = new VueRouter({
  // mode: "history",
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  const loggedIn = store.getters["auth/loggedIn"];

  if (to.matched.some((record) => record.meta.requireAuth) && !loggedIn) {
    next("/login");
  }
  next();
  document.title = to.name || "Stage";
});

export default router;
