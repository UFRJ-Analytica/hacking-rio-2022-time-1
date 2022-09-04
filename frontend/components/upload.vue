<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="500">
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
        <v-row no-gutters>
          <v-col id="helpMessage" cols="12">
            <v-alert
              dismissible
              text
              outlined
              :type="helpMessageType"
              v-model="showHelpMessage"
            >
              {{ this.helpMessage }}
            </v-alert>
          </v-col>
        </v-row>
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
                :width="180"
                :height="180"
              ></my-image-cropper>
            </v-col>
            <v-col>
              <p>Cabeça</p>
              <my-image-cropper
                v-model="turtlehead"
                :width="180"
                :height="180"
              ></my-image-cropper>
            </v-col>
          </v-row>
          <v-row>
            <v-text-field
              v-model="turtle_name"
              label="Nome desejado"
            ></v-text-field>
            <dateDialog
              dateKey="dateKey"
              @onSelectedDate="
                (value) => {
                  this.date = value;
                }
              "
              text="Data de Envio da Amostra"
            ></dateDialog>
          </v-row>
        </v-container>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="close"> Close </v-btn>
          <v-btn text @click="save"> Save </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>


<script>
import "vue-croppa/dist/vue-croppa.css";
export default {
  props: {
    latitude: Number,
    longitude: Number,
  },
  data() {
    return {
      dialog: false,
      turtle_name: "",
      turtle: {},
      dateKey: 0,
      helpMessage: "",
      showHelpMessage: false,
      helpMessageType: "info",
      myCoordinates: {},
      turtlehead: {},
      date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
    };
  },
  methods: {
    close() {
      this.dialog = false;
      this.turtle.remove();

      this.turtlehead.remove();
      this.dateKey += 1;
      this.turtle_name = "";
    },
    save() {
      
      console.log(this.latitude);
      this.$axios
        .$post("/submit-sample", {
          latitude: `${this.latitude}`,
          longitude: `${this.longitude}`,
          turtle_name: this.turtle_name,
          photo_date: this.date,
          photo1: this.turtle
            .generateDataUrl()
            .replace("data:image/png;base64,", ""),
          photo2: this.turtlehead
            .generateDataUrl()
            .replace("data:image/png;base64,", ""),
        })
        .then((_) => {
          this.dialog = false;
        })
        .catch((error) => {
          if (error.response.data.detail === 102) {
            this.helpMessageType = "error";
            this.showHelpMessage = true;
            this.helpMessage = error.response.data.error;
            this.has_exif = false;
          }
        });
      this.turtle_name = "";
      this.turtle.remove();
      this.turtlehead.remove();
      this.date = new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      ).toISOString();
      this.dateKey += 1;
    },
  },
};
</script>