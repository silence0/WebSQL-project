importScripts('http://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.min.js')
        $(function(){
	$("#star-1").raty({
		hints: ['1','2', '3', '4', '5'],//自定义分数
		starOff: 'iconpic-star-S-default.png',//默认灰色星星
		starOn: 'iconpic-star-S.png',//黄色星星
		path: '.',//可以是相对路径
		number: 5,//星星数量，要和hints数组对应
		showHalf: true,
		targetKeep : true,
		click: function (score, evt) {//点击事件
			//第一种方式：直接取值
			$("#result-1").html('你的评分是'+score+'分');
		}
	});
	$("#star-2").raty({
		hints: ['1','2', '3', '4', '5'],
		starOff: 'iconpic-star-S-default.png',
		starOn: 'iconpic-star-S.png',
		path: '.',
		number: 5,
		showHalf: true,
		targetKeep : true,
		click: function (score, evt) {//点击事件
			//第一种方式：直接取值
			$("#result-2").html('你的评分是'+score+'分');
		}
	})});

$("#from12_3").({

})
