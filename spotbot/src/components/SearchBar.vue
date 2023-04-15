<template>
    <div>
        <input type="text" v-model="input" placeholder="Search a playlist or album" />
        <button @click="search">Search</button>
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