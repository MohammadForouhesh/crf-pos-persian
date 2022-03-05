from crf_pos.crf import POSTagger
from crf_pos.api import downloader

downloader('https://github.com/MohammadForouhesh/crf-pos-persian/releases/download/v1/perpos.model')
pos_tagger = POSTagger("model/perpos-v1.model")
tokens = "ابراهیم رئیسی رئيس‌جمهور جمهوری اسلامی ایران می‌باشد".split()
print(pos_tagger[tokens][0][1])