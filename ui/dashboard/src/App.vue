<template>
  <v-app>
    <v-app-bar dark color="primary lighten-1" app>
      <v-toolbar-title><h1>Stage Dashboard</h1></v-toolbar-title>
      <v-spacer></v-spacer>
      <p class="pname" v-show="!!user">{{ user }}</p>
      <v-btn v-if="!loggedIn" text rounded to="login">Login</v-btn>
      <v-btn v-else text rounded @click="logout">Logout</v-btn>
    </v-app-bar>

    <v-main><router-view></router-view></v-main>

    <v-footer color="primary lighten-1" padless>
      <v-row justify="center" no-gutters>
        <v-col class="primary lighten-2 py-4 text-center white--text" cols="12">
          {{ new Date().getFullYear() }} — <strong>Stage Dashboard</strong>
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "App",

  data: () => ({
    showPassword: false,
  }),
  methods: {
    logout() {
      this.$store.dispatch("auth/logout");
    },
  },
  computed: {
    ...mapGetters("auth", ["loggedIn"]),
    user() {
      return this.$store.getters["user/getCurrentUser"];
    },
  },
};
</script>

<style scoped>
.pname {
  margin-bottom: 0;
}
</style>
