# bert-chinese-ner

使用预训练语言模型BERT做中文NER尝试，fine - tune BERT模型

代码参考

- **[BERT-NER](https://github.com/kyzhouhzau/BERT-NER)，想看英文原版请务必移步**
- [BERT-TF](https://github.com/google-research/bert)

## 使用方法

从[BERT-TF](https://github.com/google-research/bert)下载bert源代码，存放在路径下bert文件夹中

从[BERT-Base Chinese](https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip)下载模型，存放在checkpoint文件夹下

使用BIO数据标注模式，使用人民日报经典数据

train：

`python BERT_NER.py --data_dir=data/ --bert_config_file=checkpoint/bert_config.json --init_checkpoint=checkpoint/bert_model.ckpt --vocab_file=vocab.txt --output_dir=./output/result_dir/`

## 结果

经过100个epoch跑出来的结果

```
eval_f = 0.9662649
eval_precision = 0.9668882
eval_recall = 0.9656949
global_step = 135181
loss = 40.160034
```

测试结果第一句：

![](test.png)
