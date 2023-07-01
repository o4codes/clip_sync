<script>
import Hamburger from "./icons/Hamburger.vue";
export default {
  data() {
    return {
      showMenu: false,
    };
  },
  methods: {
    toggleNav() {
      console.log("trying to toggle nav");
      this.showMenu = !this.showMenu;
    },
  },

  components: { Hamburger },
};
</script>

<template>
  <header>
    <nav class="container mx-auto md:flex md:justify-between md:items-center py-[2%] sm:py-[2%] px-[4%]  sm:px-[10%]">
      <div class="flex items-center justify-between">
        <router-link to="/" class="text-2xl font-bold md:text-2xl"
          >ClipSync
        </router-link>
        <!-- Mobile menu button -->
        <div @click="toggleNav" class="flex md:hidden">
          <button
            type="button"
            class="text-gray-800 hover:text-gray-400 focus:outline-none focus:text-gray-400"
          >
            <Hamburger />
          </button>
        </div>
      </div>

      <!-- Mobile Menu open: "block", Menu closed: "hidden" -->
      <div
        :class="showMenu ? 'flex' : 'hidden'"
        class="flex-col mt-8 space-y-4 md:flex md:space-y-0 md:flex-row md:items-center md:space-x-10 md:mt-0"
      >
        <router-link to="/">SignUp</router-link>
        <router-link to="/">Login</router-link>
      </div>
    </nav>
  </header>
</template>
