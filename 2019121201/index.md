1.5U の L3 スイッチを機内手荷物として持ち込んだことがある技術四課のテツカです（2002年当時）。

さて、今回は AWS re:Invent 2019 で発表された AWS Transit Gateway Multicast を検証しました。<a href="#1">[1]</a>

> AWS Transit Gateway Multicast を使用すると、クラウドでマルチキャストアプリケーションを構築し、接続された数千の仮想プライベートクラウドネットワークにデータを配信することが容易になります。
>
> マルチキャストは、単一のデータストリームを多数のユーザーに同時に配信します。 これは、ニュース記事や株価などのマルチメディアコンテンツやサブスクリプションデータをサブスクライバーグループにストリーミングするための好ましいプロトコルです。
>
> 引用元： <a href="https://aws.amazon.com/jp/blogs/news/aws-transit-gateway-adds-multicast-and-inter-regional-peering/">AWS Transit Gatewayにマルチキャストとインターリージョンピアリング機能を追加</a>

# 制限・考慮事項

現時点ではバージニア北部のみ対応のようです。<a href="#2">[2]</a>

> マルチキャストは米国東部 (バージニア北部) で利用できます。
>
> 引用元： <a href="https://aws.amazon.com/jp/blogs/news/aws-transit-gateway-adds-multicast-and-inter-regional-peering/">AWS Transit Gatewayにマルチキャストとインターリージョンピアリング機能を追加</a>

下記の制限を避けるため、検証では Nitro インスタンスを使用します。<a href="#1">[3]</a><a href="#2">[4]</a>

> If you use a non-Nitro instance, you must disable the Source/Dest check. For information about disabling the check, see Changing the Source or Destination Checking in the Amazon EC2 User Guide for Linux Instances.
> A non-Nitro instance cannot be a multicast sender.
>
> <a href="https://docs.aws.amazon.com/ja_jp/vpc/latest/tgw/tgw-multicast-overview.html">Multicast on Transit Gateways</a>

# 検証構成
- US East (N. Virginia) us-east-1 に VPC を 2 つ作成します
- ここに t3.micro の EC2 を 3 台設置します（mc0, mc1, mc2） 
  - mc0 と mc1 は同一 Subnet に設置
  - mc2 のみ別 VPC/Subnet に設置
- 2 つの VPC を Transit Gateway で接続します

<img src="http://blog.serverworks.co.jp/tech/wp-content/uploads/2019/12/29-1.png" width="663" class="alignnone size-full wp-image-77139" />

- 下記は Trasnsit Gateway multicast domain 設定です<a href="#5">[5]</a>

<img src="http://blog.serverworks.co.jp/tech/wp-content/uploads/2019/12/tgwm.png" alt="" width="2628" class="alignnone size-full wp-image-76910" />

### Group IP Address: 239.192.0.29
- Source: mc0
- Member: mc1, mc2

### Group IP Address: ff18::beef
- Source: mc0
- Member: mc1, mc2

# 検証内容

## 2. IPv4 マルチキャスト配信
- mc0 から `ping 239.192.0.29` を実行します
- ICMP echo request が mc1 と mc2 の両方に配信されることを確認します

## 3. IPv6 マルチキャスト配信
- mc0 から `ping6 ff18::beef` を実行します
- ICMP6 echo request が mc1 と mc2 の両方配信されることを確認します

# 結果
mc0 からマルチキャスト IP アドレス宛の ping を実行し、mc1 と mc2 の両方に配信されることを確認できました。
下記は上から順に mc0, mc1, mc2 のターミナルです。ping と ping6 を 3 発づつ送信しています。

<img src="http://blog.serverworks.co.jp/tech/wp-content/uploads/2019/12/beef29.gif" alt="" width="1492" class="alignnone size-full wp-image-76909" />

## 気づいたこと
- マウスポチポチで L3 マルチキャストネットワークを作成できます
- Group IP Address/Source/Member の紐付けは手動設定です
- Source と Member は同一 Subnet も可です
- Group IP Address にブロードキャストは設定できません（エラーになります）
- 次の制限により、VRRP 等の制御系プロトコルで遊ぶことは難しそうです
  - 同一 Group IP Address に複数の Source を設定できません
  - 1 つの Subnet が所属できる Multicast domain は 1 つのみです

# 最後に

※ なんかガイドが更新されたような...MLD サポート!?

> We support Multicast Listener Discovery (MLD) on IPv4 and IPv6 for managing group membership.
> 
> <a href="https://docs.aws.amazon.com/ja_jp/vpc/latest/tgw/tgw-multicast-overview.html">Multicast on Transit Gateways</a>

# 参考リンク
<li id="1">[1] <a href="https://aws.amazon.com/jp/blogs/news/aws-transit-gateway-adds-multicast-and-inter-regional-peering/">AWS Transit Gatewayにマルチキャストとインターリージョンピアリング機能を追加</a></li>
<li id="2">[2] <a href="https://docs.aws.amazon.com/ja_jp/vpc/latest/tgw/tgw-multicast-overview.html">Multicast on Transit Gateways</a></li>
<li id="3">[3] <a href="https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/instance-types.html#ec2-nitro-instances">Nitro ベースのインスタンス</a></li>
<li id="4">[4] <a href="https://docs.aws.amzoマルチかｙn.com/ja_jp/AWSEC2/latest/UserGuide/using-eni.html#change_source_dest_check">送信元または送信先チェックの変更</a></li>
<li id="5">[5] <a href="https://docs.aws.amazon.com/ja_jp/vpc/latest/tgw/working-with-multicast.html">Working with Multicast</a></li>

