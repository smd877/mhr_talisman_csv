# MHR お守りをcsvに出力するツール.

dockerを使ってなるべく簡単に検証できるようにした。
自分もすぐコマンド忘れるのでコマンド実行も書いておく。

### イメージの立ち上げまで

```
// イメージのビルド。 mhr_talisman_csv と名前を付けておく。
$ docker image build -t mhr_talisman_csv .
// イメージの実行。
$ docker run -itd --name mhr_talisman_csv -v カレントディレクトリのパス:/opt mhr_talisman_csv
// コンテナにシェルで入る。
$ docker exec -it mhr_talisman_csv /bin/sh

// python コマンドを実行してimport cv2が動けばok
# cd /opt
# python
Python 3.10.8 (main, Oct 13 2022, 22:58:41) [GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> img = cv2.imread('tmpl_skill_lvs.png')
>>> exit()
# exit

// 不要になったコンテナを捨てる場合は以下。
$ docker stop mhr_talisman_csv; docker rm mhr_talisman_csv; docker rmi mhr_talisman_csv
```

### 主な使い方

```
// 動画ファイルを指定して解析してみる
# cd /opt
# python
>>> import talisman_util as t
>>> t.check_loop('sample_movie.mp4')
攻撃,3,,0,3,1,0
回避性能,2,弱点特効,1,4,0,0
逆恨み,3,力の解放,2,3,0,0
終了
>>> exit()
# exit
```

### 注意点

dockerで動かす場合、キャプチャーボードの入力をPCに流しても、それをイメージに渡す方法は調べていません。
各自対応してくださいね。