"""OpenCVを使ってMHRのお守りを確認するツール."""

# このツールのベース幅高さはフルHD
BASE_WIDTH = 1920
BASE_HEIGHT = 1080
# 対象デバイス 数値ならデバイスID、パス指定でファイル。
DEVICE_TARGET = 0
# キャプチャのサイズ指定
CAP_WIDTH = 1920
CAP_HEIGHT = 1080

PATH_TEMPORARY = 'tmpdir/tmp_{}.png'

SKILL_NAMES = [
  [
    '攻撃',
    '挑戦者',
    'フルチャージ',
    '逆恨み',
    '死中に活',
    '見切り',
    '超会心',
    '弱点特効',
    '力の解放',
    '渾身',
    '会心撃【属性】',
    '達人芸',
    '火属性攻撃強化',
    '水属性攻撃強化',
    '氷属性攻撃強化',
    '雷属性攻撃強化',
    '龍属性攻撃強化',
    '毒属性強化',
  ],
  [
    '麻痺属性強化',
    '睡眠属性強化',
    '爆破属性強化',
    '匠',
    '業物',
    '弾丸節約',
    '剛刃研磨',
    '心眼',
    '弾導強化',
    '鈍器使い',
    '集中',
    '強化持続',
    'ランナー',
    '体術',
    'スタミナ急速回復',
    'ガード性能',
    'ガード強化',
    '攻めの守勢',
  ],
  [
    '抜刀術【技】',
    '抜刀術【力】',
    '納刀術',
    'ＫＯ術',
    'スタミナ奪取',
    '滑走強化',
    '笛吹き名人',
    '砲術',
    '砲弾装填',
    '特殊射撃強化',
    '通常弾・連射矢強化',
    '貫通弾・貫通矢強化',
    '散弾・拡散矢強化',
    '装填拡張',
    '装填速度',
    '反動軽減',
    'ブレ抑制',
    '速射強化',
  ],
  [
    '防御',
    '精霊の加護',
    '体力回復量ＵＰ',
    '回復速度',
    '早食い',
    '耳栓',
    '風圧耐性',
    '耐震',
    '泡沫の舞',
    '回避性能',
    '回避距離ＵＰ',
    '火耐性',
    '水耐性',
    '氷耐性',
    '雷耐性',
    '龍耐性',
    '属性やられ耐性',
    '毒耐性',
  ],
  [
    '麻痺耐性',
    '睡眠耐性',
    '気絶耐性',
    '泥雪耐性',
    '爆破やられ耐性',
    '植生学',
    '地質学',
    '破壊王',
    '幸運',
    '砥石使用高速化',
    'ボマー',
    'キノコ大好き',
    'アイテム使用強化',
    '広域化',
    '満足感',
    '火事場力',
    '不屈',
    'ひるみ軽減',
  ],
  [
    'ジャンプ鉄人',
    '剥ぎ取り鉄人',
    '腹減り耐性',
    '飛び込み',
    '陽動',
    '乗り名人',
    '翔蟲使い',
    '壁面移動',
    '逆襲',
    '高速変形',
    '鬼火纏',
    '災禍転福',
    '合気',
    '供応',
    'チャージマスター',
    '攻勢',
    'チューンアップ',
    '研磨術【鋭】',
  ],
  [
    '刃鱗磨き',
    '壁面移動【翔】',
    '連撃',
  ],
]

POINTS_SKILL1_NAME = [1550, 399, 230, 32]
POINTS_SKILL2_NAME = [1550, 475, 230, 32]
POINTS_SKILL1_LV = [1790, 440, 90, 25]
POINTS_SKILL2_LV = [1790, 516, 90, 25]
POINTS_SLOT_1 = [1750, 300, 41, 36]
POINTS_SLOT_2 = [1792, 300, 41, 36]
POINTS_SLOT_3 = [1834, 300, 41, 36]
POINTS_SKILL_LIST = [1546, 184, 250, 684]
