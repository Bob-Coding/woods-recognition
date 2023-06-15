<template>
  <div>
    <v-container>
      <v-card>
        <bubble-chart :data="chartData" />
      </v-card>
    </v-container>
  </div>
</template>

<style scoped></style>

<script>
import BubbleChart from "@/components/BubbleChart.vue";

export default {
  name: "Statistics",
  components: { BubbleChart },
  data() {
    return {
      chartData: {
        dense: [
          { x: 1, y: 2, size: 10 },
          { x: 2, y: 4, size: 20 },
          { x: 3, y: 6, size: 15 },
          // Add more data points for the "Dense Model" here
        ],
        seq_dense: [
          { x: 4, y: 5, size: 12 },
          { x: 5, y: 3, size: 18 },
          { x: 6, y: 1, size: 25 },
          // Add more data points for the "Seq Dense Model" here
        ],
      },
    };
  },
  methods: {},
  mounted() {},
};
</script>
