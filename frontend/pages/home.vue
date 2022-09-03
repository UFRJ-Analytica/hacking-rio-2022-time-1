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
            <Upload></Upload>
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
                  Privacy Policy
                </v-card-title>

                <v-card-text> </v-card-text>

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
import Upload from "../components/upload.vue";
export default {
    data() {
        return {
            dialog: false,
        };
    },
    components: { Upload }
};
</script>
<style scoped>
</style>

