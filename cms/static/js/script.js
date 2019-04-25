$(function () {
    function render_time() {
        return moment($(this).data('timestamp')).format('lll')
    }
    $('[data-toggle="tooltip"]').tooltip(
        {title: render_time}
    );
});

$('#js-go_top').gotoTop({
    offset : 500, //距离顶部的位置
    speed : 300, //移动到顶部的速度
    /*     iconSpeed : 300, //icon动画样式的速度*/
    animationShow : {
        'transform' : 'translate(0,0)',
        'transition': 'transform .5s ease-in-out'
    }, //icon动画样式显示时
    animationHide : {
        'transform' : 'translate(80px,0)',
        'transition': 'transform .5s ease-in-out'
    } //icon动画样式隐藏时
});
