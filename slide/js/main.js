    var slideshow = remark.create({
      highlightStyle: 'monokai'
    });
    //从新标签页打开链接
    var allLinks = document.getElementsByTagName("a");
    for (var i = 0; i != allLinks.length; i++) {
      allLinks[i].target = "_blank";
    }