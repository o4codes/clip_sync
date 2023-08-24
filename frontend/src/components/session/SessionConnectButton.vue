<template>
  <button v-if="props.sessionCode" @click="joinSession"
          class="bg-teal-600 text-white font-bold px-4 py-3 rounded-lg whitespace-nowrap">Join Session
  </button>
  <button v-else @click="createSession" class="bg-orange-300 px-4 py-3 rounded-lg font-semibold whitespace-nowrap">New
    Session
  </button>
</template>

<script setup lang="ts">
// import router from "@/router";
import {useRouter} from "vue-router";
const router = useRouter();
const props = defineProps({
  sessionCode: {type: String, default: null},
});

function joinSession(): void {
  console.log('join session');
  console.log(props.sessionCode);
  router.push(`/session/${props.sessionCode}`);
}

function createSession(): string {
  console.log('create session');
  return '';
}
</script>