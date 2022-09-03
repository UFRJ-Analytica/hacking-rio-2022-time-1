<template>
  <div class="text-center">
    <v-dialog v-model="dialog2" width="500">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          v-bind="attrs"
          v-on="on"
          color="orange darken-3"
          class="white--text"
        >
          <v-icon left>mdi-camera</v-icon>
          Adicionar uma foto
        </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="text-h5">Upload</span>
        </v-card-title>
        <v-card-text>
          Realize dois cortes: o primeiro deve enquadradar toda a tartaruga, o
          segundo deve conter apenas a cabeça da tartaruga.
        </v-card-text>

        <v-container>
          <v-row>
            <v-col>
              <p>Tartaruga</p>
              <my-image-cropper
                v-model="turtle"
                :width="200"
                :height="200"
              ></my-image-cropper>
            </v-col>
            <v-col>
              <p>Cabeça</p>
              <my-image-cropper
                v-model="turtlehead"
                :width="200"
                :height="200"
              ></my-image-cropper>
            </v-col>

          </v-row>
          <v-row>
            <v-input>Nome desejado</v-input>
          </v-row>
        </v-container>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="dialog = false"> Close </v-btn>
          <v-btn text @click="uploadCroppedImage"> Save </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>


<script>
import "vue-croppa/dist/vue-croppa.css";
export default {
  data() {
    return {
      dialog: false,
      turtle: {},
      turtlehead: {},
    };
  },
  methods: {
    uploadCroppedImage() {
      this.dialog = false;
      this.turtle.generateBlob((blob) => {
        console.log(blob);
      });
    },
  },
};
</script>