<template>
  <v-app>
    <v-main>
      <v-toolbar color="#08649c">
        <!-- <a href="link">
          <img src="logo" height="100px" alt="UFRJ Analytica" />
        </a> -->
        <v-spacer></v-spacer>

        <v-toolbar-title style="color: white; font-weight: bold">
        HACKINGRIO 2022
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
            <img src="/branco_com_brasao.png" height="50px" alt="UFRJ Analytica" />
          </a>
      </v-col>
    </v-footer>
  </v-app>
</template>

<style>
a {
  color: #696969;
}
</style>