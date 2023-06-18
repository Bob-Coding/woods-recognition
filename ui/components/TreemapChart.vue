<template>
  <div class="chart-container" ref="chart"></div>
</template>

<script>
import Plotly from "plotly.js-dist";

export default {
  props: {
    defectData: {
      type: Object,
      required: true,
    },
  },
  mounted() {
    this.renderChart();
  },
  methods: {
    renderChart() {
      var labels = [
        "Crack",
        "Dead_Knot",
        "Knot_Missing",
        "Knot_With_Crack",
        "Live_Knot",
        "Marrow",
        "Quartzity",
        "Resin",
        "defect(s)",
      ];

      var parents = [
        "defect(s)",
        "defect(s)",
        "defect(s)",
        "defect(s)",
        "defect(s)",
        "defect(s)",
        "defect(s)",
        "defect(s)",
        "",
      ];

      // function traverse(node, parent = "") {
      //   labels.push(node.name);
      //   parents.push(parent);

      //   if (node.children) {
      //     node.children.forEach((child) => {
      //       traverse(child, node.name);
      //     });
      //   }
      // }
      // traverse(this.defectData);

      // const values = labels.map((label) => {
      //   const node = this.getNodeByName(label);
      //   return node.value || 0;
      // });

      const data = [
        {
          type: "treemap",
          labels: labels,
          values: [56, 658, 9, 61, 943, 54, 19, 49, 1849],
          parents: parents,
          textinfo: "label+value+percent parent",
          domain: { x: [0, 0.7], y: [0, 1] }, // Pas de waarden van x en y aan
          marker: {
            color: "black",
            line: { width: 2 },
          },
          pathbar: { visible: false },
        },
        {
          type: "treemap",
          labels: labels,
          parents: parents,
          domain: { x: [0.4, 1] },
          values: [0, 211, 1, 11, 874, 104, 88, 474, 1763],
          textinfo: "label+value+percent parent",
          marker: { line: { width: 2 } },
          pathbar: { visible: false },
        },
        {
          type: "treemap",
          labels: ["clean"],
          parents: [""],
          domain: { x: [0.8, 1] },
          values: [388],
          textinfo: "label+value+percent parent",
          marker: { line: { width: 2 } },
          pathbar: { visible: false },
        },
      ];

      var layout = {
        annotations: [
          {
            showarrow: false,
            text: "<b>Multiple defects</b>",
            x: 0.2,
            xanchor: "center",
            y: 1.1,
            yanchor: "bottom",
          },
          {
            showarrow: false,
            text: "<b>Single defect</b>",
            x: 0.5,
            xanchor: "center",
            y: 1.1,
            yanchor: "bottom",
          },
          {
            showarrow: false,
            text: "<b>Clean</b>",
            x: 0.8,
            xanchor: "center",
            y: 1.1,
            yanchor: "bottom",
          },
        ],
      };

      Plotly.newPlot(this.$refs.chart, data, layout, { responsive: true });
    },
  },
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 400px;
  background-color: black;
}
.main-svg {
  background: none !important;
  background-color: #1e1e1e !important;
}
</style>
