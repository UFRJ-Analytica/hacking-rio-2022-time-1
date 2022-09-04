<template>
  <v-app>
    <v-main>
      <v-toolbar color="#08649c">
        <v-btn v-if="$route.path === '/home'" icon left @click="to">
          <v-icon>mdi-logout</v-icon>
        </v-btn>
        <v-btn
          v-else-if="$route.path !== '/'"
          icon
          left
          @click="to"
        >
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <v-btn
          v-else
          disabled
          icon
          left
        >
        </v-btn>
        <v-spacer></v-spacer>
        <a href="https://oceanpact.com/">
          <img src="../static/marca-removebg-preview.png" height="50px" alt="Oceanpact" />
        </a>
        

        <v-toolbar-title style="color: white">
        Turtle Head
        </v-toolbar-title>


      </v-toolbar>
      <v-container style="padding-top: 30px">
        <Nuxt />
      </v-container>
    </v-main>
    <v-footer color="#08649c" padless>
      <v-col class="text-center" style="color: white" cols="12">
          <a href="https://ufrjanalytica.ml/">
            <!-- <img
                    src="/logo_horizontal_invertido.png"
                    height="40px"
                    alt="UFRJ Analytica"
                    /> -->
            <img src="/branco_com_brasao.png" height="25px" alt="UFRJ Analytica" />
          </a>
      </v-col>
    </v-footer>
  </v-app>
</template>

<style>
a {
  color: #696969;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: calc(100% - 65px);
}
.v-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: calc(100% - 65px);
}
</style>

<script>
  export default {
  data() {
    return {};
  },
  methods: {
    to() {
      this.$router.go(-1);
    },
  },
};
</script>