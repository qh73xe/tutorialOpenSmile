===========================
OpenSmile
===========================

:author: qh73xe
:Last Change: 21-May-2024.

.. contents::
    :depth: 2


このパートで行うこと
===========================

- OpenSmile が解決したい課題を理解する
- OpenSmile の音響特徴量の基本構成を理解する
- 読み込んだ音声データから音響特徴量を抽出する
- 抽出した音響特徴量を比較する

はじめに
===========================

:ref:`前章 <sec1>` では, 音声データを解析するときには,
ソース(音源, 基本周波数) とフィルタ(声道特性, スペクトル特性) の二つの要素を
使えば, 元の音声データを再現できる程度の情報を得られることを説明しました.
しかし, 特にスペクトル特性に関しては,
解釈が難しく, 少し使いにくい指標であることも説明しました.

このセッションで取り扱う :code:`OpenSmile` は,
この問題意識から生まれた解析ツールになります.
実は, 過去の音声, 音響学者たちは,
声帯や声道がどういう状態になっているときに
スペクトル成分にはどういう特徴が現れるかを長年研究をしてきました.

そして, 研究が進むにつれて,
特定のジャンル, 例えば感情音声においては,
大体, こういう口の動きが重要であるということもわかってきました.
この二つが組み合わさると, つまり, スペクトル特性のうち,
こういう部分を見るのが大事なのだという指標が生まれてきます.

:code:`OpenSmile` は,
このような研究をまとめ, 
代表的ないくつかの指標のセットをまとめて
基本周波数やスペクトル特性から計算することができるツールです.

この章を試すための環境構築
============================

この章を試すためには, 以下のライブラリが必要です::

    $ pip install setuptools wheel ipython # python 用インタラクティブシェル
    $ pip install numpy scipy matplotlib pandas  # 数値計算用及び可視化ライブラリ
    $ pip install opensmile  # 今回の主題である音響解析ツール. 3 章で使用.

音声を録音する (Praat 編)
===========================

.. warning::

   この章は 3 章から読み始める方に向けた記述です.

   :ref:`前章<sec1cap2>` で音声を録音している方は,
   この章は読み飛ばしてください.

さて, 解析を行うためにはまず, 音声データが必要です.
後の章では, :code:`python` コードから録音を行う方法を紹介する予定ですが,
少し複雑なので, とりあえず, :code:`Praat` から音声を録音することにしましょう.

録音は Praat を開いて :code:`New` > :code:`Record mono sound` から行います.
新規にウィンドウが開かれるので :code:`Record` ボタンを押して録音を開始します.
`Stop` ボタンを押すと :code:`Save to list` というボタンが活性化されます.
これを押すと, メインウィンドウに録音した音声が表示されます.
最後に :code:`Save` > :code:`Save as WAV file` で音声を保存します.

.. warning::

    ここでは必ず, :code:`mono sound` で録音を行ってください.
    このチュートリアルでは, モノラル音声専用の解説を行います.
    ステレオ音声をどのように解析するのかについては,
    ご自身で調べてみてください.

音声ファイルの保存先は :ref:`前章<sec0cap3>` で作成した
:code:`OpenSmileTutorial` ディレクトリに,
:code:`sample1.wav` という名前で保存してください.

:download:`sample1.wav <./wav/sample1.wav>`.


Open Smile を用いて音響特徴量を抽出する
======================================================

早速 :code:`Open Smile` を使って音響特徴量を抽出してみましょう.

先にも述べたとおり, 基本的には, 音に対するリトマス試験紙です.
これを利用する手順は大きく以下の 4 つです.

0. 試験紙を用意する = 解析用のライブラリを読み込む
1. 観察したい標本を取得する = 音声ファイルを読み込む
2. 試験紙につける = 音声ファイルから音響特徴量を抽出する
3. 色を見る = 音響特徴量を観察する

それでは, 作業を開始しましょう::

    $ ipython


Open Smile が算出する音響特徴量を観察する
------------------------------------------------------

まず試験紙を用意します::

    In [1]: from opensmile import Smile, FeatureSet, FeatureLevel
    In [2]: from scipy.io import wavfile
    In [3]: import numpy as np
    
    In [4]: smile = Smile(
       ...:     feature_set=FeatureSet.eGeMAPSv02,
       ...:     feature_level=FeatureLevel.LowLevelDescriptors,
       ...: )



試験紙の用意の仕方が :ref:`前章 <sec1cap41>` とちょっと違うことに気がつきましたか？
:ref:`前章 <sec1cap41>` では, ただ :code:`import` して入ればすぐに利用できたのに対して,
今回は :code:`Smile` というクラスをインスタンス化しています.

