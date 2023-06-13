<template>
  <div>
    <v-container>
      <v-card> </v-card>
    </v-container>
  </div>
</template>

<style scoped></style>

<script>
export default {
  name: "Statistics",
  data() {
    return {};
  },
  computed: {
    apiUrl() {
      return process.env.API_URL;
    },
  },
  methods: {},
  mounted() {},
};
</script>
