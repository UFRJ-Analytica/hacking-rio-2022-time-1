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
  data() {
    return {
      dialog: false,
      turtle_name: "",
      turtle: {},
      dateKey: 0,
      turtlehead: {},
      date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
    };
  },
  methods: {
    close (){
      this.dialog = false
      this.turtle_name = ""
    },
    save() {
      this.dialog = false;
      this.$axios.$post("/submit-sample", {
          turtle_name: this.turtle_name,
          photo_date: this.date,
          photo1: this.turtle.generateDataUrl().replace("data:image/png;base64,", ""),
          photo2: this.turtlehead.generateDataUrl().replace("data:image/png;base64,", ""),
      });
      this.turtle_name = ""
      this.turtle = {}
      this.turtlehead = {}
      this.date =  new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString()


    },
  },
};
</script>