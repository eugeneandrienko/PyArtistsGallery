function deleteAlbum(albumId) {
    var request = new ajaxRequest();
    request.onreadystatechange = function() {
        if (request.readyState == 4) {
            if (request.status == 200 || window.location.href.indexOf("http") == -1) {
                $('#albums-table').bootstrapTable('refresh', {silent: true})
            } else {
                alert(request.responseText)
            }
        }
    }
    var parameters = "album_id=" + albumId;
    request.open("POST", "/api/delete-album", true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.send(parameters);
}

$('#editAlbumModal').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget);
    var album_id = button.data('id');
    var album_name = button.data('name');
    var album_description = button.data('description');
    var modal = $(this);
    $("#album-id").val(album_id);
    $("#album-name").val(album_name);
    $("#album-description").val(album_description);
})

function editAlbum() {
    var request = new ajaxRequest();
    request.onreadystatechange = function() {
        if (request.readyState == 4) {
            if (request.status == 200 || window.location.href.indexOf("http") == -1) {
                $('#albums-table').bootstrapTable('refresh', {silent: true})
            } else {
                alert(request.responseText)
            }
        }
    }
    var album_id = $("#album-id").val();
    var album_name = $("#album-name").val();
    var album_description = $("#album-description").val();
    var parameters = "album_id=" + album_id + "&album_name=" + album_name + "&album_description=" + album_description;
    request.open("POST", "/api/edit-album", true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send(parameters);
}
