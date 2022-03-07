from re import sub
import os

from crf_pos.api import downloader
from crf_pos.normalization.tokenizer import clean_text


class Normalizer:
    def __init__(self, downloading: bool = False):
        if downloading: Normalizer.get_resources()
        self.dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "/"
        self.dic1 = self.load_dictionary(self.dir_path + 'model/normalizer/Dic1_new.txt')
        self.dic2 = self.load_dictionary(self.dir_path + 'model/normalizer/Dic2_new.txt')
        self.dic3 = self.load_dictionary(self.dir_path + 'model/normalizer/Dic3_new.txt')

    @staticmethod
    def get_resources():
        load_dir = 'https://raw.githubusercontent.com/MohammadForouhesh/Parsivar/master/parsivar/resource/normalizer'
        save_dir = os.path.dirname(os.path.realpath(__file__)) + '/model/normalizer/'
        os.makedirs(save_dir, exist_ok=True)
        for ind in range(1, 4):
            downloader(path=load_dir + f'/Dic{ind}_new.txt', save_path=save_dir + f'Dic{ind}_new.txt', mode='wb')

    @staticmethod
    def load_dictionary(file_path):
        dictionary = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for words in lines:
                word = words.split(' ')
                dictionary[word[0].strip()] = sub('\n', '', word[1].strip())
        return dictionary

    @staticmethod
    def space_correction(text: str) -> str:
        text = sub(r'^(بی|می|نمی)( )', r'\1‌', text)
        text = sub(r'( )(می|نمی|بی)( )', r'\1\2‌', text)
        pattern = r'( )(هایی|ها|های|ایی|هایم|هایت|هایش|هایمان|هایتان|هایشان|ات|ان|ین' \
                  r'|انی|بان|ام|ای|یم|ید|اید|اند|بودم|بودی|بود|بودیم|بودید|بودند|ست)( )' \
                  r'( )(طلبان|طلب|گرایی|گرایان|شناس|شناسی|گذاری|گذار|گذاران|شناسان|گیری|پذیری|بندی|آوری|سازی|' \
                  r'بندی|کننده|کنندگان|گیری|پرداز|پردازی|پردازان|آمیز|سنجی|ریزی|داری|دهنده|آمیز|پذیری' \
                  r'|پذیر|پذیران|گر|ریز|ریزی|رسانی|یاب|یابی|گانه|گانه‌ای|انگاری|گا|بند|رسانی|دهندگان|دار)( )'
        text = sub(pattern, r'‌\2\3', text)
        return sub(r'( )(شده|نشده)( )', r'‌\2‌', text)

    def space_correction_plus1(self, text: str) -> str:
        out_sentences = ''
        for word in text.split(' '):
            try:                out_sentences += ' ' + self.dic1[word]
            except KeyError:    out_sentences += ' ' + word
        return out_sentences

    def space_correction_plus2(self, text: str) -> str:
        out_sentences = ''
        words = text.split(' ')
        if len(words) < 2:
            return text
        cnt = 1
        for i in range(0, len(words) - 1):
            w = words[i] + words[i + 1]
            try:
                out_sentences += ' ' + self.dic2[w]
                cnt = 0
            except KeyError:
                if cnt == 1:    out_sentences += ' ' + words[i]
                cnt = 1
        if cnt == 1:            out_sentences += ' ' + words[-1]
        return out_sentences

    def space_correction_plus3(self, text: str) -> str:
        out_sentences = ''
        words = text.split(' ')
        if len(words) < 3:   return text
        cnt = 1
        cnt2 = 0
        for i in range(0, len(words) - 2):
            w = words[i] + words[i + 1] + words[i + 2]
            try:
                out_sentences = out_sentences + ' ' + self.dic3[w]
                cnt = 0
                cnt2 = 2
            except KeyError:
                if cnt == 1 and cnt2 == 0:  out_sentences += ' ' + words[i]
                else:                       cnt2 -= 1
                cnt = 1
        if cnt == 1 and cnt2 == 0:          out_sentences += ' ' + words[-2] + ' ' + words[-1]
        elif cnt == 1 and cnt2 == 1:        out_sentences += ' ' + words[-1]
        return out_sentences

    def normalize(self, text: str, new_line_elimination: bool = False):
        normalized_string = clean_text(text, new_line_elimination).strip()
        return self.space_correction(
            self.space_correction_plus1(
                self.space_correction_plus2(
                    self.space_correction_plus3(normalized_string)))).strip()
