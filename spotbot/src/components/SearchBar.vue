<template>
    <div id="search_holder">
        <input type="text" v-model="input" placeholder="Search a playlist or album" class="search_bar"/>
        <button @click="search" class="search_button"><i class="fa fa-search"></i></button>
    </div>
 </template>

<script>

export default {
    name: 'SearchBar',
    data() {
        return {
            input: '',
            albums: [],
            playlists: []
        }
    },
    methods: {
        search() {
            const api_url = 'http://localhost:5001/search';
            const query_params = { q: this.input };
            fetch(api_url + '?' + new URLSearchParams(query_params), {mode: 'cors'})
                .then(response => response.json())
                .then(data => {
                    var raw_albums = data.albums.items;
                    var raw_playlists = data.playlists.items
                    var albums = this.process_albums(raw_albums);
                    var playlists = this.process_playlists(raw_playlists);
                    this.emitter.emit("search-albums", albums);
                    this.emitter.emit("search-playlists", playlists);

                })
                .catch(error => {
                    console.error('Error searching API:', error);
                });
        },
        process_albums(raw_albums) {
            var albums = [];
            raw_albums.forEach((album, index) => {
                var new_album = {};
                new_album['id'] = index;
                new_album['name'] = album.name;
                new_album['imageUrl'] = album.images[0].url;
                new_album['artist'] = album.artists[0].name;
                albums.push(new_album);
            });
            return albums;
        },
        process_playlists(raw_playlists) {
            var playlists = [];
            raw_playlists.forEach((playlist, index) => {
                var new_playlist = {};
                new_playlist['id'] = index;
                new_playlist['name'] = playlist.name;
                new_playlist['imageUrl'] = playlist.images[0].url;
                new_playlist['artist'] = playlist.owner.display_name;
                playlists.push(new_playlist);
            });
            return playlists;
        }
    }
}
</script>

<style scoped>

#search_holder {
    display: flex;
    width: 60%;
    margin: auto;
}
.search_bar{
    border: 0;
    font-size: 1.5rem;
    outline: 0;
    width: 100%;
    padding: 0.8rem 1.6rem;
    border-radius: 0.7rem;
}

.search_button {
    width: 3.3rem;
    height: 3.3rem;
    margin: 0rem 1rem;
    font-size: 1.5rem;
    border-radius: 1.5rem;
    border: 4px solid #f3ac45;
    background-color: transparent;
    outline: none;
    color: #f3ac45;
    cursor: pointer;
}
</style>