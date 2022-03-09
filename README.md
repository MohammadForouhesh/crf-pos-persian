# Persian Parts-of-Speech tagger

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/MohammadForouhesh/crf-pos-persian/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/MohammadForouhesh/crf-pos-persian/?branch=main)
[![Code Coverage](https://scrutinizer-ci.com/g/MohammadForouhesh/crf-pos-persian/badges/coverage.png?b=main)](https://scrutinizer-ci.com/g/MohammadForouhesh/crf-pos-persian/?branch=main)
[![Build Status](https://scrutinizer-ci.com/g/MohammadForouhesh/crf-pos-persian/badges/build.png?b=main)](https://scrutinizer-ci.com/g/MohammadForouhesh/crf-pos-persian/build-status/main)
[![Code Intelligence Status](https://scrutinizer-ci.com/g/MohammadForouhesh/crf-pos-persian/badges/code-intelligence.svg?b=main)](https://scrutinizer-ci.com/code-intelligence)
[![Maintainability](https://api.codeclimate.com/v1/badges/26cc09040c2262f3ecb7/maintainability)](https://codeclimate.com/github/MohammadForouhesh/crf-pos-persian/maintainability)
![Last commit](https://img.shields.io/github/last-commit/MohammadForouhesh/crf-pos-persian)
![ask]

[ask]: https://img.shields.io/badge/Ask%20me-anything-1.svg

This repository contains Persian Part of Speech tagger based on Conditional Random Fields and a native Text Normalizer.

# Table of Contents
1. [TO-DO](#todo)
2. [Installation](#install)
    1. [on CoLab](#colab)
3. [Usage](#usage)
4. [Evaluation](#eval)

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
- [ ] Smooth Installation
- [x] Excel code quality [pull#11](https://github.com/MohammadForouhesh/crf-pos-persian/pull/11)

## Installation: <a name="install"></a>
```shell
$ git clone https://github.com/MohammadForouhesh/crf-pos-persian 
$ cd crf-pos-persian
$ python setup.py install
```
### on CoLab <a name="colab"></a>
```shell
! pip install git+https://github.com/MohammadForouhesh/crf-pos-persian.git
```

## Usage <a name="usage"></a>

```jupyterpython
from crf_pos.pos_tagger.wapiti import WapitiPosTagger
pos_tagger = WapitiPosTagger()
tokens = text = 'او رئیس‌جمهور حجتالاسلاموالمسلمین ابرهیم رئیسی رئیس جمهور می باشد'.split()
pos_tagger[tokens]

[1]: 
[('ابراهیم', 'N'),
('رپیسی', 'N'),
('ریپس', 'ADJ'),
('جمهور', 'N'),
('جمهوری', 'N'),
('اسلامی', 'ADJ'),
('ایران', 'N'),
('میباشد', 'V')]
```
## Evaluation <a name="eval"></a>
|Part-of-Speech|  precision|   recall|      f1-score|    support|
|--------------|-----------|---------|--------------|-----------|
|          N   |     0.985 |   0.970 |       0.977  |    186585 | 
|          P   |     0.998 |   0.998 |       0.998  |     89450 |
|          V   |     0.999 |   0.999 |       0.999  |     87762 | 
|        ADV   |     0.976 |   0.972 |       0.974  |     15983 |
|       ADVe   |     0.988 |   0.978 |       0.983  |     1053  |
|        RES   |     0.989 |   0.992 |       0.991  |     2784  |
|       RESe   |     1.000 |   0.989 |       0.994  |     174   |
|        DET   |     0.973 |   0.977 |       0.975  |     19786 |
|       DETe   |     0.960 |   0.970 |       0.965  |     2156  |
|         AJ   |     0.978 |   0.975 |       0.977  |     61526 |
|        AJe   |     0.949 |   0.964 |       0.957  |     19919 |
|         CL   |     0.932 |   0.918 |       0.925  |     1892  |
|        INT   |     1.000 |   1.000 |       1.000  |     73    |
|       CONJ   |     0.996 |   0.997 |       0.997  |     74796 |
|      CONJe   |     1.000 |   1.000 |       1.000  |     82    |
|      POSTP   |     1.000 |   1.000 |       1.000  |     13174 |
|        PRO   |     0.973 |   0.974 |       0.973  |     23094 |
|       PROe   |     0.878 |   0.579 |       0.698  |     273   |
|        NUM   |     0.988 |   0.992 |       0.990  |     24864 |
|       NUMe   |     0.932 |   0.918 |       0.925  |     2519  |
|       PUNC   |     1.000 |   1.000 |       1.000  |     84088 |
|         Ne   |     0.970 |   0.985 |       0.977  |     163760|
|         Pe   |     0.986 |   0.992 |       0.989  |    10004  |
||
|   <b> avg/total </b> |     0.985 |   0.985 |       0.985  |    885797 |
    
 
