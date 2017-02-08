# -*- coding: utf-8 -*-

import tweepy
import team9_lib_jojo
import random
import re

# ------------------------
# Twitter APIの準備
# ------------------------
consumer_key        = 'xrKH2EMIGGAOe2bz42Hb5lOQ4'
consumer_secret     = 'zwtSjaubs2SKZLrouCHFEkD6PQxWdOdyHmloKvsQ9xTbVrq96V'
access_token        = '800596419073540096-oEbWG4AxwDBVrSptsd1rH760YdluYdl'
access_token_secret = 'XVwJrL5pIFXxvQEUqqYTXgu732xO38W4fQu4UzLCa3Mew'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# ------------------------
# チーム９の処理
# ------------------------

# {'諭吉側の単語':'ジョジョっぽい単語', '諭吉側の単語':'ジョジョっぽい単語', '諭吉側の単語':'ジョジョっぽい単語', ...}
# {'精神': '黄金の精神', '世界': '世界（ザ・ワールド）ッ！',}
jojo_words = [['善人','空条承太郎'],['悪人','悪人、DIO'],['学者','海洋学者(空条承太郎)'],['石','石仮面'],['鉄面', '石仮面'],['薄弱', '薄弱！薄弱ゥ！'],['貧弱', '貧弱！貧弱ゥ！'],['貧富', '貧富！貧富ゥ！'],['母', 'ママッ子（マンモーニ）'],['精神', '黄金の精神'], ['世界', '世界（ザ・ワールド）ッ！'],['魂', 'ツェペリ魂'],['非常', 'ディ・モールト'],['誇り', '『誇り』'],['失礼', '失礼（し・トウ・れい）ィィィィィ～～～'],['愚民', '変幻自在の砂の「愚者(フール)」'],['愚人', '変幻自在の砂の「愚者(フール)」'],['自由自在', '変幻自在の砂の「愚者(フール)」'],['下々', 'たかが虫ケラ'],['下人', 'とるにたらぬ人間どもよ！'],['未来', '未来（フューチャー）'],['スピリット', 'スタンド'],['驚き', 'スタンドも月までブッ飛ぶこの衝撃・・・']]
# 母音に左右されない語尾
# ['単語','単語','単語','単語','単語','単語','単語','単語',....]
jojo_footers = ['そこにシビれる！あこがれるゥ！','アリアリアリアリアリアリ、アリーヴェデルチ！',' YES I AM！','チュミミ～ン！！','レロレロレロレロレロ...','ドゥー・ユゥー・アンダスタンンンンドゥ！','しかし「クレイジーＤ」！！　ドララララララララララララ','やれやれだぜ。','だからおれが裁く','だが断る。','…なんていうか…その…下品なんですが…勃起…しちゃいましてね…','！！','...フハハハハハ　フフフフ　フハフハフハフハ',' ＷＲＹＹＹＹＹＹＹＹＹＹーーーーーーッ','メモっておけよなー 几帳面によぉ～～～','コラァーーッ！']

japanese = [
	["ア","カ","サ","タ","ナ","ハ","マ","ヤ","ラ","ワ","ガ","ザ","ダ","バ"],
	["イ","キ","シ","チ","ニ","ヒ","ミ","リ","ギ","ジ","ヂ","ビ"],
	["ウ","ク","ス","ツ","ヌ","フ","ム","ユ","ル","グ","ズ","ヅ","ブ"],
	["エ","ケ","セ","テ","ネ","ヘ","メ","レ","ゲ","ゼ","デ","ベ"],
	["オ","コ","ソ","ト","ノ","ホ","モ","ヨ","ロ","ヲ","ゴ","ゾ","ド","ボ"]
]

# 母音に左右される語尾
# [
#   ['ァァ', 'ァン！！'],
#   ['イィ'],
#   [],
#   [],
#   [],
# ]
jojo_footers_boin = [
   ['ァーーーッ', 'ァン！！','あ～ッ！！','ァァァァァァァアアア！','……','アアアア！','ァァアァ！！','ああ～～～～～っ！？','ャアアあああ～～～～～～ン！','ーーーーッ！！','ッ！','ッ！！','ッーーーッ！！'],
   ['イィ！','イイイイイイ！！','ィィィイイイイ！','ィィーーーっ！？','ィ！','イーーーッ！！','い〜ッ！！','ーーーーッ！！','ッ！','ッ！！','ッーーーッ！！'],
   ['ゥ！','ウーーーッ！！','う〜ッ！！','ゥゥゥゥゥゥウウウ！！','ウウウウウウウウ！','ーーーーッ！！','ッ！','ッ！！','ッーーーッ！！'],
   ['ぇッー！','エーーーッ！！','え〜ッ！！','ェェェェェェエエエ！','エエエエエエ！！','ーーーーッ！！','ッ！','ッ！！','ッーーーッ！！'],
   ['ォォォォ－－－－－ッ！！','ォ～～～～～～～～～～～～ッ！','ォオオオ～～～～～～～～～～ッ！！','ォ！','オーーーッ！！','お〜ッ！！','ーーーーッ！！','ッ！','ッ！！','ッーーーッ！！'],
]

