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
    var id = $(this).val();
    var url = '/api/get-pictures-list';
    $('#pictures-table').bootstrapTable('refresh',
                                        {
                                            silent: true,
                                            url: url,
                                            query: {album_id: id}
                                        });
});
