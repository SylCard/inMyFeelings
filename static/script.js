function spotify_redirect(){
  var scopes = 'user-library-read user-read-currently-playing user-top-read playlist-modify-public user-follow-read';
  var redirect_uri = 'https://inmyfeelings.me/logged'
  var url = 'https://accounts.spotify.com/authorize' +
    '?response_type=code' +
    '&client_id=' + '1f6e7665f5c74cf8bc7d1c880321b6f3' +
    (scopes ? '&scope=' + encodeURIComponent(scopes) : '') +
    '&redirect_uri=' + encodeURIComponent(redirect_uri);

    window.location.replace(url);
}
