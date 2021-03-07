$(document).ready(function() {
    var clipboard = new ClipboardJS('#copy_path', {
        target: function(e) {
            return e.parentNode;
        }
    });
    clipboard.on('success', function(e) {
        alert('复制成功！');
    });
    clipboard.on('error', function(e) {
        alert('复制失败！');
    });
    // 监听iframe点击时间
    let iframe = document.getElementById('chatIframe'); 
    iframe.onload = function onload (){
        $(iframe.contentDocument.getElementById('close')).on('click', function () {
            $('div#webchat').removeClass('webchat');
            $('div#webchat').addClass('chat-close');
        });
    }
    // 监听消息按钮
    $('div.tool-button').on('click', function () {
        $('div#webchat').addClass('webchat');
        $('div#webchat').removeClass('chat-close');
    });
});