なぜかと言えば :code:`Open Smile` が複数の指標を
**セットでまとめて検査するキット** だからです.

この特徴量のセットの内容は
解析する目的に応じて変わります.
それを指定している箇所が :code:`feature_set` です.

このセットには色々なものがあるのですが,
今回は感情音声の解析によく使われる指標のセットである
`eGeMAPS <https://sail.usc.edu/publications/files/eyben-preprinttaffc-2015.pdf>`_
の最新バージョンを利用しています.
時間の関係で, それぞれのセットについての解説は割愛しますが,
興味がある方はリンク先を参照してください.

- `FeatureSet <https://audeering.github.io/opensmile-python/api/opensmile.FeatureSet.html#opensmile.FeatureSet.eGeMAPSv02>`_
- このページには, 利用可能な特徴量セットの一覧があります.
- また, そのセットが発表された論文へのリンクもあります.
- 現在は, emobase に関しては論文のリンクはありませんが
  `この資料 <https://audeering.github.io/opensmile/get-started.html>`_
  を読む限り, `INTERSPEECH 2010 Paralinguistic Challenge <https://mediatum.ub.tum.de/doc/1082470/document.pdf>`_ が元になっているようです.

もう一つ :code:`feature_level` という引数があります.
これは, 解析の時間軸を決める設定です.
:ref:`前章 <sec1cap4>` でみた通り, 音声データは基本的に時間軸を持っています.
そうすると, 基本的には, 各一つ一つの解析フレームに対して,
指標を得ることも可能です.
このような解析を行いたい場合には :code:`FeatureLevel.LowLevelDescriptors` を指定します.

一方で, 一つの音声といった比較的長い区間の特性を知りたい場合もあります.
例えば, ある音声のうち, 声帯振動が起きていない時間の比率や,
F0 が時間的にどのように傾いているのかなどです.
この場合には :code:`FeatureLevel.Functionals` を指定します.

:code:`feature_level` に関しては,
このチュートリアルでは, 両方ともに紹介をしていく予定ですが,
まずは, 基本となる :code:`FeatureLevel.LowLevelDescriptors`
から試してみましょう.

検査キットの用意が終わったので,
次に観察したい標本を取得します.
これは:ref:`前章 <sec1cap41>` と同様の方法で実施できます::

   In [5]: fs, x = wavfile.read("./sample1.wav")

.. note:: この部分の解説は `以下 <sec1cap41>` を参照してください.

最後に, 試験紙に標本をつけてみます::

    In [6]: result = smile.process_signal(x, fs)
    In [7]: df = result.reset_index()
    In [8]: df.head()
    Out[8]:
                       start  ... F3amplitudeLogRelF0_sma3nz
    0        0 days 00:00:00  ...                     -201.0
    1 0 days 00:00:00.010000  ...                     -201.0
    2 0 days 00:00:00.020000  ...                     -201.0
    3 0 days 00:00:00.030000  ...                     -201.0
    4 0 days 00:00:00.040000  ...                     -201.0
    
    [5 rows x 27 columns]

それなりに指標の数が多いので, 省略されてしまいますね.
とりあえず, ヘッダーを確認してみましょう::

    In [9]: df.columns.tolist()
    Out[9]:
    ['start',
     'end',
     'Loudness_sma3',
     'alphaRatio_sma3',
     'hammarbergIndex_sma3',
     'slope0-500_sma3',
     'slope500-1500_sma3',
     'spectralFlux_sma3',
     'mfcc1_sma3',
     'mfcc2_sma3',
     'mfcc3_sma3',
     'mfcc4_sma3',
     'F0semitoneFrom27.5Hz_sma3nz',
     'jitterLocal_sma3nz',
     'shimmerLocaldB_sma3nz',
     'HNRdBACF_sma3nz',
     'logRelF0-H1-H2_sma3nz',
     'logRelF0-H1-A3_sma3nz',
     'F1frequency_sma3nz',
     'F1bandwidth_sma3nz',
     'F1amplitudeLogRelF0_sma3nz',
     'F2frequency_sma3nz',
     'F2bandwidth_sma3nz',
     'F2amplitudeLogRelF0_sma3nz',
     'F3frequency_sma3nz',
     'F3bandwidth_sma3nz',
     'F3amplitudeLogRelF0_sma3nz']


:code:`start` と :code:`end` は, それぞれの解析フレームの開始時刻と終了時刻です.
それ以外の 25 行が, 音響特徴量のセットになります.

それぞれの特徴量が何を計測したものであるのかを,
以下に示します.

