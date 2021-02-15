<template>
  <div class="columns">
    <div class="column is-4">
      <aside class="menu box has-background-light mx-4">
        <p class="menu-label">Name of the Stage</p>
        <ul class="menu-list">
          <li>
            <router-link
              to="/dashboard/stage-management"
              exact-active-class="is-active"
              >General</router-link
            >
          </li>
          <li>
            <router-link
              to="/dashboard/stage-management/layout"
              exact-active-class="is-active"
              >Layout</router-link
            >
          </li>
          <li>
            <router-link
              to="/dashboard/stage-management/chat"
              exact-active-class="is-active"
              >Chat</router-link
            >
          </li>
          <li><a>Record</a></li>
          <li>
            <router-link
              to="/dashboard/stage-management/scenes"
              exact-active-class="is-active"
              >Scenes</router-link
            >
            <ul>
              <li><a>Avatar</a></li>
              <li><a>Props</a></li>
              <li><a>Backdrop</a></li>
              <li><a>Sound</a></li>
              <li><a>Videos</a></li>
              <li><a>Loading</a></li>
            </ul>
          </li>
        </ul>
      </aside>
    </div>
    <div class="column is-8">
      <div class="pt-4 pr-4 pb-4">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style>
</style>