# ['単語','単語','単語','単語','単語','単語','単語','単語',....]
jojo_headers = ['ふるえるぞハート！燃えつきるほどヒート！！','無駄だ無駄ァァァッ！言ったはずだジョニィ・ジョースター！','スイませェん…','ジャイロ！','ジョオニィ・ジオシュタァー…','いいか、ドッピオ…','ドッピオよ…おおドッピオ…わたしのかわいいドッピオ…','ブチャラティィィィィィィィィィ！','おいペッシッ！','ジョルノッ！','最高に『ハイ！』ってやつだアアアアア！','たとえるなら！','気づくのが遅いんだよアホレイツォ！','オラオラオラオラオラオラオラオラァァ！','無駄無駄無駄無駄無駄無駄無駄無駄ァ！','DIO、','承太郎、','この岸辺露伴が、','フフフ…','ズギュウウウン！！','ＵＵＵＲＲＲＲＹＹＹ！！','貧弱！ 貧弱ゥ！','KWAHHH！','うむむむ～～～んんんんんん、','クックックッ　最終ラウンドだ！  ','ウリイイイイヤアアアッー！','俺はバカだからよぉ～～～、','ウダウダ言ってんじゃあねーぞこのタコ！','グレートでスよ こいつはぁ～～～っ！','死んだ人に言うのも何だけどよ・・・','チクショーーッッ！','ルン！ルン！ルン！ぬウフフフフ、']


japanese = [
 ["ア","カ","サ","タ","ナ","ハ","マ","ヤ","ラ","ワ","ガ","ザ","ダ","バ"],
 ["イ","キ","シ","チ","ニ","ヒ","ミ","リ","ギ","ジ","ヂ","ビ"],
 ["ウ","ク","ス","ツ","ヌ","フ","ム","ユ","ル","グ","ズ","ヅ","ブ"],
 ["エ","ケ","セ","テ","ネ","ヘ","メ","レ","ゲ","ゼ","デ","ベ"],
 ["オ","コ","ソ","ト","ノ","ホ","モ","ヨ","ロ","ヲ","ゴ","ゾ","ド","ボ"]
]
# 母音を決定
def getLastBoin(last_char):
	last_boin = -1
	for i, char_set in enumerate(japanese):
		for char in char_set:
			if last_char == char.decode("utf-8"):
				last_boin = i
	return last_boin



# 変数originalにオリジナルの名言クラスのインスタンスを代入。
factory = team9_lib_jojo.MeigenFactory()
original = factory.random() # Meigenクラスのインスタンス
while original.getLength() > 47:
	original = factory.random()
print original
print "------------------------------"
original_morphemes = original.getMorphemes()

# ---------------------
material_morphemes = jojo_words

# ジョジョ文体化処理
for i, original_morpheme in enumerate(original_morphemes):
	for material_morpheme in material_morphemes:
		# 当てはまる単語があった場合は置き換える
		if original_morpheme[0] == material_morpheme[0]:
			original_morphemes[i][0] = material_morpheme[1]
			break
	# 1/5の確立で名詞を「」で囲む
	if not random.randint(0,4) and re.match(r"名詞.+一般", original_morpheme[1]):
		original_morphemes[i][0] = "「" + original_morphemes[i][0] + "」"

	# 助詞が来たらfootersをつける
	if re.match(r"助詞.+一般", original_morpheme[1]):
		joshi = original_morpheme[2].decode("utf-8")
		last_joshi_char = joshi[len(joshi)-1:]
		last_joshi_boin = getLastBoin(last_joshi_char)

		original_morphemes[i][0] = original_morphemes[i][0] + random.choice(jojo_footers_boin[last_joshi_boin])

# ジョジョ文体にした単語を連結して文字列を生成
result = "".join([original_morpheme[0] for original_morpheme in original_morphemes])

# ---------------------
# 語尾に追加
# ---------------------
# 最後の文字を抽出
last_word = original_morphemes[len(original_morphemes)-1][2].decode("utf-8")
last_char = last_word[len(last_word)-1:]
last_boin = getLastBoin(last_char)

result = result + random.choice(jojo_footers_boin[last_boin])
# 1/2
if not random.randint(0,1):
	result = result + random.choice(jojo_footers)


# ---------------------
# 文頭に追加
# ---------------------
# 2/3
if random.randint(0,2):
	result = random.choice(jojo_headers) + result

print result

# ツイート
try:
	api.update_status(status=result)
	
except tweepy.TweepError as e:
	print e
