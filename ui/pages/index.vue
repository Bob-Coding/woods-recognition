<template>
  <div>
    <v-container>
      <v-card>
        <bubble-chart
          :data="this.datasets"
          v-if="Object.keys(this.datasets).length"
        />
        <doughnut-chart :data="this.dougnutDataSet" />
        <treemap-chart :defectData="this.defectData" class="chart-container" />
      </v-card>
    </v-container>
  </div>
</template>

<style scoped>
.chart-container {
  width: 100%;
  height: 400px;
}
</style>

<script>
import BubbleChart from "@/components/BubbleChart.vue";
import DoughnutChart from "@/components/Doughnut.vue";
import TreemapChart from "@/components/TreemapChart.vue";

export default {
  name: "Statistics",
  components: { BubbleChart, DoughnutChart, TreemapChart },
  data() {
    return {
      datasets: {},
      defectData: {
        name: "root",
        children: [
          {
            name: "Multiple defects",
            value: 1763,
            children: [
              { name: "Crack", value: 0 },
              { name: "Quartzity", value: 88 },
              { name: "Live_Knot", value: 874 },
              { name: "Dead_Knot", value: 211 },
              { name: "Knot_With_Crack", value: 11 },
              { name: "Resin", value: 474 },
              { name: "Knot_Missing", value: 1 },
              { name: "Marrow", value: 104 },
            ],
          },
          {
            name: "Single defect",
            value: 1849,
            children: [
              { name: "Crack", value: 56 },
              { name: "Quartzity", value: 19 },
              { name: "Live_Knot", value: 943 },
              { name: "Dead_Knot", value: 658 },
              { name: "Knot_With_Crack", value: 61 },
              { name: "Resin", value: 49 },
              { name: "Knot_Missing", value: 9 },
              { name: "Marrow", value: 54 },
            ],
          },
          {
            name: "Clean",
            value: 388,
          },
        ],
      },
      dougnutDataSet: {
        datasets: [
          {
            data: [70, 1660, 100, 398, 1234, 77, 24, 49, 388],
            backgroundColor: [
              "rgb(255, 99, 132)",
              "rgb(54, 162, 235)",
              "rgb(255, 205, 86)",
              "rgb(75, 192, 192)",
              "rgb(153, 102, 255)",
              "rgb(255, 159, 64)",
              "rgb(255, 0, 0)",
              "rgb(0, 255, 0)",
              "rgb(0, 0, 255)",
            ],
            hoverOffset: 4,
          },
        ],
      },
    };
  },
  methods: {
    async getBubbleChartData() {
      try {
        const response = await this.$axios.get("/bubble_chart");
        let data = {
          datasets: [
            {
              label: "dense(correct)",
              data: [],
              backgroundColor: "green",
            },
            {
              label: "dense(wrong)",
              data: [],
              backgroundColor: "red",
            },
            {
              label: "dense(total)",
              data: [],
              backgroundColor: "grey",
            },
            {
              label: "seq_dense(correct)",
              data: [],
              backgroundColor: "green",
            },
            {
              label: "seq_dense(wrong)",
              data: [],
              backgroundColor: "red",
            },
            {
              label: "seq_dense(total)",
              data: [],
              backgroundColor: "grey",
            },
          ],
        };

        for (const [model, defects] of Object.entries(response.data)) {
          for (const [defectName, values] of Object.entries(defects)) {
            const correctDatasets = data.datasets.find((m) => {
              return (
                model === m.label.split("(")[0] && m.label.endsWith("(correct)")
              );
            });
            const wrongDatasets = data.datasets.find((m) => {
              return (
                model === m.label.split("(")[0] && m.label.endsWith("(wrong)")
              );
            });
            const totalDatasets = data.datasets.find((m) => {
              return (
                model === m.label.split("(")[0] && m.label.endsWith("(total)")
              );
            });
            wrongDatasets?.data?.push(
              values["total_guesses"] - values["correct_guesses"]
            );
            correctDatasets?.data?.push(values["correct_guesses"]);
            totalDatasets?.data?.push(values["total_guesses"]);
          }
        }
        this.datasets = data;
      } catch (error) {
        console.log("error", error);
      }
    },
  },
  async mounted() {
    await this.getBubbleChartData();
  },
};
</script>
