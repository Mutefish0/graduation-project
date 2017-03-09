~ function () {
    var elcv = document.getElementById('cv'),
        elcorrect = document.getElementById('correct')
        cv = elcv.getContext('2d'),
        height = elcv.height,
        width = elcv.width,
        startRecogT = null

    cv.strokeStyle = '#fff'
    cv.lineWidth = 8
    cv.lineCap = 'round'
    cv.lineJoin = 'round'

    elcv.addEventListener('mousedown', start)
    elcv.addEventListener('mouseup', end)

    // 鼠标移动
    function move (e) {
        cv.lineTo(e.clientX - elcv.offsetLeft, e.clientY - elcv.offsetTop)
        cv.stroke()
    }

    // 开始一次笔画
    function start (e) {
        clearTimeout(startRecogT)
        cv.beginPath()
        cv.moveTo(e.clientX - elcv.offsetLeft, e.clientY - elcv.offsetTop)
        elcv.addEventListener('mousemove', move)
    }

    // 结束一次笔画
    function end (e) {
        elcv.removeEventListener('mousemove', move)
        startRecogT = setTimeout(startRecognize, 1500)
    }

    // 开始处理识别
    function startRecognize () {
        var rect = getTargetRect()
        cv.strokeStyle = 'green'
        cv.lineWidth = 2
        cv.strokeRect(rect[0], rect[1], rect[2], rect[3])
        cv.strokeStyle = '#fff'
        cv.lineWidth = 8

        var imageData = cv.getImageData(rect[0], rect[1], rect[2], rect[3]),
            jsonData = imageDataToJson(imageData)

        upload({
            width: imageData.width,
            height: imageData.height,
            data: jsonData,
            correct: elcorrect.value
        })
    }

    // 识别完毕
    var recognized = (function () {
        var el = document.getElementById('recognize')
        return function (number) {
            el.innerHTML = number
            elcorrect.value = ''
            cv.clearRect(0, 0, width, height)
        }
    }) ()

    function imageDataToJson (imageData) {
        var jsonData = []
        for (var y = 0; y < imageData.height; y++) {
            jsonData[y] = []
            for (var x = 0; x < imageData.width; x++) {
                jsonData[y][x] = imageData.data[4 * (imageData.width * y + x)]
            }
        }
        return jsonData
    }

    function getTargetRect () {
        var minX = null, minY = null, maxX = null, maxY = null,
            data = cv.getImageData(0, 0, width, height).data,
            minx = getMinX(data),
            miny = getMinY(data),
            maxx = getMaxX(data),
            maxy = getMaxY(data)
        return [minx, miny, maxx - minx, maxy - miny]
    }

    var upload = (function () {
        var xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                recognized(JSON.parse(xhr.responseText).number)
            }
        }
        return function (json) {
            xhr.open('POST', '/pd')
            xhr.setRequestHeader('Content-Type', 'application/json')
            xhr.send(JSON.stringify(json))
        }
    })()

    function getMinX (data) {
        for (var x = 0; x < width; x++) {
            for (var y = 0; y < height; y++) {
                if (data[4 * (width * y + x)])
                    return x
            }
        }
    }

    function getMinY (data) {
        for (var y = 0; y < height; y++) {
            for (var x = 0; x < width; x++) {
                if (data[4 * (width * y + x)])
                    return y
            }
        }
    }

    function getMaxX (data) {
        for (var x = width - 1; x > -1; x--) {
            for (var y = 0; y < height; y++) {
                if (data[4 * (width * y + x)])
                    return x
            }
        }
    }

    function getMaxY (data) {
        for (var y = height - 1; y > -1; y--) {
            for (var x = 0; x < width; x++) {
                if (+data[4 * (width * y + x)])
                    return y
            }
        }
    }

} ()
