<template>
  <v-container>
    <v-row>
      <v-col>
        <h2>Explorar</h2>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-container>
          <v-row>
            <v-col>
              <p>
                (Latitude {{Math.round(myCoordinates.latitude*100, )/100 }} / Longitude: {{Math.round(myCoordinates.longitude*100)/100 }})
            </p>
            </v-col>
          </v-row>
          <v-row>
            <Upload :latitude="myCoordinates.latitude" :longitude="myCoordinates.longitude"></Upload>
          </v-row>
          <v-row>
            <v-dialog v-model="dialog" width="500">
              <template v-slot:activator="{ on, attrs }">
                <a
                  style="font-size: 15px; margin-top: 3px"
                  v-bind="attrs"
                  v-on="on"
                  class="disabled-link"
                  >Como funciona?</a
                >
              </template>

              <v-card>
                <v-card-title class="text-h5 grey lighten-2">
                  Reconhecimento das tartarugas
                </v-card-title>
                <br>
                <v-card-text> 
                  As cabeças das tartarugas possuem um padrão único, servindo como uma impressão digital. Quando você encontrar uma tartaruga, tire uma foto que inclua a parte superior da cabeça dela (preferencialmente). Em seguida, faça upload no nosso site que identificaremos se você enontrou uma tartaruga nova ou se ela já está na nossa base. Não esqueça de perimitir o uso do GPS! Sua localização será usada unicamente para mapear a aparição das tartarugas.
                </v-card-text>

                <v-divider></v-divider>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" text @click="dialog = false">
                    Entendido
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-row>
        </v-container>
      </v-col>
    </v-row>
    <v-col>
      <Table></Table>
    </v-col>
  </v-container>
</template>

<script>
import Upload from "../components/upload.vue";
export default {
  data() {
    return {
      dialog: false,
      myCoordinates: {
        latitude: 0,
        longitude: 0,
      },
    };
  },
  components: { Upload },
  created() {
    this.$geolocation
      .getCurrentPosition({})
      .then((position) => {
        this.myCoordinates = position.coords;
        this.loading = false;
      })
      .catch((error) => console.log(error));
  },
};
</script>
<style scoped>
</style>

