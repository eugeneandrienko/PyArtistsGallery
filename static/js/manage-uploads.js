$("#inputFile").fileinput(
    {
        'allowedFileTypes': ['image'],
        'allowedPreviewTypes': ['image'],
        'previewSettings': {
            image: {width: "auto", height: "100px"},
            other: {width: "80px", height: "100px"},
        },
        'maxFileSize': 102400, // 100 MB max.
        'showUpload': false,
        'showUploadedThumbs': false,
        'removeLabel': 'Clear'
    }
);

// Populate select (list of albums) with values
$.getJSON("/api/get-albums-list-short", function(data) {
    var items = [];
    $("#selectAlbum").empty();
    $.each(data, function(key, val) {
        $("#selectAlbum").append('<option value="' + val.id.toString() + '">' + val.name + '</option>');
    });
});
