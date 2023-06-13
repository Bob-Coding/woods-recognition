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
          multiple
        />
        <v-btn
          color="primary"
          v-if="!files"
          @click="selectFile"
          class="btn-select-image"
        >
          Select an image
        </v-btn>
        <div class="selectedFile" v-if="files">
          <div
            class="filename"
            v-for="(file, fileIndex) in files"
            :key="generateId()"
          >
            {{ file.name }}
            <svg
              :name="file.name"
              xmlns="http://www.w3.org/2000/svg"
              class="remove-icon"
              @click="removeSelected(fileIndex)"
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
          v-if="files"
          @click="classifyImage"
          class="btn-select-image"
        >
          Classify image
        </v-btn>
      </v-card>
    </v-container>
    <v-container>
      <v-card v-for="image in plotUrls" :key="generateId()">
        <div
          class="image-container"
          v-for="(_value, key) in image"
          :key="generateId()"
        >
          <v-card-title class="plot-title">{{ key }}</v-card-title>
          <div class="plot-container">
            <img
              v-for="value in image[key]"
              :src="value"
              class="plot-image"
              :key="generateId()"
            />
          </div>
        </div>
      </v-card>
    </v-container>
  </div>
</template>

<style scoped>
.selectedFile {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  color: #9e9e9e;
  align-items: flex-start;
  gap: 10px;
  margin-left: 16px;
}
.filename {
  display: flex;
  gap: 10px;
}

.btn-select-image {
  display: inline-flex;
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
}
.remove-icon:hover {
  cursor: pointer;
}
.plot-image {
  width: 45%;
  object-fit: contain;
  margin-bottom: 30px;
}
.plot-container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  gap: 20px;
}
</style>

<script>
export default {
  name: "Dashboard",
  data() {
    return {
      files: null,
      selectedFileNames: null,
      plotUrls: null,
    };
  },
  computed: {
    apiUrl() {
      return process.env.API_URL;
    },
  },
  methods: {
    generateId() {
      return Math.random().toString(36).substr(2, 9);
    },
    selectFile() {
      this.$refs.fileInput.click();
    },
    onFileSelected(event) {
      this.files = [];
      for (const file of event.target.files) {
        this.files.push(file);
      }
    },
    removeSelected(fileIndex) {
      this.files.splice(fileIndex, 1);
      if (this.$refs.fileInput.files.length === 0) {
        this.$refs.fileInput.value = "";
      }
    },
    async classifyImage(event) {
      event.preventDefault();
      const formData = new FormData();
      for (let i = 0; i < this.files.length; i++) {
        const file = this.files[i];
        formData.append("imageFiles", file);
      }

      const config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };

      try {
        const response = await this.$axios.post(
          "/classify_image",
          formData,
          config
        );
        this.plotUrls = response.data;
        this.files = null;
      } catch (error) {
        console.log("error", error);
      }
    },
  },
};
</script>
