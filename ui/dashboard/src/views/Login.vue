<template>
  <div class="columns is-mobile is-centered is-vcentered is-fullheight">
    <div
      class="column is-three-quarters-mobile is-two-thirds-tablet is-half-desktop is-one-third-widescreen is-one-quarter-fullhd"
    >
      <div class="card">
        <header class="card-header">
          <p class="card-header-title">Login</p>
        </header>
        <div class="card-content">
          <div class="content">
            <div class="field">
              <p class="control has-icons-left has-icons-right">
                <input
                  class="input"
                  v-model="username"
                  placeholder="Username"
                  required
                />
                <span class="icon is-small is-left">
                  <i class="fas fa-user"></i>
                </span>
                <span class="icon is-small is-right">
                  <i class="fas fa-check"></i>
                </span>
              </p>
            </div>
            <div class="field">
              <p class="control has-icons-left">
                <input
                  class="input"
                  type="password"
                  placeholder="Password"
                  v-model="password"
                  password-reveal
                  required
                />
                <span class="icon is-small is-left">
                  <i class="fas fa-lock"></i>
                </span>
              </p>
            </div>
          </div>
        </div>
        <footer class="card-footer">
          <a class="card-footer-item" @click="submit"
            >Login

            <span class="icon is-medium">
              <i class="fas fa-chevron-right"></i>
            </span>
          </a>
        </footer>
      </div>
    </div>
  </div>
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

<style>
.is-fullheight {
  height: 90vh;
}
</style>
