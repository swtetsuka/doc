# シェルスクリプトで表計算

さっそく試してみましょう!

## 準備
シェルスクリプトが動作するターミナルを用意します
- Win: WSL, Amazon Linux/Cloud9 等
- Mac: ターミナル

## ウォームアップ

入力はコマンド、ファイルどちらでも構いません。

### Q1. 空白を '_' に置換してください
入力
```
1 2 3 4 5 6 7 8 9 
```

出力
```
1_2_3_4_5_6_7_8_9
```

例)
```
echo {1..9} | tr ' ' '_'
```

### Q2. 3 ワード 毎に改行してください
入力
```
1 2 3 4 5 6 7 8 9 
```

出力
```
1 2 3
4 5 6
7 8 9
```

例)
```
echo {1..9} | xargs -n 3
```

### Q3. 改行をスペースに変換し 1 行にしてください
入力
```
1 2 3
4 5 6
7 8 9
```

出力
```
1 2 3 4 5 6 7 8 9 
```

例)
```
echo {1..9} | xargs -n 3 | xargs
```

### 04. 2 行目の合算を出力してください
入力
```
1 2 3
4 5 6
7 8 9
```

出力
```
4 5 6 15
```

例)
```
echo {1..9} | xargs -n 3 | awk 'NR==2 {print $1, $2, $3, $1+$2+$3}'
```

### 05. 2 列目の合算を出力してください
入力
```
1 2 3
4 5 6
7 8 9
```

出力
```
2
5
8
15
```

例)
```
echo {1..9} | xargs -n 3 | awk '{sum+=$2; print $2} END {print sum}'
```

## 実践
- チームスピリットの工数実績ページの一番下にある月次稼働より、ジョブ工数の合算を求めましょう
- 月次集計をテキストエディタにコピー&ペーストをすると、次の様なフォーマットになるので、これを入力にします

入力例
```
[名前1]ジョブ名1
23:26
[名前2]ジョブ名2
16:36
[名前1] ジョブ名2
13:00
``` 

出力例
```
[名前1]ジョブ名1 23.4333
[名前2]ジョブ名2 16.6
[名前1]_ジョブ名2 13
計 53.0333
```

フィルタ例
```
# ファイルにペースト
cat << EOS > file
入力を貼り付け
EOS

# フィルタ実行
cat file |
tr ' ' '_' |
xargs -n 2 |
tr ':' ' ' |
awk '{print $1, $2*60+$3}' |
awk '{sum+=$2; print $1, $2} END {print "計",sum}' |
awk '{print $1, $2/60}'
```

もし時間があれば、次も試してみましょう
- 特定の[名前]のみを合算する
- 工数を hh:mm 形式に戻す # ここら辺から手段が目的に変わりがち

以上
