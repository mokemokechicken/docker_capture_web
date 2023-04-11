# About

Webページ全体のScreenShot画像を取得するDockerコンテナです。
Google Chromeのheadlessを使っています。
縦長のWebページでもだいたい上手くScreenShotをとることができます。
固定ヘッダーがあっても概ね大丈夫ですが、固定フッターはおそらく変な結果になると思います。

A Docker container that captures a fullpage screenshot of any given webpage.
Uses Google Chrome in headless mode.
Works well even with vertically long webpages.
Webpages with fixed headers generally work well, but fixed footers may lead to unusual results.

## Requirements

以下の環境で動作を確認しています。

Tested on the following environments

### macOS

* macOS High Sierra 10.13.3
* Docker Community Edition Version 18.03.0-ce-mac59

### Linux

* Linux 6.1
* Docker Version 23.0.1, build a5ee5b1dfc

## How To Use

### Build

```bash
./build
```

Then either run

```bash
docker run --rm -v `pwd`:/tmp/screenshot -v /dev/shm:/dev/shm mokemokechicken/capture_web <URL> <output_image.png> [options]
```

or run

```bash
./capture <URL> <output_image.png> [options]
```

## Examples

### PC

```bash
docker run --rm -v `pwd`:/tmp/screenshot -v /dev/shm:/dev/shm mokemokechicken/capture_web "https://www.yahoo.co.jp/" yahoo_pc.png
```

### iPhone

```bash
docker run --rm -v `pwd`:/tmp/screenshot -v /dev/shm:/dev/shm mokemokechicken/capture_web "https://www.yahoo.co.jp/" yahoo_sp.png -w 414x735 --ua 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
```

## Help

```bash
% docker run --rm -v `pwd`:/tmp/screenshot -v /dev/shm:/dev/shm mokemokechicken/capture_web
usage: screenshot.py [-h] [-w WINDOW_SIZE] [--ua USER_AGENT] [--wait WAIT] [--lang LANG] [--language LANGUAGE]
                     [-v] [--vv]
                     url filename

positional arguments:
  url                  specify URL
  filename             specify capture image filename

optional arguments:
  -h, --help           show this help message and exit
  -w WINDOW_SIZE       specify window size like 1200x800
  --ua USER_AGENT      specify user-agent
  --wait WAIT          specify wait seconds after scroll
  --lang LANG          set LANG environment variable
  --language LANGUAGE  set LANGUAGE environment variable
  -v                   set LogLevel to INFO
  --vv                 set LogLevel to DEBUG
```
