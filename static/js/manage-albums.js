function deleteAlbum(albumId) {
    var request = new ajaxRequest();
    request.onreadystatechange = function() {
        if (request.readyState == 4) {
            if (request.status == 200 || window.location.href.indexOf("http") == -1) {
                $('#albums-table').bootstrapTable('refresh', {silent: true})
            } else {
                alert("Cannot delete repository!")
            }
        }
    }
    var parameters = "album_id=" + albumId;
    request.open("POST", "/api/delete-album", true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.send(parameters);
}
