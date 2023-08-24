<script>
import {SessionConnect, AppHeader, AppFooter } from "@/components";

export default {
    components: {
      AppHeader,
      AppFooter,
      SessionConnect,
    },
}
</script>

<template>
  <main class="flex flex-col h-screen">
    <AppHeader />
    <SessionConnect class="flex-1"/>
    <AppFooter />
  </main>
</template>

<style scoped>
main {
  background-image: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
}
</style>
