$(function () {
    $("textarea#input-content").on("focus", function () {
        if ($(this).attr("status") === "disable") {
            $(this).val("");
            $(this).attr("status", "enable");
        }
        $(this).addClass("focus-color");
    });
    $("textarea#input-content").on("blur", function () {
        if (!$(this).val()) {
            $(this).val("说点什么吧...");
            $(this).removeClass("focus-color");
        }
        $(this).attr("status", "disable");
    });
    // websocket部分
    let ws = null;
    // 创建websocket连接
    let nick_name = '';
    let ip = '';
    let per_time = 0;
    let is_paly = false;
    if ('WebSocket' in window) {
        ws = new WebSocket(ws_url);
    } else if ('MozWebSocket' in window) {
        ws = new MozWebSocket(ws_url);
    } else {
        ws = new SockJS(ws_url);
    }
    let content = $("#chat_content");
    ws.onopen = function () {
        console.log('连接成功：', new Date());
    };
    ws.onmessage = function (event) {
        let event_data = JSON.parse(event.data);
        // console.log('获取到来自服务器消息：', event_data, event);
        if (!event_data.is_update) {
            let temp_array = make_html(event_data);
            for (let temp in temp_array) {
                if (temp) {
                    $(content).append(temp_array[temp]);
                }
            }
            let audio = $('audio#tips')[0];
            if (is_paly) {
                audio.play();
            }
        }
        $('div.scroll-title').html(`大厅（${event_data.chat_people}）`);
    };
    $("#send").on("click", click_send);
    function click_send () {
        let msg = $('#input-content').val();
        if ($('#input-content').val() && $('#input-content').val() !== '说点什么吧...') {
            msg = msg.replace('\r\n', '<br/>');
            msg = msg.replace('\n', '<br/>');
            msg = msg.replace('\r', '<br/>');
            let chat_data = JSON.stringify({'nick_name': nick_name, 'message': msg});
            $('#input-content').val("说点什么吧...");
            $('#input-content').removeClass("focus-color");
            ws.send(chat_data);
        }
        return false;
    }
    function make_html(obj) {
        let mine_class = obj.is_mine ? 'me' : 'other';
        let nick_name_img = '';
        let nick_name = obj.nick_name ? `${obj.nick_name}(${obj.ip})` : `${obj.ip}`;
        ip = obj.ip ? obj.ip : '';
        if (!obj.nick_name){
            nick_name_img = obj.ip.split('.')[3];
            if (nick_name_img.length > 2) {
                nick_name_img = nick_name_img.substr(1);
            }
        } else {
            if (obj.nick_name.length > 1) {
                nick_name_img = nick_name.substr(0, 1)
            } else {
                nick_name_img = obj.nick_name;
            }
        }
        let temp = `<div class="user-bar-${mine_class}">
                        <div class="user-image">${nick_name_img}</div>
                        <div class="message-bar">
                            <div class="user-info">${nick_name}</div>
                            <div class="message-content">${obj.message}</div>
                        </div>
                    </div>`;
        let time = 0;
        let time_stamp = new Date();
        if ((time_stamp - per_time) < (60*5)) {
            time = timeString(time_stamp);
        } else if ((time_stamp - per_time) > (60*60*24)) {
            time = timeString(time_stamp);
        }
        let time_temp = `<p class="time-bar">${time}</p>`;
        let result_array = [];
        if (time > 0) {
            result_array.push(time_temp);
        }
        result_array.push(temp);
        return result_array
    }
    $(window).unload(function () {
        ws.close();
    });
    function timeString(time, choose_date){
        let datetime = new Date();
        datetime.setTime(time);
        let year = datetime.getFullYear();
        let month = datetime.getMonth() + 1 < 10 ? "0" + (datetime.getMonth() + 1) : datetime.getMonth() + 1;
        let date = datetime.getDate() < 10 ? "0" + datetime.getDate() : datetime.getDate();
        let hour = datetime.getHours()< 10 ? "0" + datetime.getHours() : datetime.getHours();
        let minute = datetime.getMinutes()< 10 ? "0" + datetime.getMinutes() : datetime.getMinutes();
        let second = datetime.getSeconds()< 10 ? "0" + datetime.getSeconds() : datetime.getSeconds();
        let result = "";
        if (!choose_date) {
            result = hour+":"+minute+":"+second;
        } else {
            result = year+"-"+month+"-"+date+" "+hour+":"+minute+":"+second;
        }
        return result;
    }
    // 监听点击静音按钮
    $("a#m_able").on('click', function (param) {
        if (!is_paly) {
            $(this).removeClass("glyphicon-volume-off");
            $(this).addClass("glyphicon glyphicon-volume-up");
            is_paly = true;
        } else {
            $(this).removeClass("glyphicon-volume-up");
            $(this).addClass("glyphicon-volume-off");
            is_paly = false;
        }
        return false;
    });
    // 监听回车键
    $(document).keypress(function(event){
        if (event.altKey && event.witch === 13 || event.which === 10){
            $('#input-content').val($('#input-content').val()+'\n')
        }else if (event.keyCode === 13) {
            if ($('#input-content').val() !== '' && $('#input-content').val() !== '说点什么吧...'){
                $('#input-content').blur()
                click_send();
                return false
            }
            return false
        }
    });
    // 修改昵称
    $("#update").on("click", function () {
        $('#myModal').modal('hide');
        if ($("#nick_name").val() && $("#nick_name").val().length <= 8) {
            nick_name = $("#nick_name").val();
            updateNickName();
        }
    });
    // 更新全局昵称
    function updateNickName() {
        $('div.user-bar-me').each(function (i, v) {
            let user_info = `${nick_name}(${ip})`
            let nick_name_res = nick_name;
            if (nick_name.length > 1) {
                nick_name_res = nick_name.substr(0, 1);
            }
            $(v).find('div.user-image').eq(0).html(nick_name_res);
            $(v).find('div.user-info').eq(0).html(user_info);
        });
    }
});