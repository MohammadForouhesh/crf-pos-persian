# Persian Parts-of-Speech tagger

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/MohammadForouhesh/crf-pos-persian/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/MohammadForouhesh/crf-pos-persian/?branch=main)
[![Code Coverage](https://scrutinizer-ci.com/g/MohammadForouhesh/crf-pos-persian/badges/coverage.png?b=main)](https://scrutinizer-ci.com/g/MohammadForouhesh/crf-pos-persian/?branch=main)
[![Build Status](https://scrutinizer-ci.com/g/MohammadForouhesh/crf-pos-persian/badges/build.png?b=main)](https://scrutinizer-ci.com/g/MohammadForouhesh/crf-pos-persian/build-status/main)
[![Code Intelligence Status](https://scrutinizer-ci.com/g/MohammadForouhesh/crf-pos-persian/badges/code-intelligence.svg?b=main)](https://scrutinizer-ci.com/code-intelligence)
[![Maintainability](https://api.codeclimate.com/v1/badges/26cc09040c2262f3ecb7/maintainability)](https://codeclimate.com/github/MohammadForouhesh/crf-pos-persian/maintainability)
![Last commit](https://img.shields.io/github/last-commit/MohammadForouhesh/crf-pos-persian)
![ask]

[ask]: https://img.shields.io/badge/Ask%20me-anything-1.svg

[![Downloads](https://pepy.tech/badge/crf-pos)](https://pepy.tech/project/crf-pos)
[![Downloads_per_month](https://pepy.tech/badge/crf-pos/month)](https://pepy.tech/project/crf-pos)

This repository contains Persian Part of Speech tagger based on Conditional Random Fields and a native Text Normalizer.

# Table of Contents
1. [TO-DO](#todo)
2. [Installation](#install)
   1. [Using Pip](#pip)
   2. [From Source](#source)
   3. [Nn CoLab](#colab)
3. [Usage](#usage)
4. [Implementation Details](#implementation-details)
5. [Evaluation](#eval)
6. [How To Contribute](#contrib)

[comment]: <> (5. [I/O]&#40;#tpa_io&#41;)

[comment]: <> (6. [Motivation]&#40;#tpa_motiv&#41;)

[comment]: <> (7. [Related Works]&#40;#tpa_lit&#41;)

[comment]: <> (8. [Contributions of this paper]&#40;#tpa_contribution&#41;)

[comment]: <> (9. [Proposed Method]&#40;#tpa_method&#41;)

[comment]: <> (10. [Experiments]&#40;#tpa_exp&#41;)


## TO-DO: <a name="todo"></a>

- [x] CRF tagger [commit#64](https://github.com/MohammadForouhesh/crf-pos-persian/commit/c0897ae7534ff322a594808c6ff1d2b4f12b627b)
- [x] Wapiti tagger [commit#56](https://github.com/MohammadForouhesh/crf-pos-persian/commit/9b267ad01d5ccac162fe9d29071c6ea22d34804f)
- [x] Native Normalizer [pull#4](https://github.com/MohammadForouhesh/crf-pos-persian/pull/4#issuecomment-1060246648)
- [x] UnitTesting [commit#127](https://github.com/MohammadForouhesh/crf-pos-persian/commit/8c0c6d4ae9908d29c39e326bf1a3d14947555141)
- [x] CI/CD [pull#5](https://github.com/MohammadForouhesh/crf-pos-persian/pull/5#issuecomment-1060697450)
- [x] Scrutinize Coverage [issue#8](https://github.com/MohammadForouhesh/crf-pos-persian/issues/8#issue-1162353982)
- [x] Documentation [pull#9](https://github.com/MohammadForouhesh/crf-pos-persian/pull/9#issuecomment-1061754671)
- [x] Improve Coverage [pull#9](https://github.com/MohammadForouhesh/crf-pos-persian/pull/9#issuecomment-1061754671)  
- [x] Smooth Installation [issue#12](https://github.com/MohammadForouhesh/crf-pos-persian/issues/12) [pull#13](https://github.com/MohammadForouhesh/crf-pos-persian/pull/13)
- [x] Excel code quality [pull#11](https://github.com/MohammadForouhesh/crf-pos-persian/pull/11)
- [x] Adding documentation and flowchart of the code.
- [x] CircleCI CI/CD Pipeline Config [issue#14](https://github.com/MohammadForouhesh/crf-pos-persian/issues/14)

## Installation: <a name="install"></a>
### Using Pip <a name="pip"></a>
```shell
! pip install crf_pos
```

### From Source <a name="source"></a>
```shell
$ git clone https://github.com/MohammadForouhesh/crf-pos-persian 
$ cd crf-pos-persian
$ python setup.py install
```
### On CoLab <a name="colab"></a>
```shell
! pip install git+https://github.com/MohammadForouhesh/crf-pos-persian.git
```

## Usage <a name="usage"></a>

```jupyterpython
from crf_pos.pos_tagger.wapiti import WapitiPosTagger
pos_tagger = WapitiPosTagger()
tokens = 'او رئیس‌جمهور حجتالاسلاموالمسلمین ابرهیم رئیسی رئیس جمهور ایران اسلامی می باشد'
pos_tagger[tokens]

[1]: 
[('او', 'PRO'),
('رئیس\u200cجمهور', 'N'),
('حجت\u200cالاسلام\u200cوالمسلمین', 'N'),
('ابرهیم', 'N'),
('رئیسی', 'N'),
('رئیس\u200cجمهور', 'N'),
('ایران', 'N'),
('اسلامی', 'ADJ'),
('می\u200cباشد', 'V')]
```

## Implementation Details <a name="implementation-details"></a>
[![](https://mermaid.ink/svg/pako:eNptkkFvgjAUx79K0xMkQgQ8kehh4i7ObVGTRccOFSo2g5aVdnFTv_sKlA0YPfW99-u_7_3bC4xYjKEPE47yE9gGIQVq3RlH5B-RFaUkPzDEYyDwWZjAsmZg7150kSUFeGQ8Qyn5xvxWHy3kodZCdVyumHAcCcIoeFj_ZVeTSu-KokhmMkUCX8HKa9W9gbrbqrsDdadVd4Bl24qYG0Z0wtG7qQYo4w7kllBFOX3M7fZia87tc153JrsBvT44CWmNYhrXm5Vj_JoJJCWW8i7TPqvjGTqbpibdFnnogprwWoTgXQRoZtJmsOBoQGjvgumUVe1WoafCGdi1n32LkuT_kzvNfLtSL2iuKj2wig-JOAbz9b3ZYhZDzAvKiSBmI7aomluODeOTCdz4Eehsz9DluM6_1rpa8flpYwmUvIUUjmCG1Zclsfr0l_JMCMUJZziEvtpSLJUnaQhDelOozGP1rRYxEYxDpZcWeASRFGzzRSPoCy5xAwUElU5q6vYDbdLy1Q)](https://mermaid.ink/svg/pako:eNptkkFvgjAUx79K0xMkQgQ8kehh4i7ObVGTRccOFSo2g5aVdnFTv_sKlA0YPfW99-u_7_3bC4xYjKEPE47yE9gGIQVq3RlH5B-RFaUkPzDEYyDwWZjAsmZg7150kSUFeGQ8Qyn5xvxWHy3kodZCdVyumHAcCcIoeFj_ZVeTSu-KokhmMkUCX8HKa9W9gbrbqrsDdadVd4Bl24qYG0Z0wtG7qQYo4w7kllBFOX3M7fZia87tc153JrsBvT44CWmNYhrXm5Vj_JoJJCWW8i7TPqvjGTqbpibdFnnogprwWoTgXQRoZtJmsOBoQGjvgumUVe1WoafCGdi1n32LkuT_kzvNfLtSL2iuKj2wig-JOAbz9b3ZYhZDzAvKiSBmI7aomluODeOTCdz4Eehsz9DluM6_1rpa8flpYwmUvIUUjmCG1Zclsfr0l_JMCMUJZziEvtpSLJUnaQhDelOozGP1rRYxEYxDpZcWeASRFGzzRSPoCy5xAwUElU5q6vYDbdLy1Q)

## Evaluation <a name="eval"></a>
Test and training is perfomed on Mojgan Seraji's [Uppsala Persian Corpus](https://sites.google.com/site/mojganserajicom/home/upc)

|Part-of-Speech| Description | precision|   recall|   f1-score|    support|
|--------------|-----------|---------|-----------|-----------|---------|
|          N   |    Noun   |   0.985 |     0.970 |    0.977  |    186585 | 
|          P   |Preposition|   0.998 |     0.998 |     0.998 |     89450 |
|          V   |    Verb   |   0.999 |     0.999 |    0.999  |     87762 | 
|        ADV   |    Adverb |   0.976 |     0.972 |    0.974  |     15983 |
|        FW    |Foreign Word|  0.989 |     0.992 |     0.991 |     2784  |
|        DET   | Determiner|   0.973 |     0.977 |    0.975  |     19786 |
|        ADJ   | Adjective |   0.978 |     0.975 |    0.977  |     61526 |
|        INT   |Interjection|  1.000 |     1.000 |    1.000  |     73    |
|       CONJ   |Conjunction|   0.996 |     0.997 |    0.997  |     74796 |
|        PRO   |   Pronoun |   0.973 |     0.974 |    0.973  |     23094 |
|        NUM   |   Numeral |   0.988 |     0.992 |     0.990 |     24864 |
||
|   <b> avg/total </b> |  -  |    0.985 |   0.985 |    0.985  |  586703|
    
## How To Contribute <a name="contrib"></a>

   1.   Report any encountered error trough [[BUG]](https://github.com/MohammadForouhesh/crf-pos-persian/issues/new?assignees=MohammadForouhesh&labels=bug&template=bug_report.md&title=%5Bbug%5D)
   2.   Report if Normalizer mis-out half-space correction trough [[ZWNJ]](https://github.com/MohammadForouhesh/crf-pos-persian/issues/new?assignees=MohammadForouhesh&labels=enhancement&template=half-space-request.md&title=%5BZWNJ%5D) 
