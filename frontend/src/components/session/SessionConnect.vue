<template>
    <div class="text-center flex-1 flex flex-col justify-center px-3">
        <div>
          <h2 class="text-6xl font-sans m-3 heading-font font-bold">Experience Seamless Content Sharing </h2>
          <h2 class="text-3xl font-sans m-3 heading-font">Across Devices in Real Time</h2>
        </div>
        <div class="flex flex-col justify-center my-16 gap-2 md:flex-row ">
          <input type="text" v-model="sessionCode" class="rounded-md border-orange-300 border-solid border-2 px-3 py-3 md:w-4/12 outline-none focus:border-orange-500" placeholder="Enter Session code">
          <SessionConnectButton :session-code="sessionCode" />
        </div>
    </div>
</template>

<script setup lang="ts">
  import {ref} from "vue";
  import { SessionConnectButton } from ".";

  const sessionCode = ref("");
</script>
