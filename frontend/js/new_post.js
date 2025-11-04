const {
    ClassicEditor,
    Essentials,
    Bold,
    Italic,
    Font,
    Paragraph
} = CKEDITOR;

ClassicEditor
    .create(document.querySelector('#conteudo_new_post'), {
        licenseKey: 'eyJhbGciOiJFUzI1NiJ9.eyJleHAiOjE3OTM4MzY3OTksImp0aSI6IjQzNDkxNGY2LTY3MTMtNGZlOC1hNzkxLTc5ZTcyNzMyNWE0ZCIsInVzYWdlRW5kcG9pbnQiOiJodHRwczovL3Byb3h5LWV2ZW50LmNrZWRpdG9yLmNvbSIsImRpc3RyaWJ1dGlvbkNoYW5uZWwiOlsiY2xvdWQiLCJkcnVwYWwiXSwiZmVhdHVyZXMiOlsiRFJVUCIsIkUyUCIsIkUyVyJdLCJyZW1vdmVGZWF0dXJlcyI6WyJQQiIsIlJGIiwiU0NIIiwiVENQIiwiVEwiLCJUQ1IiLCJJUiIsIlNVQSIsIkI2NEEiLCJMUCIsIkhFIiwiUkVEIiwiUEZPIiwiV0MiLCJGQVIiLCJCS00iLCJGUEgiLCJNUkUiXSwidmMiOiI4OGY3NjNmMiJ9.eLfM6v4VJxL2mzX0W3KAG8P2KP-eEb26fxkMnzWki-4aSz4LR4H5wjY4whIFD0U6Xn8YPvScTOBYVmJ7GoktGQ',
        plugins: [Essentials, Bold, Italic, Font, Paragraph],
        toolbar: [
            'undo', 'redo', '|', 'bold', 'italic', '|',
            'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor'
        ]
    })
    .then( /* ... */)
    .catch( /* ... */);