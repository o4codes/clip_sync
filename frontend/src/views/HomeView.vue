<script>
import SessionCreate from '../components/SessionCreate.vue';
import AppFooter from "@/components/AppFooter.vue";
import AppHeader from "@/components/AppHeader.vue";

export default {
    components: {
      AppHeader,
      AppFooter,
      SessionCreate,
    },
}
</script>

<template>
  <main class="flex flex-col h-screen">
    <AppHeader />
    <SessionCreate class="flex-1"/>
    <AppFooter />
  </main>
</template>

<style scoped>
main {
  background-image: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
}
</style>
