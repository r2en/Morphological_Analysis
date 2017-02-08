# -*- coding: utf-8 -*-
import MeCab
import random
import requests
import bs4
import re

class MeigenFactory:
	def random(self):
		# 学問のすすめのサイトURL
		url = u'http://www.aozora.gr.jp/cards/000296/files/47061_29420.html'

		# 学問のすすめを取得
		res = requests.get(url)
		string = bs4.BeautifulSoup(res.text.encode(res.encoding),"html.parser")
		main_text = string.select('.main_text')
		text = main_text[0].getText()

		# 学問のすすめからランダムに１文を取得
		sentences = text.encode("utf-8").split("。")
		result = random.choice(sentences).replace("\n", '').decode("utf-8")
		return Meigen(result)

class Meigen:
	def __init__(self, string):
		self.__body = string   # 文字列          ex) "天は人の上に人を造らず人の下に人を造らず"
		self.__morphemes = self.__parse(string)  # 形態素のリスト   ex) [ ["天","名刺", "テン"], ["は","助詞", "ハ"],... ]

	def getLength(self):
		return len(self.__body)

	def getMorphemes(self):
		return self.__morphemes

	def __parse(self, string):
		morphemes = []

		# 文字列（仮引数:string）を受け取り、それを形態素解析して、リストにして返す。
		# 返すリストの形は
		#   [ [ 実際の単語, 品詞, 読み ], [ 実際の単語, 品詞, 読み ], [ 実際の単語, 品詞, 読み ], ... ]という二次元配列。
		#   例えば[ ["天","名刺", "テン"], ["は","助詞", "ハ"],... ]な感じ。

		# 名言文字列からアルファベットを削除
		result = self.__remove_alphabet(string)

		# chasen形式で形態素解析
		mecab = MeCab.Tagger("-Ochasen")
		parsed_string = mecab.parse(result.encode("utf-8"))

		for line in parsed_string.split('\n'):
			line = line.rstrip('\r\n')
			if line == "EOS".encode("utf-8"):
				break
			else:
				chasen_list = line.split('\t')
				if chasen_list[0] in morphemes:
					pass
				else:
					chasen_list = [chasen_list[0], chasen_list[3], chasen_list[1]]
					morphemes.append(chasen_list)

		return morphemes

	def __remove_alphabet(self, string):
		result = u''
		for c in string:
			#!UnicodeコードポイントからUnicode文字列を判別
			if ord(c) > 255:
				result += c
		return result

	def __str__(self):
		return self.__body.encode("utf-8")
