function refreshPictureTable() {
    var url = '/api/get-pictures-list';
    var id = $('#selectAlbumMPics').val();
    $('#pictures-table').bootstrapTable('refresh',
                    {
                        silent: true,
                        url: url,
                        query: {album_id: id}
                    });
}

function deletePicture(pictureId) {
    var request = new ajaxRequest();
    request.onreadystatechange = function() {
        if (request.readyState == 4) {
            if (request.status == 200 || window.location.href.indexOf("http") == -1) {
                refreshPictureTable();
            } else {
                alert(request.responseText)
            }
        }
    }
    var parameters = "picture_id=" + pictureId;
    request.open("POST", "/api/delete-picture", true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.send(parameters);
}

$('#editPictureModal').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget);
    var picture_id = button.data('id');
    var picture_name = button.data('name');
    var picture_description = button.data('description');
    var modal = $(this);
    $("#picture-id").val(picture_id);
    $("#picture-name").val(picture_name);
    $("#picture-description").val(picture_description);
})

function editPicture() {
    var request = new ajaxRequest();
    var url = '/api/get-pictures-list';
    var id = $('#selectAlbumMPics').val();
    request.onreadystatechange = function() {
        if (request.readyState == 4) {
            if (request.status == 200 || window.location.href.indexOf("http") == -1) {
                refreshPictureTable();
            } else {
                alert(request.responseText)
            }
        }
    }
    var picture_id = $("#picture-id").val();
    var picture_name = $("#picture-name").val();
    var picture_description = $("#picture-description").val();
    var parameters = "picture_id=" + picture_id + "&picture_name=" + picture_name + "&picture_description=" + picture_description;
    request.open("POST", "/api/edit-picture", true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send(parameters);
}

// Populate select (list of albums) with values
$.getJSON("/api/get-albums-list-short", function(data) {
    var items = [];
    $("#selectAlbumMPics").empty();
    $("#selectAlbumMPics").append(
        '<option value="" selected disabled style="display:none;">Select album...</option>'
    );
    $.each(data, function(key, val) {
        $("#selectAlbumMPics").append('<option value="' + val.id.toString() + '">' + val.name + '</option>');
    });
});

$('#selectAlbumMPics').change(function() {
    refreshPictureTable();
});
