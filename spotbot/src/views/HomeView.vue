<template>
  <div class="home">
    <img class="logo" alt="Vue logo" src="../assets/logo.png">
    <div class="title_text">SpotBot</div>
    <SearchBar />
    <SearchResults />
    <album-modal />
  </div>
</template>

<script>
import SearchBar from '@/components/SearchBar.vue'
import SearchResults from '@/components/SearchResults.vue'
import AlbumModal from '@/components/AlbumModal.vue'

export default {
  name: 'HomeView',
  components: {
    SearchBar,
    SearchResults,
    AlbumModal
  }
}
</script>

<style scoped>
.logo {
  width: 18rem;
  padding: 2rem;
  margin: auto;
  display: block;
}

.title_text {
  color: white;
  font-size: 5em;
  text-align: center;
  font-family: 'helvetica';
  margin-top: -0.5em;
  margin-bottom: 0.4em;
}
</style>
