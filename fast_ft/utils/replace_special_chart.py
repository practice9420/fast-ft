
html_tag = {
    '&lt;': '<', '&gt;': '>', '&apos;': "'", '&yen;': '¥',
    '&copy;': '©', '&divide;': '÷', '&times;': 'x', '&trade;': '™', '&reg;': '®', '&sect;': '§', '&euro;': '€',
    '&pound;': '£', '&cent;': '￠', '&raquo;': '»'
}


def replace_special_chart(target_str: str) -> str:
    """ 替换html特殊字符 """

    for k, v in html_tag.items():
        target_str = target_str.replace(v, k)
    return target_str


if __name__ == '__main__':
    target_str = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="referrer" content="always"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0"/>
    <link rel="shortcut icon" href="/static/favicon.ico">
    {% block block_title %}
    <title>基础模板</title>
    {% endblock %}
    {% block base_css %}
    <link rel="stylesheet" type="text/css" href="/static/webuploader/webuploader.css">
    <link rel="stylesheet" type="text/css" href="/static/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="/static/css/frameworks-32dce2faa502c3c56fb7b214ddbb6ec1.css">
    <link rel="stylesheet" type="text/css" href="/static/css/index.css">
    {% endblock %}
    {% block extend_css %}
    {% endblock %}
    {% block base_script %}
    <script src="/static/jquery-1.11.1.min.js"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js"></script>
    <script src="/static/webuploader/webuploader.min.js"></script>
    <script src="/static/js/tools.js"></script>
    {% endblock %}
    {% block extend_script %}
    {% endblock %}
</head>
<body>
    {% block nav %}
    <nav class="navbar navbar-default navbar-static-top">
      <div class="container height-full">
        <div class="row height-full">
            <div class="col-xs-3 brand-title height-full">
                <a href="/">
                    <h1></h1>
                </a>
            </div>
        </div>
      </div>
    </nav>
    {% endblock %}
    <div class="container main-body">
        {% block block_body %}
        {% endblock %}
    </div>
    {% block webchat %}
    <div class="tool-box">
        <div class="tool-button">
            <ul>
                <li class="message-button on-message">
                    <span class="glyphicon glyphicon-envelope"></span>
                </li>
            </ul>
        </div>
        <div class="chat-close" id="webchat">
            <iframe id="chatIframe" src="/webchat/"></iframe>
        </div>
    </div>
    {% endblock %}
</body>
</html>"""
    result = replace_special_chart(target_str)
    print(result)

