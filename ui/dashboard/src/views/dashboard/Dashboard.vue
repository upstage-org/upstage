<template>
  <section class="hero is-small is-primary is-bold">
    <div class="hero-body">
      <div class="container">
        <h1 class="title">DASHBOARD</h1>
        <h2 class="subtitle">
          <ul>
            <li>Presentation of the goal of the page...</li>
          </ul>
        </h2>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <h1 class="title">
        Stages
        <button class="button mx-2">
          <span>New</span>
          <span class="icon">
            <i class="fa fa-plus"></i>
          </span>
        </button>
        <button class="button mx-2">
          <span>Search</span>
          <span class="icon">
            <i class="fa fa-search"></i>
          </span>
        </button>
      </h1>
      <h2 class="subtitle">
        Pres <strong>New</strong> button to create a new future stage. Click
        <strong>Search</strong> button for search form to find Stage
      </h2>
      <div class="columns">
        <div class="column">
          <Stage name="Making Absence Present" access="Audiance" />
        </div>
        <div class="column">
          <Stage name="Waiting for Brexit" access="Audiance" />
        </div>
        <div class="column">
          <Stage name="Pandemic Party" access="Audiance" />
        </div>
        <div class="column"></div>
      </div>
    </div>
  </section>
</template>

<script>
import Stage from "@/components/stage/Stage";
export default {
  components: { Stage },
};
</script>

<style>
</style>