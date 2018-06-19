# prc-sites
the domain list which is in prc

爬`www.hao123.com`，拿到所有网站及其载入资源（css、js、image）的域名。

这样PRC网站的域名基本就齐全了，可以作为智能路由的白名单，配合PAC文件，进行智能上网。

需要安装Firefox和[geckodriver](https://github.com/mozilla/geckodriver)

推荐用一台[HTPC](https://polr.liuboping.com/pOXO9)做家庭服务器，或者
在VPS上（例如[搬瓦工](https://polr.liuboping.com/9zuU9)、[Vultr](https://polr.liuboping.com/PrgTf)、
[ChangeIP](https://polr.liuboping.com/changeip)、[PnzHost](https://polr.liuboping.com/pnzhost)），
定时自动生成国内域名白名单，导入到[mono-pac](https://github.com/lbp0200/mono_pac)，
再生成pac文件，浏览器就可以直接使用在线PAC了。

### 配合mono-pac
复制生成的`result/prc-sites.txt`内容，到`mono-pac`的`whiteList`，执行`mono-pac`的`src/make.py`。