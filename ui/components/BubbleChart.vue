<div>
    <v-card>
      <v-card-title>Interactive Bubble Chart</v-card-title>
      <v-card-text>
        <canvas ref="chartCanvas"></canvas>
      </v-card-text>
    </v-card>
</div>

<script>
import { Bubble } from "vue-chartjs";

export default {
  extends: Bubble,
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
  computed: {
    chartData() {
      return {
        datasets: [
          {
            label: "Dense Model",
            data: this.data.dense.map((point) => ({
              x: point.x,
              y: point.y,
              r: point.size,
            })),
            backgroundColor: "rgba(0, 123, 255, 0.7)",
          },
          {
            label: "Seq Dense Model",
            data: this.data.seq_dense.map((point) => ({
              x: point.x,
              y: point.y,
              r: point.size,
            })),
            backgroundColor: "rgba(255, 0, 123, 0.7)",
          },
        ],
      };
    },
    options() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            title: {
              display: true,
              text: "X-axis",
            },
            ticks: {
              beginAtZero: true,
            },
          },
          y: {
            title: {
              display: true,
              text: "Y-axis",
            },
            ticks: {
              beginAtZero: true,
            },
          },
        },
      };
    },
  },
};
</script>

<style>
/* Add any custom styles for the component here */
</style>
