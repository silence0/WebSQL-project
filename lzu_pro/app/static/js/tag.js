$(document).ready(function () {
    $.fn.choose = function () {
        var text = $(this).text();
        var newDom = "<span>" + text + "</span>";
        var temp = $(".choosed").append(newDom);
        this.remove();
    };
    $.fn.unchoose = function () {
        var text = $(this).text();
        var newDom = "<span>" + text + "</span>";
        var temp = $(".unchoosed").append(newDom);
        this.remove();
    };


    //初始化的时候设置标签,可以在已选择标签和可选标签里面选择
    $.fn.setTag = function (tagString,block) {
        var tagList = tagString.split(',');
        for (var i in tagList){
            $("."+block).append("<span>"+tagList[i]+"</span>")
        }
    }

    //获取已选择的标签,并且用的是','连接
    $.fn.getTag = function () {
        var tagList = []
        $('.choosed span').each(function () {
            tagList.push($(this).text())
        })
        return (tagList.join(','))
    }


    $(".unchoosed").on('click','span',$.fn.choose);
    $(".choosed").on('click','span',$.fn.unchoose);

    //test for setTag
    // $.fn.setTag('test,1,a,b','choosed');
    // $.fn.getTag()
});