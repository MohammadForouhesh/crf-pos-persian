from cfr_pos.crf import POSTagger

pos_tagger = POSTagger("model/perpos.model")
tokens = "ابراهیم رئیسی رئيس‌جمهور جمهوری اسلامی ایران می‌باشد".split()
print(pos_tagger[tokens])