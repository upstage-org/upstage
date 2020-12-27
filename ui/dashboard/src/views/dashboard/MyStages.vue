<template>
  <section class="section">
    <div class="container">
      <h1 class="title">
        My Stages
        <button class="button mx-2 is-dark">
          <span>New</span>
          <span class="icon">
            <i class="fa fa-plus"></i>
          </span>
        </button>
        <button class="button mx-2 is-dark">
          <span>Search</span>
          <span class="icon">
            <i class="fa fa-search"></i>
          </span>
        </button>
      </h1>
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
  <section class="section">
    <div class="container">
      <h1 class="title">Other Stages</h1>
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
  I
</template>

<script>
import Stage from "@/components/stage/Stage";
export default {
  components: { Stage },
};
</script>

<style>
</style>