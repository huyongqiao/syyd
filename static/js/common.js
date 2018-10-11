$.pt = $.pt || {};
(function ($)
{
    $.pt =
    {
        init : function () {},
        addFav : function ()
        {
            var url = window.location.href;
            var title = window.document.title;
            if (confirm("收藏名称：" + title + "\n收藏网址：" + url + "\n确定添加收藏？"))
            {
                var ua = navigator.userAgent.toLowerCase();
                if (ua.indexOf("msie 8") > -1) {
                    window.external.addToFavoritesBar(url, title);
                }
                else
                {
                    try {
                        window.external.addFavorite(url, title)
                    }
                    catch (e)
                    {
                        try {
                            window.sidebar.addPanel(title, url, "");
                        }
                        catch (e) {
                            alert("加入收藏失败，请使用Ctrl+D进行添加")
                        }
                    }
                }
            }
        },
        setHome : function (url)
        {
            if (document.all)
            {
                document.body.style.behavior = 'url(#default#homepage)';
                document.body.setHomePage(url)
            }
            else if (window.sidebar)
            {
                if (window.netscape)
                {
                    try {
                        netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect")
                    }
                    catch (e) {
                        alert("该操作被浏览器拒绝")
                    }
                }
                var prefs = Components.classes['@mozilla.org/preferences-service;1'].getService(Components.interfaces.nsIPrefBranch);
                prefs.setCharPref('browser.startup.homepage', url)
            }
        },
        backTop : function (s)
        {
            $(window).scroll(function ()
            {
                if ($(window).scrollTop() >= 200) {
                    $(s).fadeIn(500)
                }
                else {
                    $(s).fadeOut(500)
                }
            });
            $(s).click(function ()
            {
                $('body,html').animate({
                    scrollTop : 0
                }, 500);
                return false;
            })
        },
        tab : function ()
        {
            $('.pt-tab .pt-tab-nav li').on('mouseover', function ()
            {
                $(this).addClass('active').siblings().removeClass('active');
                console.log($(this).index());
                $(this).parents('.pt-tab').find('.pt-tab-con ul').eq($(this).index()).removeClass('none').siblings().addClass('none')
            })
        },
        gopos : function (s)
        {
            $('body,html').animate({
                scrollTop : $(s).offset().top
            }, 500)
        }
    }
})($);
$(function ()
{
    $.pt.backTop('.gotop');
    $.pt.tab();
    $('img').on('error', function ()
    {
        this.src = '/public/image/nocover.jpg';
    });
    $('.dropmenu').hover(function ()
    {
        $(this).addClass("hover")
    },
    function ()
    {
        $(this).removeClass("hover")
    });
    $('.searchbox .dropmenu-item li').on('click', function ()
    {
        $('[name=searchtype]').val($(this).data('type'));
        $(this).prependTo($(this).parent());
        $('.dropmenu').removeClass('hover')
    })
});
