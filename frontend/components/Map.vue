<template>
  <v-container>
    <h2>Por onde anda essa tartaruga?</h2>
    <div>
      <Plotly
        :data="plotly_data"
        :layout="layout"
        :display-mode-bar="false"
      ></Plotly>
    </div>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      map: null,

      myCoordinates: {
        latitude: 0,
        longitude: 0,
      },
      zoom: 7,
      plotly_data: [],
      layout: {
        mapbox: {
          style: "carto-positron",
          center: {
            lon: -43.2001796,
            lat: -22.9365994,
          },
          zoom: 2,
        },
      },
    };
  },
  async created() {
    let filterDict = {};
    filterDict["nome"] = this.$route.params.nome;
    filterDict["date"] = "";
    filterDict["cidade"] = "";
    filterDict["estado"] = "";
    let lat = []
    let lon = []
    let text = []
    const response = await this.$axios.$post(`/filter-samples`, filterDict);
    response["Samples"].forEach((item) => {
        lat.push(item.latitude);
        text.push(`${item.cidade}, ${item.estado}`);
        lon.push(item.longitude);
    });
    this.plotly_data = [{
      width: 180,

      height: 180,
      type: "scattermapbox",
      mode: "markers+text",
      text: text,
      lon: lon,
      lat: lat,
      marker: {
        size: 7,
        line: {
          width: 10,
        },
      },
      name: "Canadian cities",
      //   textposition: [],
    }]
    console.log(this.plotly_data);
  },
};
</script>
