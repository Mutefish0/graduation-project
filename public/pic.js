~function () {
    var input = document.getElementById('input');
    var preview = document.getElementById('preview');
    var result = document.getElementById('result');

    input.addEventListener('change', readFile);

    function readFile() {
        var file = input.files[0];
        if (file.type.indexOf('image') < 0) {
            alert('上传的图片格式不正确，请重新选择');
            input.vaule = '';
            return;
        }

        result.innerHTML = '';
         var reader = new FileReader();
         reader.readAsDataURL(file);
         reader.onload = loadImage;
    }

    function loadImage() {
        preview.src = this.result;
        upload({
            data: this.result.split(',')[1]
        });
    }

    var upload = (function () {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var jsond = JSON.parse(xhr.responseText);
                result.innerHTML = jsond.numbers.join(', ');
            }
        }
        return function (json) {
            xhr.open('POST', './pd_pic')
            xhr.setRequestHeader('Content-Type', 'application/json')
            xhr.send(JSON.stringify(json))
        }
    })();

}()
