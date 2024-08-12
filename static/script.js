document.getElementById('uploadButton').addEventListener('click', function() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('uploadResult').innerText = data.message;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('downloadButton').addEventListener('click', function() {
    const fileKey = document.getElementById('fileKey').value;
    const fileName = document.getElementById('fileName').value;

    fetch(`/download/${fileName}`)
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        a.remove();
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
