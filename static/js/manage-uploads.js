$("#inputFiles").fileinput(
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
