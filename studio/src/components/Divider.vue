<template>
  <div class="divider">
    <hr class="zig" />
    <hr class="zag" />
    <span class="text-in-middle">
      <slot></slot>
    </span>
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
.divider {
  position: relative;
}
hr.zig,
hr.zag {
  border: none;
  height: 30px;
  margin: 0 16px;
}
hr.zig {
  background:
    linear-gradient(-135deg, #fff 20px, rgba(0, 0, 0, 0) 0) 0 5px,
    linear-gradient(135deg, #fff 20px, rgba(0, 0, 0, 0) 0) 0 5px;
  background-color: rgba(0, 0, 0, 0);
  background-position: center bottom;
  background-repeat: repeat-x;
  background-size: 10px 40px;
  z-index: 100;
  position: relative;
}
hr.zag {
  background:
    linear-gradient(-135deg, #333 20px, rgba(0, 0, 0, 0) 0) 0 5px,
    linear-gradient(135deg, #333 20px, #fff 0) 0 5px;
  background-color: rgba(0, 0, 0, 0);
  background-position: center bottom;
  background-repeat: repeat-x;
  background-size: 10px 40px;
  z-index: 50;
  margin-top: -28px;
}
.text-in-middle {
  background: white;
  position: absolute;
  top: 0;
  left: 50%;
  z-index: 101;
  padding: 4px 8px;
  transform: translateX(-50%);
}
</style>