.. csv-table::
   :header-rows: 1

   特徴量名, 説明
   Loudness_sma3, 音圧に対する知覚強度の推定値
   alphaRatio_sma3, 50-1000 Hz と 1-5 kHz のエネルギー比
   hammarbergIndex_sma3, 0-2 kHz 領域に対する 2-5 kHz 領域の最も強いエネルギーピーク比
   slope0-500_sma3, 帯域内の対数パワースペクトルの線形回帰勾配
   slope500-1500_sma3, 帯域内の対数パワースペクトルの線形回帰勾配
   spectralFlux_sma3, 連続する 2 つのフレームのスペクトルの差の平均
   mfcc1_sma3, MFCC 第 1 次元
   mfcc2_sma3, MFCC 第 2 次元
   mfcc3_sma3, MFCC 第 3 次元
   mfcc4_sma3, MFCC 第 4 次元
   F0semitoneFrom27.5Hz_sma3nz, 27.5 Hz を基準とする半音周波数スケールでの対数 F0
   jitterLocal_sma3nz, 個々の連続した F0 の長さの偏差
   shimmerLocaldB_sma3nz, 個々の連続した F0 の振幅に対する偏差
   HNRdBACF_sma3nz, ノイズ成分に対する信号成分の比率
   logRelF0-H1-H2_sma3nz, 第 1 倍音と第 2 倍音の振幅差
   logRelF0-H1-A3_sma3nz, 第 1 倍音と第 3 フォルマント周波数に近接した倍音の振幅差
   F1frequency_sma3nz, 第 1 フォルマントの周波数
   F1bandwidth_sma3nz, 第 1 フォルマントの帯域幅
   F1amplitudeLogRelF0_sma3nz, 第 1 フォルマントの振幅
   F2frequency_sma3nz, 第 2 フォルマントの周波数
   F2bandwidth_sma3nz, 第 2 フォルマントの帯域幅
   F2amplitudeLogRelF0_sma3nz, 第 2 フォルマントの振幅
   F3frequency_sma3nz, 第 3 フォルマントの周波数
   F3bandwidth_sma3nz, 第 3 フォルマントの帯域幅
   F3amplitudeLogRelF0_sma3nz, 第 3 フォルマントの振幅


さて, 続いては音声全体の統計量を測る指標に変更してみましょう::

    In [10]: smile = Smile(
       ...:     feature_set=FeatureSet.eGeMAPSv02,
       ...:     feature_level=FeatureLevel.Functionals,
       ...: )
    In [11]: res2 = smile.process_signal(x, fs)
    In [12]: df2 = res2.reset_index()
    In [13]: df2
    Out[13]:
       start                       end  ...  StddevUnvoicedSegmentLength  equivalentSoundLevel_dBp
    0 0 days 0 days 00:00:15.924535147  ...                          0.0                 -3.026643
    
    [1 rows x 90 columns]

今度は一つの音声ファイル全体に対する評価指標であるので,
行数は :code:`1 rows` となっています.
代わりに列数は :code:`90 columns` となっています.

