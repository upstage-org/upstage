<template>
  <div class="columns" :style="'width: ' + avatars.length * 100 + 'px'">
    <div v-for="avatar in avatars" :key="avatar" class="column">
      <Image :src="avatar.src" fit="contain" />
    </div>
  </div>
</template>

<script>
import Image from "@/components/Image";
import config from "@/../vue.config";

export default {
  components: { Image },
  setup: () => {
    const files = [
      "01.png",
      "02.png",
      "03.png",
      "04.png",
      "05.png",
      "06.png",
      "07.png",
      "08.png",
      "09.png",
      "10.png",
      "11.png",
      "blob_avatar_1.jpg",
      "blob_avatar_2.jpg",
      "logo-upstage-official-print_500px.png",
      "mobilise-demoblise-logo-version-black.gif",
      "mobilise-demoblise-logo-version-white.png",
      "plague_doctor_clearcut2.png",
      "plague_doctor_clearcut.png",
      "virus_1.png",
      "virus_2.png",
      "virus_3.png",
    ];
    const avatars = files.map((file) => ({
      name: file,
      src: `${config.publicPath}demo/avatars/${file}`,
    }));
    return { avatars };
  },
};
</script>

<style scoped>
.column {
  width: 160px;
  height: 90px;
}
</style>