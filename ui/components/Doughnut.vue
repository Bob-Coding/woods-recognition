<template>
  <div>
    <v-card>
      <v-card-title>Data set distribution</v-card-title>
      <v-card-text>
        <canvas ref="chartCanvas"></canvas>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { Chart } from "chart.js";

export default {
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  mounted() {
    this.renderChart();
  },
  methods: {
    renderChart() {
      const chartData = this.data.datasets;
      new Chart(this.$refs.chartCanvas, {
        type: "doughnut",
        data: {
          labels: [
            "Crack",
            "Dead_Knot",
            "Knot_Missing",
            "Knot_With_Crack",
            "Live_Knot",
            "Marrow",
            "Quartzity",
            "Resin",
            "clean",
          ],
          datasets: chartData,
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
        },
      });
    },
  },
};
</script>
