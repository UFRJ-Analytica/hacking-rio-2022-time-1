<template>
  <v-container>
    <v-row>
      <v-col>

        <v-container>
              
              <v-row>
                
                <v-btn color="orange darken-3" class="white--text">
                  <v-icon left>mdi-camera</v-icon>
                  Adicionar uma foto
                </v-btn>
              </v-row>
              <v-row>
                
                <v-dialog v-model="dialog" width="500">
                  <template v-slot:activator="{ on, attrs }">
                    <a style="font-size: 15px; margin-top: 3px;" v-bind="attrs" v-on="on" class="disabled-link">Como funciona?</a>
                  </template>
      
                  <v-card>
                    <v-card-title class="text-h5 grey lighten-2">
                      Privacy Policy
                    </v-card-title>
      
                    <v-card-text>
                      
                    </v-card-text>
      
                    <v-divider></v-divider>
      
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="primary" text @click="dialog = false">
                        I accept
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
  export default {
    data () {
      return {
        dialog: false,
      }
    },
  }
</script>
<style scoped>

</style>

