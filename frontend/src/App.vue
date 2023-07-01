<script>
import { RouterLink, RouterView } from "vue-router";
import AppHeader from "./components/AppHeader.vue";
import AppFooter from "./components/AppFooter.vue";

export default {
  components: {
    AppFooter, AppHeader
  },
}

</script>

<template>
  <div id="app" class="flex flex-col">
    <AppHeader />
    <RouterView />
    <AppFooter />
  </div>
</template>

<style scoped>
</style>
