# Zero的笔记

---



<div id="text" style="font-family: Helvetica, 'Hiragino Sans GB', 'Microsoft Yahei', '微软雅黑', Arial, sans-serif;"></div>



---

<p id="img"></p>

<p id="day" style="color: #8c8c8c;text-align: right"></p>



<script>
    var mykey = "f7c47ddd88ca4a0c5d6d787e2214c6fb";
        $.get("https://api.tianapi.com/txapi/one/index",{key:mykey},function (data) {
            if(data.code==200){
                var imgSrc = data.newslist[0].imgurl;
                var path = '<img src="'+imgSrc+'"style="height:550px;width:980px;"/>';
                $("#img").html(path);
                $("#text").html(data.newslist[0].word);
                $("#day").html(data.newslist[0].date)
            }
        });</script>

