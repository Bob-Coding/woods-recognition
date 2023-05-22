<template>
  <div>
    <v-app-bar app>
      <v-toolbar-title>Dashboard</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" @click="showPlotMogelijkeGokken">Show Plot</v-btn>
      <v-btn color="primary" @click="selectFile">Upload Image</v-btn>
    </v-app-bar>

    <v-container>
      <v-card>
        <v-card-title>Data</v-card-title>
        <v-card-text>
          <ul>
            <li v-for="(item, index) in data" :key="index">
              {{ item }}
            </li>
          </ul>
        </v-card-text>
      </v-card>

      <v-card>
        <v-card-title>Upload Image</v-card-title>
        <v-card-text>
          <input
            type="file"
            ref="fileInput"
            style="display: none"
            @change="onFileSelected"
          />
          <v-btn color="primary" @click="selectFile">Select an image</v-btn>
          <span>{{ selectedFileName }}</span>
        </v-card-text>
      </v-card>

      <v-card>
        <v-card-title>Plot</v-card-title>
        <v-card-text>
          <img :src="plotUrl" v-if="plotUrl" />
        </v-card-text>
      </v-card>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      data: [],
      file: null,
      selectedFileName: null,
      plotUrl: null,
    };
  },
  computed: {
    apiUrl() {
      return process.env.API_URL;
    },
  },
  methods: {
    async fetchData() {
      const response = await this.$axios.get("/data");
      this.data = response.data;
    },
    async showPlotVoorspeldLabel() {
      const response = await this.$axios.get("/voorspeld_label", {
        responseType: "blob",
      });
      this.plotUrl = URL.createObjectURL(response.data);
    },
    async showPlotMogelijkeGokken() {
      const response = await this.$axios.get("/mogelijke_gokken", {
        responseType: "blob",
      });
      this.plotUrl = URL.createObjectURL(response.data);
    },
    selectFile() {
      console.log(this.$refs.fileInput);
      this.$refs.fileInput.click();
    },
    onFileSelected(event) {
      this.file = event.target.files[0];
      this.selectedFileName = this.file.name;
    },
    async uploadImage() {
      const formData = new FormData();
      formData.append("file", this.file);
      await this.$axios.post(this.apiUrl + "/dashboard/data/images", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>
