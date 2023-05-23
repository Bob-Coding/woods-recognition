<template>
  <div>
    <v-container>
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
  name: "Dashboard",
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
    selectFile() {
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
