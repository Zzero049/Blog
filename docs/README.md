# Zero的笔记

---



<div id="text" style="font-family: Helvetica, 'Hiragino Sans GB', 'Microsoft Yahei', '微软雅黑', Arial, sans-serif;"></div>



---

<p id="img"></p>

<p id="day" style="color: #8c8c8c;text-align: right"></p>



<script>$.get("http://api.youngam.cn/api/one.php",{},function (data) {
        if(data.code==200){
            var imgSrc = data.data[0].src;
            var path = '<img src="'+imgSrc+'"style="height:550px;width:900px;"/>';
            $("#img").html(path);
            $("#text").html(data.data[0].text);
            $("#day").html(data.data[0].day)
        }
    });</script>

