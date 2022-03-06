from re import sub
import os


class Normalizer:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"

        self.dic1_path = self.dir_path + 'resource/normalizer/Dic1_new.txt'
        self.dic2_path = self.dir_path + 'resource/normalizer/Dic2_new.txt'
        self.dic3_path = self.dir_path + 'resource/normalizer/Dic3_new.txt'
        self.dic1 = self.load_dictionary(self.dic1_path)
        self.dic2 = self.load_dictionary(self.dic2_path)
        self.dic3 = self.load_dictionary(self.dic3_path)

        self.data_helper = DataHelper()

    @staticmethod
    def load_dictionary(file_path):
        dict = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            g = f.readlines()
            for Wrds in g:
                wrd = Wrds.split(' ')
                dict[wrd[0].strip()] = sub('\n', '', wrd[1].strip())
        return dict

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

    def space_correction_plus1(self, doc_string):
        out_sentences = ''
        for wrd in doc_string.split(' '):
            try:
                out_sentences = out_sentences + ' ' + self.dic1[wrd]
            except KeyError:
                out_sentences = out_sentences + ' ' + wrd
        return out_sentences

    def space_correction_plus2(self, text: str) -> str:
        out_sentences = ''
        wrds = text.split(' ')
        L = wrds.__len__()
        if L < 2:
            return text
        cnt = 1
        for i in range(0, L - 1):
            w = wrds[i] + wrds[i + 1]
            try:
                out_sentences = out_sentences + ' ' + self.dic2[w]
                cnt = 0
            except KeyError:
                if cnt == 1:
                    out_sentences = out_sentences + ' ' + wrds[i]
                cnt = 1
        if cnt == 1:
            out_sentences = out_sentences + ' ' + wrds[i + 1]
        return out_sentences

    def space_correction_plus3(self, text: str) -> str:
        out_sentences = ''
        wrds = text.split(' ')
        L = wrds.__len__()
        if L < 3:
            return text
        cnt = 1
        cnt2 = 0
        for i in range(0, L - 2):
            w = wrds[i] + wrds[i + 1] + wrds[i + 2]
            try:
                out_sentences = out_sentences + ' ' + self.dic3[w]
                cnt = 0
                cnt2 = 2
            except KeyError:
                if cnt == 1 and cnt2 == 0:
                    out_sentences = out_sentences + ' ' + wrds[i]
                else:
                    cnt2 -= 1
                cnt = 1
        if cnt == 1 and cnt2 == 0:
            out_sentences = out_sentences + ' ' + wrds[i + 1] + ' ' + wrds[i + 2]
        elif cnt == 1 and cnt2 == 1:
            out_sentences = out_sentences + ' ' + wrds[i + 2]
        return out_sentences

    def normalize(self, text: str, new_line_elimination: bool = False):
        normalized_string = self.data_helper.clean_text(text, new_line_elimination).strip()

        return self.space_correction(self.space_correction_plus1(self.space_correction_plus2(self.space_correction_plus3(normalized_string)))).strip()
