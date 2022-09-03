<template>
  <v-container>
    <p>
      As tonalidades mais escuras do mapa indicam que a Unidade de conservação
      precisa de mais atenção. Essa estimativa foi feita avaliando a relação
      entre o capital humano e o desmatamento.
    </p>
    <Plotly :data="data" :layout="layout" :display-mode-bar="false"></Plotly>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      data: [
        {
          type: "scattergeo",
          mode: "markers+text",
          text: [
            "Montreal",
            "Toronto",
            "Vancouver",
            "Calgary",
            "Edmonton",
            "Ottawa",
            "Halifax",
            "Victoria",
            "Winnepeg",
            "Regina",
          ],
          lon: [
            -73.57, -79.24, -123.06, -114.1, -113.28, -75.43, -63.57, -123.21,
            -97.13, -104.6,
          ],
          lat: [
            45.5, 43.4, 49.13, 51.1, 53.34, 45.24, 44.64, 48.25, 49.89, 50.45,
          ],
          marker: {
            size: 7,
            color: [
              "#bebada",
              "#fdb462",
              "#fb8072",
              "#d9d9d9",
              "#bc80bd",
              "#b3de69",
              "#8dd3c7",
              "#80b1d3",
              "#fccde5",
              "#ffffb3",
            ],
            line: {
              width: 1,
            },
          },
          name: "Canadian cities",
          textposition: [
            "top right",
            "top left",
            "top center",
            "bottom right",
            "top right",
            "top left",
            "bottom right",
            "bottom left",
            "top right",
            "top right",
          ],
        },
      ],
      layout: {
        mapbox: {
          style: "carto-positron",
          center: {
            lon: -50,
            lat: -20,
          },
          zoom: 3.5,
        },
      },
    };
  },

  // async mounted() {
  // const response = await this.$axios.$get("/generateRandomData");
  // console.log(response)
  // console.log(this)
  // this.data.push(response)
  // },
};
</script>

<style>
</style>