<template>
    <div class="text-center flex-1 flex flex-col justify-center px-3">
        <div>
            <h2 class="text-3xl font-sans m-3">Share Media and Text</h2>
            <p class="text-sm">Clip-Sync allows you to share content across devices.</p>
            <p class="text-sm">Create an account/Login to store sessions across devices.</p>
            <p class="text-sm">Join or create a session to get started. </p>
        </div>
        <div class="flex flex-col justify-center my-16 gap-2 md:flex-row ">
          <input type="text" v-model="sessionCode" class="rounded-md border-orange-300 border-solid border-2 px-3 py-3 md:w-4/12 outline-none focus:border-orange-500" placeholder="Enter Session code">
          <HomeSessionBtn :session-code="sessionCode" class="md:w-1/12 "/>
        </div>
    </div>
</template>

<script setup lang="ts">
  import HomeSessionBtn from "@/components/session/SessionConnectButton.vue";
  import {ref} from "vue";

  const sessionCode = ref("");
</script>