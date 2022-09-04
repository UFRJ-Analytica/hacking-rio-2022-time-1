<template>
  <v-container>
    <v-container>
      <h2>Conheça o {{ $route.params.nome }}</h2>
      <br />
      <v-carousel :show-arrows="true" height="350">
        <v-carousel-item
          v-for="(item, i) in items"
          :key="i"
          :src="item.src"
        ></v-carousel-item>
      </v-carousel>
    </v-container>
    <Map />
  </v-container>
</template>

<script>
export default {
  async mounted() {
    let filterDict = {};
    filterDict["nome"] = this.$route.params.nome;
    filterDict["date"] = "";
    filterDict["cidade"] = "";
    filterDict["estado"] = "";
    const response = await this.$axios.$post(`/filter-samples`, filterDict);
    this.items = response["Samples"].map((item) => {
      return {
        src: `data:image/png;base64,${item.imagem_corpo.slice(2, -1)}`,
      };
    });
  },
  data() {
    return {
      items: [],
    };
  },
};
</script>

<style scoped>
</style>
