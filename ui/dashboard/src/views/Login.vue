<template>
  <v-main>
    <v-card width="500" class="mx-auto mt-5">
      <v-card-title>Login</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="login">
          <v-text-field
            name="username"
            label="Username"
            prepend-icon="mdi-account-circle"
            v-model="username"
          />
          <v-text-field
            :name="password"
            v-model="password"
            label="Password"
            :type="showPassword ? 'text' : 'password'"
            prepend-icon="mdi-lock"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="showPassword = !showPassword"
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <!-- <v-btn color="warning">Register</v-btn> -->
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="submit">Login</v-btn>
      </v-card-actions>
    </v-card>
  </v-main>
</template>

<script>
export default {
  data() {
    return {
      showPassword: false,
      username: "",
      password: "",
    };
  },
  methods: {
    submit() {
      const user = {
        username: this.username,
        password: this.password,
      };
      this.$store.dispatch("auth/login", user).then(() => {
        this.$router.push({ name: "Dashboard" });
      });
    },
  },
};
</script>

<style></style>
