<template>
  <div>
    <v-container>
      <v-card>
        <v-card-title class="title">Upload Image</v-card-title>
        <input
          type="file"
          ref="fileInput"
          style="display: none"
          @change="onFileSelected"
        />
        <v-btn
          color="primary"
          v-if="!selectedFileName"
          @click="selectFile"
          class="btn-select-image"
        >
          Select an image
        </v-btn>
        <div class="selectedFile">
          <div class="filename">{{ selectedFileName }}</div>
          <div v-if="selectedFileName">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="remove-icon"
              @click="removeSelected"
              width="16"
              height="16"
              viewBox="0 0 16 16"
            >
              <path
                fill="currentColor"
                d="M15.854 12.854L11 8l4.854-4.854a.503.503 0 0 0 0-.707L13.561.146a.499.499 0 0 0-.707 0L8 5L3.146.146a.5.5 0 0 0-.707 0L.146 2.439a.499.499 0 0 0 0 .707L5 8L.146 12.854a.5.5 0 0 0 0 .707l2.293 2.293a.499.499 0 0 0 .707 0L8 11l4.854 4.854a.5.5 0 0 0 .707 0l2.293-2.293a.499.499 0 0 0 0-.707z"
              />
            </svg>
          </div>
        </div>
        <v-btn
          color="primary"
          v-if="selectedFileName"
          @click="classifyImage"
          class="btn-select-image"
        >
          Classify image
        </v-btn>
      </v-card>
    </v-container>
    <v-container>
      <v-card>
        <v-card-title>Plot</v-card-title>
        <v-card-text>
          <img :src="plotUrl" v-if="plotUrl" />
        </v-card-text>
      </v-card>
    </v-container>
  </div>
</template>

<style scoped>
.selectedFile {
  color: #9e9e9e;
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: 16px;
}
.btn-select-image {
  margin: 16px 0px 16px 16px;
  margin-left: 16px;
}
.title {
  font-size: 25px;
  font-weight: bold;
}
.remove-icon {
  color: red;
  width: 16px;
  height: 16px;
}
.remove-icon:hover {
  cursor: pointer;
}
</style>

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
      console.log("hi");
      this.file = event.target.files[0];
      console.log("this file", this.file);

      this.selectedFileName = this.file.name;
    },
    removeSelected() {
      this.file = null;
      this.selectedFileName = null;
      // Reset de waarde van het bestandsinvoerelement
      this.$refs.fileInput.value = "";
    },
    async classifyImage() {
      const formData = new FormData();
      formData.append("file", this.file);
      await this.$axios.post(this.apiUrl + "/classify_image", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    },
  },
  mounted() {
    // this.fetchData();
  },
};
</script>
