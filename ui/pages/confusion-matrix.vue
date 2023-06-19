<template>
  <div>
    <v-container>
      <v-card>
        <v-card-title class="title">DenseNet Model:</v-card-title>
        <img :src="matrix_dense" />
        <v-card-title class="title">Sequential DenseNet Model:</v-card-title>
        <img :src="matrix_seq_dense" />
      </v-card>
    </v-container>
  </div>
</template>

<style scoped></style>

<script>
export default {
  name: "confusionMatrix",
  data() {
    return {
      matrix_dense: null,
      matrix_seq_dense: null,
    };
  },
  methods: {
    async getMatrixes() {
      try {
        const response = await this.$axios.get("/confusion_matrixes");
        this.matrix_dense = response.data["dense"];
        this.matrix_seq_dense = response.data["seq_dense"];

        console.log(this.matrix_dense);
        console.log(this.matrix_seq_dense);
      } catch (error) {
        console.log("error", error);
      }
    },
  },
  async mounted() {
    await this.getMatrixes();
  },
};
</script>