先ほどと同様に, どのような音響特徴量が計測されているのかを
確認してみましょう::

    In [14]: df2.columns.to_list()
    Out[14]:
    ['start',
     'end',
     'F0semitoneFrom27.5Hz_sma3nz_amean',
     'F0semitoneFrom27.5Hz_sma3nz_stddevNorm',
     'F0semitoneFrom27.5Hz_sma3nz_percentile20.0',
     'F0semitoneFrom27.5Hz_sma3nz_percentile50.0',
     'F0semitoneFrom27.5Hz_sma3nz_percentile80.0',
     'F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2',
     'F0semitoneFrom27.5Hz_sma3nz_meanRisingSlope',
     'F0semitoneFrom27.5Hz_sma3nz_stddevRisingSlope',
     'F0semitoneFrom27.5Hz_sma3nz_meanFallingSlope',
     'F0semitoneFrom27.5Hz_sma3nz_stddevFallingSlope',
     'loudness_sma3_amean',
     'loudness_sma3_stddevNorm',
     'loudness_sma3_percentile20.0',
     'loudness_sma3_percentile50.0',
     'loudness_sma3_percentile80.0',
     'loudness_sma3_pctlrange0-2',
     'loudness_sma3_meanRisingSlope',
     'loudness_sma3_stddevRisingSlope',
     'loudness_sma3_meanFallingSlope',
     'loudness_sma3_stddevFallingSlope',
     'spectralFlux_sma3_amean',
     'spectralFlux_sma3_stddevNorm',
     'mfcc1_sma3_amean',
     'mfcc1_sma3_stddevNorm',
     'mfcc2_sma3_amean',
     'mfcc2_sma3_stddevNorm',
     'mfcc3_sma3_amean',
     'mfcc3_sma3_stddevNorm',
     'mfcc4_sma3_amean',
     'mfcc4_sma3_stddevNorm',
     'jitterLocal_sma3nz_amean',
     'jitterLocal_sma3nz_stddevNorm',
     'shimmerLocaldB_sma3nz_amean',
     'shimmerLocaldB_sma3nz_stddevNorm',
     'HNRdBACF_sma3nz_amean',
     'HNRdBACF_sma3nz_stddevNorm',
     'logRelF0-H1-H2_sma3nz_amean',
     'logRelF0-H1-H2_sma3nz_stddevNorm',
     'logRelF0-H1-A3_sma3nz_amean',
     'logRelF0-H1-A3_sma3nz_stddevNorm',
     'F1frequency_sma3nz_amean',
     'F1frequency_sma3nz_stddevNorm',
     'F1bandwidth_sma3nz_amean',
     'F1bandwidth_sma3nz_stddevNorm',
     'F1amplitudeLogRelF0_sma3nz_amean',
     'F1amplitudeLogRelF0_sma3nz_stddevNorm',
     'F2frequency_sma3nz_amean',
     'F2frequency_sma3nz_stddevNorm',
     'F2bandwidth_sma3nz_amean',
     'F2bandwidth_sma3nz_stddevNorm',
     'F2amplitudeLogRelF0_sma3nz_amean',
     'F2amplitudeLogRelF0_sma3nz_stddevNorm',
     'F3frequency_sma3nz_amean',
     'F3frequency_sma3nz_stddevNorm',
     'F3bandwidth_sma3nz_amean',
     'F3bandwidth_sma3nz_stddevNorm',
     'F3amplitudeLogRelF0_sma3nz_amean',
     'F3amplitudeLogRelF0_sma3nz_stddevNorm',
     'alphaRatioV_sma3nz_amean',
     'alphaRatioV_sma3nz_stddevNorm',
     'hammarbergIndexV_sma3nz_amean',
     'hammarbergIndexV_sma3nz_stddevNorm',
     'slopeV0-500_sma3nz_amean',
     'slopeV0-500_sma3nz_stddevNorm',
     'slopeV500-1500_sma3nz_amean',
     'slopeV500-1500_sma3nz_stddevNorm',
     'spectralFluxV_sma3nz_amean',
     'spectralFluxV_sma3nz_stddevNorm',
     'mfcc1V_sma3nz_amean',
     'mfcc1V_sma3nz_stddevNorm',
     'mfcc2V_sma3nz_amean',
     'mfcc2V_sma3nz_stddevNorm',
     'mfcc3V_sma3nz_amean',
     'mfcc3V_sma3nz_stddevNorm',
     'mfcc4V_sma3nz_amean',
     'mfcc4V_sma3nz_stddevNorm',
     'alphaRatioUV_sma3nz_amean',
     'hammarbergIndexUV_sma3nz_amean',
     'slopeUV0-500_sma3nz_amean',
     'slopeUV500-1500_sma3nz_amean',
     'spectralFluxUV_sma3nz_amean',
     'loudnessPeaksPerSec',
     'VoicedSegmentsPerSec',
     'MeanVoicedSegmentLengthSec',
     'StddevVoicedSegmentLengthSec',
     'MeanUnvoicedSegmentLength',
     'StddevUnvoicedSegmentLength',
     'equivalentSoundLevel_dBp']

何か色々と増えていますが,
実は多くの内容は, 先ほどの特徴量に対して,
平均や標準偏差, パーセンタイルなどの統計量を計算しただけです.
少し, 特殊なものとして, 
F0 に対しては, 上昇傾斜や下降傾斜の回数の平均や標準偏差が計算されています.
また, 以下のような特徴量も計算されています.

.. csv-table::
   :header-rows: 1

   特徴量名, 説明

   loudnessPeaksPerSec, 一秒あたりの音圧ピークの数
   VoicedSegmentsPerSec, 一秒あたりの有声音セグメントの数
   MeanVoicedSegmentLengthSec, 有声音セグメントの平均長
   StddevVoicedSegmentLengthSec, 有声音セグメントの標準偏差
   MeanUnvoicedSegmentLength, 無声音セグメントの平均長
   StddevUnvoicedSegmentLength, 無声音セグメントの標準偏差
   equivalentSoundLevel_dBp, 等価音圧レベル



どのような音響特徴量が変化するのかを考え実際に比較する
--------------------------------------------------------


この章のまとめ
======================================================


次の章に向けて
======================================================


