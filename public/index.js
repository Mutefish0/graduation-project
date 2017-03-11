~ function () {
    var elc = document.getElementById('cv'),
        elr = document.getElementById('recognize'),
        elcorrect = document.getElementById('correct'),
        cv = elc.getContext('2d'),
        height = elc.height,
        width = elc.width,
        startRecogT = null,
        x = 0,
        y = 0,
        xoffset = 0,
        yoffset = -24

    y = getTop(elc) + yoffset
    x = getLeft(elc) + xoffset

    cv.strokeStyle = '#fff'
    cv.lineWidth = 8
    cv.lineCap = 'round'
    cv.lineJoin = 'round'


    elc.addEventListener('mousedown', start)
    elc.addEventListener('mouseup', end)

    // 移动端
    elc.addEventListener('touchstart', mStart)
    elc.addEventListener('touchend', mEnd)

    window.addEventListener('resize', function () {
        y = getTop(elc) + yoffset
        x = getLeft(elc) + xoffset
    })

    function getTop (el) {
        var offset = el.offsetTop
        if(el.offsetParent != null)
            offset += getTop(el.offsetParent)
        return offset
    }

    function getLeft (el) {
        var offset = el.offsetLeft
        if(el.offsetParent != null)
            offset += getLeft(el.offsetParent)
        return offset
    }

    // 鼠标移动
    function move (e) {
        cv.lineTo(e.clientX - x, e.clientY - y)
        cv.stroke()
    }

    //移动端
    function mMove (e) {
        cv.lineTo(e.touches[0].clientX - x, e.touches[0].clientY - y)
        cv.stroke()
    }

    // 开始一次笔画
    function start (e) {
        resetView()
        clearTimeout(startRecogT)
        cv.beginPath()
        cv.moveTo(e.clientX - x, e.clientY - y)
        elc.addEventListener('mousemove', move)
    }

    //移动端
    function mStart (e) {
        resetView()
        clearTimeout(startRecogT)
        cv.beginPath()
        cv.moveTo(e.touches[0].clientX - x, e.touches[0].clientY - y)
        elc.addEventListener('touchmove', mMove)
    }

    // 结束一次笔画
    function end (e) {
        elc.removeEventListener('mousemove', move)
        startRecogT = setTimeout(startRecognize, 1500)
    }

    //移动端
    function mEnd (e) {
        elc.removeEventListener('touchmove', mMove)
        startRecogT = setTimeout(startRecognize, 1500)
    }

    // 开始处理识别
    function startRecognize () {
        var rect = getTargetRect()
        cv.strokeStyle = 'indianred'
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
    function recognized (data) {
        updateView(data)
    }

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
                recognized(JSON.parse(xhr.responseText))
            }
        }
        return function (json) {
            xhr.open('POST', './pd')
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

    function resetView () {

    }

    function updateView (data) {
        elr.innerHTML = data.number
        elcorrect.value = ''
        cv.clearRect(0, 0, width, height)

        drwaWave(data)
    }

} ()
