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
});