About
=======

Webページ全体のScreenShot画像を取得するDockerコンテナです。
Google Chromeのheadlessを使っています。
縦長のWebページでもだいたい上手くScreenShotをとることができます。
固定ヘッダーがあっても概ね大丈夫ですが、固定フッターはおそらく変な結果になると思います。

Requirements
------------
以下の環境で動作を確認しています。

* macOS High Sierra 0.13.3
* Docker Community Edition Version 18.03.0-ce-mac59

How To Use
=========

```bash
docker run -v `pwd`:/tmp/screenshot mokemokechicken/capture_web <URL> <output_image.png> [options]
```

or

```bash
./capture <URL> <output_image.png> [options]
```

例
----

### PC
```bash
docker run -v `pwd`:/tmp/screenshot mokemokechicken/capture_web "https://www.yahoo.co.jp/" yahoo_pc.png
```

### iPhone
```bash
docker run -v `pwd`:/tmp/screenshot mokemokechicken/capture_web "https://www.yahoo.co.jp/" yahoo_sp.png -w 414x735 --ua 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
```

HELP
----

```bash
% docker run -v `pwd`:/tmp/screenshot mokemokechicken/capture_web
usage: screenshot.py [-h] [-w WINDOW_SIZE] [--ua USER_AGENT] [--wait WAIT]
                     [-v] [--vv]
                     url filename

positional arguments:
  url              specify URL
  filename         specify capture image filename

optional arguments:
  -h, --help       show this help message and exit
  -w WINDOW_SIZE   specify window size like 1200x800
  --ua USER_AGENT  specify user-agent
  --wait WAIT      specify wait seconds after scroll
  -v               set LogLevel to INFO
  --vv             set LogLevel to DEBUG
```

How To Build
===========

```bash
./build
```
