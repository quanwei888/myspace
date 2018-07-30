#!/bin/sh

一 安装opennmt-torch

二 进入opennmt-torch目录,创建data目录,并将数据文件train.en和train.zh拷贝进data

三 数据处理:
1)处理英文
#数字替换+大写转小写
sed 's/[0-9]\+/NUM/g' data/train.en | awk '{print tolower($0)}' > data/train.en.num
#生成bpe编码
th tools/learn_bpe.lua -size 50000 -save_bpe data/train.en.num.bpe < data/train.en.num
#用bpe编码分词
th tools/tokenize.lua -bpe_model data/train.en.num.bpe < data/train.en.num > data/train.en.tok
2)处理中文
#数字替换
sed 's/[0-9]\+/ NUM /g' data/train.zh | th tools/tokenize.lua  -segment_alphabet Han > data/train.zh.tok
3)生成train数据集 
#train数据集,仅改名
mv data/train.en.tok　 data/src-train.txt
mv data/train.zh.tok  data/tgt-train.txt
#生成val数据集
paste data/src-train.txt data/tgt-train.txt | shuf -n 1000 > tmp 
cut -f1 tmp > data/src-val.txt
cut -f2 tmp > data/tgt-val.txt
rm tmp
#生成test数据集
paste data/src-train.txt data/tgt-train.txt | shuf -n 1000 > tmp
cut -f1 tmp > data/src-test.txt
cut -f2 tmp > data/tgt-test.txt
rm tmp
4)预处理,生成输入格式
python preprocess.py -max_shard_size 52428800 -report_every 10000 -tgt_vocab_size 10000 -src_seq_length 20  -train_src data/src-train.txt -train_tgt data/tgt-train.txt -valid_src data/src-val.txt -valid_tgt data/tgt-val.txt -save_data data/aic 
python train.py -data data/aic -save_model aic-model -encoder_type brnn -gpuid 1 -train_steps 10000000 -save_checkpoint_steps 2000 -keep_checkpoint 20 -train_from aic-model_step_468000.pt -learning_rate 0.1

四 训练transformer模型
python  train.py -data data/aic -save_model aic-transformer -gpuid 1 \
        -layers 6 -rnn_size 512 -word_vec_size 512   \
        -encoder_type transformer -decoder_type transformer -position_encoding \
        -train_steps 10000000  -max_generator_batches 32 -dropout 0.1 \
        -batch_size 4096 -batch_type tokens -normalization tokens  -accum_count 4 \
        -optim adam -adam_beta2 0.998 -decay_method noam -warmup_steps 8000 -learning_rate 2 \
        -max_grad_norm 0 -param_init 0  -param_init_glorot -save_checkpoint_steps 500 \
        -label_smoothing 0.1 -train_from aic-transformer_step_57500.pt

五 评估
#测试评估(咋AIC的测试50000个step后bleu达到30+
python translate.py -model aic-transformer_step_500.pt -src data/src-test.txt -tgt data/tgt-test.txt  -replace_unk -verbose -gpu 0 -report_bleu




#-----------------在opennmt-torch下运行-------------------
########en
#数字替换+大写转小写
sed 's/[0-9]\+/NUM/g' data/train.en | awk '{print tolower($0)}' > data/train.en.num
#生成bpe编码
th tools/learn_bpe.lua -size 50000 -save_bpe data/train.en.num.bpe < data/train.en.num
#用bpe编码分词
th tools/tokenize.lua -bpe_model data/train.en.num.bpe < data/train.en.num > data/train.en.tok

########zh
#数字替换
sed 's/[0-9]\+/ NUM /g' data/train.zh | th tools/tokenize.lua  -segment_alphabet Han > data/train.zh.tok


#生成train数据集
mv data/train.en.tok　 data/src-train.txt
mv data/train.zh.tok  data/tgt-train.txt

#生成val数据集
paste data/src-train.txt data/tgt-train.txt | shuf -n 1000 > tmp 
cut -f1 tmp > data/src-val.txt
cut -f2 tmp > data/tgt-val.txt
rm tmp

#生成test数据集
paste data/src-train.txt data/tgt-train.txt | shuf -n 1000 > tmp
cut -f1 tmp > data/src-test.txt
cut -f2 tmp > data/tgt-test.txt
rm tmp



#预处理数据集
th preprocess.lua -train_src data/src-train.txt -train_tgt data/tgt-train.txt -valid_src data/src-val.txt -valid_tgt data/tgt-val.txt -save_data data/voc
#训练
th train.lua -data data/voc-train.t7 -save_model ./models/model -validation_metric bleu -gpuid 1 -attention global -brnn_merge concat
th train.lua -data data/voc-train.t7 -save_model models/model -validation_metric bleu　-gpuid 1　-attention　global　-brnn_merge concat 
th train.lua -data data/voc-train.t7 -save_model model -validation_metric bleu -gpuid 1 -src_seq_length 20

#翻译
th translate.lua -model model_checkpoint.t7 -src data/src-test.txt  -gpuid 1 -output /tmp/out
th tools/tokenize.lua -segment_alphabet Han < data/tgt-test.txt > /tmp/ref.tok
sed 's/<unk>//g' /tmp/out > /tmp/out.unk
th tools/tokenize.lua -segment_alphabet Han < /tmp/out.unk > /tmp/out.tok
th tools/score.lua -scorer bleu /tmp/ref.tok < /tmp/out.tok



#OpenNMT-tf
onmt-main train_and_eval --model_type NMTSmall --config config/opennmt-defaults.yml config/data/toy-ende.yml
onmt-main infer --config config/opennmt-defaults.yml config/data/toy-ende.yml --features_file data/src-test.txt

python preprocess.py -max_shard_size 52428800 -report_every 10000 -tgt_vocab_size 10000 -src_seq_length 20  -train_src data/src-train.txt -train_tgt data/tgt-train.txt -valid_src data/src-val.txt -valid_tgt data/tgt-val.txt -save_data data/aic 
python train.py -data data/aic -save_model aic-model -encoder_type brnn -gpuid 1 -train_steps 10000000 -save_checkpoint_steps 2000 -keep_checkpoint 20 -train_from aic-model_step_468000.pt -learning_rate 0.1

#transformar模型训练
python train.py -data data/aic -save_model aic-transformer -encoder_type transformer -decoder_type transformer -gpuid 1 -train_steps 10000000 -save_checkpoint_steps 2000 -keep_checkpoint 20

python  train.py -data data/aic -save_model aic-transformer -gpuid 1 \
        -layers 6 -rnn_size 512 -word_vec_size 512   \
        -encoder_type transformer -decoder_type transformer -position_encoding \
        -train_steps 10000000  -max_generator_batches 32 -dropout 0.1 \
        -batch_size 4096 -batch_type tokens -normalization tokens  -accum_count 4 \
        -optim adam -adam_beta2 0.998 -decay_method noam -warmup_steps 8000 -learning_rate 2 \
        -max_grad_norm 0 -param_init 0  -param_init_glorot -save_checkpoint_steps 500 \
        -label_smoothing 0.1 -train_from aic-transformer_step_57500.pt

#测试评估
python translate.py -model aic-transformer_step_500.pt -src data/src-test-min.txt -tgt data/tgt-test-min.txt  -replace_unk -verbose -gpu 0 -report_bleu
