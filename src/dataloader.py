
import torch
import torch.nn as nn
import torch.utils.data as data
from torch.utils.data import DataLoader

from tqdm import tqdm
import random
import logging
logger = logging.getLogger()

# from transformers import BertTokenizer
# bert_tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
from src.config import get_params
params = get_params()
from transformers import AutoTokenizer
auto_tokenizer = AutoTokenizer.from_pretrained(params.model_name)
pad_token_label_id = nn.CrossEntropyLoss().ignore_index

politics_labels = ['O', 'B-country', 'B-politician', 'I-politician', 'B-election', 'I-election', 'B-person', 'I-person', 'B-organisation', 'I-organisation', 'B-location', 'B-misc', 'I-location', 'I-country', 'I-misc', 'B-politicalparty', 'I-politicalparty', 'B-event', 'I-event']
science_labels = ['O', 'B-scientist', 'I-scientist', 'B-person', 'I-person', 'B-university', 'I-university', 'B-organisation', 'I-organisation', 'B-country', 'I-country', 'B-location', 'I-location', 'B-discipline', 'I-discipline', 'B-enzyme', 'I-enzyme', 'B-protein', 'I-protein', 'B-chemicalelement', 'I-chemicalelement', 'B-chemicalcompound', 'I-chemicalcompound', 'B-astronomicalobject', 'I-astronomicalobject', 'B-academicjournal', 'I-academicjournal', 'B-event', 'I-event', 'B-theory', 'I-theory', 'B-award', 'I-award', 'B-misc', 'I-misc']
music_labels = ['O', 'B-musicgenre', 'I-musicgenre', 'B-song', 'I-song', 'B-band', 'I-band', 'B-album', 'I-album', 'B-musicalartist', 'I-musicalartist', 'B-musicalinstrument', 'I-musicalinstrument', 'B-award', 'I-award', 'B-event', 'I-event', 'B-country', 'I-country', 'B-location', 'I-location', 'B-organisation', 'I-organisation', 'B-person', 'I-person', 'B-misc', 'I-misc']
literature_labels = ["O", "B-book", "I-book", "B-writer", "I-writer", "B-award", "I-award", "B-poem", "I-poem", "B-event", "I-event", "B-magazine", "I-magazine", "B-literarygenre", "I-literarygenre", 'B-country', 'I-country', "B-person", "I-person", "B-location", "I-location", 'B-organisation', 'I-organisation', 'B-misc', 'I-misc']
ai_labels = ["O", "B-field", "I-field", "B-task", "I-task", "B-product", "I-product", "B-algorithm", "I-algorithm", "B-researcher", "I-researcher", "B-metrics", "I-metrics", "B-programlang", "I-programlang", "B-conference", "I-conference", "B-university", "I-university", "B-country", "I-country", "B-person", "I-person", "B-organisation", "I-organisation", "B-location", "I-location", "B-misc", "I-misc"]
coustom_conll = ['O',
 'U-NAME',
 'B-SSN',
 'I-SSN',
 'L-SSN',
 'B-DATE_TIME',
 'I-DATE_TIME',
 'L-DATE_TIME',
 'B-CREDIT_DEBIT_NUMBER',
 'I-CREDIT_DEBIT_NUMBER',
 'L-CREDIT_DEBIT_NUMBER',
 'B-NAME',
 'L-NAME',
 'B-ADDRESS',
 'I-ADDRESS',
 'L-ADDRESS',
 'U-ADDRESS',
 'B-PHONE',
 'I-PHONE',
 'L-PHONE',
 'B-BANK_ACCOUNT_NUMBER',
 'I-BANK_ACCOUNT_NUMBER',
 'L-BANK_ACCOUNT_NUMBER',
 'U-DATE_TIME',
 'B-DATE_OF_BIRTH',
 'I-DATE_OF_BIRTH',
 'L-DATE_OF_BIRTH',
 'I-NAME',
 'U-SSN',
 'B-EMAIL',
 'I-EMAIL',
 'L-EMAIL',
 'B-CREDIT_DEBIT_EXPIRY',
 'I-CREDIT_DEBIT_EXPIRY',
 'L-CREDIT_DEBIT_EXPIRY',
 'B-CREDIT_DEBIT_CVV',
 'I-CREDIT_DEBIT_CVV',
 'L-CREDIT_DEBIT_CVV',
 'U-DATE_OF_BIRTH',
 'B-AGE',
 'I-AGE',
 'L-AGE',
 'U-CREDIT_DEBIT_NUMBER',
 'U-PHONE',
 'U-CREDIT_DEBIT_EXPIRY',
 'B-URL',
 'I-URL',
 'L-URL',
 'U-CREDIT_DEBIT_CVV',
 'U-EMAIL',
 'U-BANK_ROUTING',
 'U-BANK_ACCOUNT_NUMBER',
 'B-BANK_ROUTING',
 'I-BANK_ROUTING',
 'L-BANK_ROUTING',
 'U-URL',
 'U-AGE',
 'B-PIN',
 'I-PIN',
 'L-PIN',
 'U-PIN',
 'B-DRIVER_ID',
 'I-DRIVER_ID',
 'L-DRIVER_ID',
 'U-DRIVER_ID',
 'U-CREDIT_DEBIT_NUMBER_ENDING',
 'L-ADDRESS_ON_CARD',
 'I-CREDIT_DEBIT_NUMBER_ENDING',
 'U-ADDRESS_ON_CARD',
 'L-CREDIT_DEBIT_NUMBER_ENDING',
 'B-CREDIT_DEBIT_EXPIRY_DATE',
 'B-NAME_ON_CARD',
 'L-NAME_ON_CARD',
 'L-AGENT_NAME',
 'L-BANK_ROUTING_NUMBER',
 'L-CREDIT_DEBIT_EXPIRY_DATE',
 'L-BANK_ACCOUNT_NUMBER_ENDING',
 'I-BANK_ROUTING_NUMBER',
 'I-CREDIT_DEBIT_EXPIRY_DATE',
 'I-NAME_ON_CARD',
 'I-BANK_ACCOUNT_NUMBER_ENDING',
 'B-AGENT_NAME',
 'B-BANK_ACCOUNT_NUMBER_ENDING',
 'I-AGENT_NAME',
 'B-BANK_ROUTING_NUMBER',
 'U-NAME_ON_CARD',
 'U-CREDIT_DEBIT_EXPIRY_DATE',
 'I-ADDRESS_ON_CARD',
 'U-AGENT_NAME',
 'U-BANK_ACCOUNT_NUMBER_ENDING',
 'B-ADDRESS_ON_CARD',
 'B-CREDIT_DEBIT_NUMBER_ENDING']
domain2labels = {"coustom_connl":coustom_conll,"politics": politics_labels, "science": science_labels, "music": music_labels, "literature": literature_labels, "ai": ai_labels}

def read_ner(datapath, tgt_dm):
    inputs, labels = [], []
    with open(datapath, "r") as fr:
        token_list, label_list = [], []
        for i, line in enumerate(fr):
            line = line.strip()
            if line == "":
                if len(token_list) > 0:
                    assert len(token_list) == len(label_list)
                    inputs.append([auto_tokenizer.cls_token_id] + token_list + [auto_tokenizer.sep_token_id])
                    labels.append([pad_token_label_id] + label_list + [pad_token_label_id])
                
                token_list, label_list = [], []
                continue
            
            splits = line.split(" ")
            token = splits[0]
            label = splits[1]

            subs_ = auto_tokenizer.tokenize(token)
            if len(subs_) > 0:
                label_list.extend([domain2labels[tgt_dm].index(label)] + [pad_token_label_id] * (len(subs_) - 1))
                token_list.extend(auto_tokenizer.convert_tokens_to_ids(subs_))
            else:
                print("length of subwords for %s is zero; its label is %s" % (token, label))

    return inputs, labels


def read_ner_for_bilstm(datapath, tgt_dm, vocab):
    inputs, labels = [], []
    with open(datapath, "r") as fr:
        token_list, label_list = [], []
        for i, line in enumerate(fr):
            line = line.strip()
            if line == "":
                if len(token_list) > 0:
                    assert len(token_list) == len(label_list)
                    inputs.append(token_list)
                    labels.append(label_list)
                
                token_list, label_list = [], []
                continue
            
            splits = line.split("\t")
            token = splits[0]
            label = splits[1]
            
            token_list.append(vocab.word2index[token])
            label_list.append(domain2labels[tgt_dm].index(label))

    return inputs, labels



class Dataset(data.Dataset):
    def __init__(self, inputs, labels):
        self.X = inputs
        self.y = labels
    
    def __getitem__(self, index):
        return self.X[index], self.y[index]

    def __len__(self):
        return len(self.X)


PAD_INDEX = 0
class Vocab():
    def __init__(self):
        self.word2index = {"PAD": PAD_INDEX}
        self.index2word = {PAD_INDEX: "PAD"}
        self.n_words = 1

    def index_words(self, word_list):
        for word in word_list:
            if word not in self.word2index:
                self.word2index[word] = self.n_words
                self.index2word[self.n_words] = word
                self.n_words += 1

def get_vocab(path):
    vocabulary = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            vocabulary.append(line)
    return vocabulary


def collate_fn(data):
    X, y = zip(*data)
    lengths = [len(bs_x) for bs_x in X]
    max_lengths = max(lengths)
    padded_seqs = torch.LongTensor(len(X), max_lengths).fill_(auto_tokenizer.pad_token_id)
    padded_y = torch.LongTensor(len(X), max_lengths).fill_(pad_token_label_id)
    for i, (seq, y_) in enumerate(zip(X, y)):
        length = lengths[i]
        padded_seqs[i, :length] = torch.LongTensor(seq)
        padded_y[i, :length] = torch.LongTensor(y_)

    return padded_seqs, padded_y


def collate_fn_for_bilstm(data):
    X, y = zip(*data)
    lengths = [len(bs_x) for bs_x in X]
    max_lengths = max(lengths)
    padded_seqs = torch.LongTensor(len(X), max_lengths).fill_(PAD_INDEX)
    for i, seq in enumerate(X):
        length = lengths[i]
        padded_seqs[i, :length] = torch.LongTensor(seq)

    lengths = torch.LongTensor(lengths)
    return padded_seqs, lengths, y


def get_dataloader_for_bilstmtagger(params):
    vocab_src = get_vocab("ner_data/conll2003/vocab.txt")
    vocab_tgt = get_vocab("ner_data/%s/vocab.txt" % params.tgt_dm)
    vocab = Vocab()
    vocab.index_words(vocab_src)
    vocab.index_words(vocab_tgt)

    logger.info("Load training set data ...")
    conll_inputs_train, conll_labels_train = read_ner_for_bilstm("ner_data/conll2003/train.txt", params.tgt_dm, vocab)
    inputs_train, labels_train = read_ner_for_bilstm("ner_data/%s/train.txt" % params.tgt_dm, params.tgt_dm, vocab)
    inputs_train = inputs_train * 10 + conll_inputs_train
    labels_train = labels_train * 10 + conll_labels_train

    logger.info("Load dev set data ...")
    inputs_dev, labels_dev = read_ner_for_bilstm("ner_data/%s/dev.txt" % params.tgt_dm, params.tgt_dm, vocab)

    logger.info("Load test set data ...")
    inputs_test, labels_test = read_ner_for_bilstm("ner_data/%s/test.txt" % params.tgt_dm, params.tgt_dm, vocab)

    logger.info("train size: %d; dev size %d; test size: %d;" % (len(inputs_train), len(inputs_dev), len(inputs_test)))

    dataset_train = Dataset(inputs_train, labels_train)
    dataset_dev = Dataset(inputs_dev, labels_dev)
    dataset_test = Dataset(inputs_test, labels_test)
    
    dataloader_train = DataLoader(dataset=dataset_train, batch_size=params.batch_size, shuffle=True, collate_fn=collate_fn_for_bilstm)
    dataloader_dev = DataLoader(dataset=dataset_dev, batch_size=params.batch_size, shuffle=False, collate_fn=collate_fn_for_bilstm)
    dataloader_test = DataLoader(dataset=dataset_test, batch_size=params.batch_size, shuffle=False, collate_fn=collate_fn_for_bilstm)

    return dataloader_train, dataloader_dev, dataloader_test, vocab


def load_corpus(tgt_dm):
    print("Loading corpus ...")
    data_path = "enwiki_corpus/%s_removebracket.tok" % tgt_dm
    sent_list = []
    with open(data_path, "r") as fr:
        for i, line in tqdm(enumerate(fr)):
            line = line.strip()
            sent_list.append(line)
    return sent_list


def get_dataloader(params):
    logger.info("Load training set data")
    inputs_train, labels_train = read_ner("ner_data/%s/train.txt" % params.tgt_dm, params.tgt_dm)
    if params.n_samples != -1:
        logger.info("Few-shot on %d samples" % params.n_samples)
        inputs_train = inputs_train[:params.n_samples]
        labels_train = labels_train[:params.n_samples]
    logger.info("Load development set data")
    inputs_dev, labels_dev = read_ner("ner_data/%s/dev.txt" % params.tgt_dm, params.tgt_dm)
    logger.info("Load test set data")
    inputs_test, labels_test = read_ner("ner_data/%s/test.txt" % params.tgt_dm, params.tgt_dm)

    logger.info("label distribution for training set")
    label_distri_train = {}
    count_tok_train = 0
    for label_seq in labels_train:
        for label in label_seq:
            if label != pad_token_label_id:
                label_name = domain2labels[params.tgt_dm][label]
                if "B" in label_name:
                    count_tok_train += 1
                    label_name = label_name.split("-")[1]
                    if label_name not in label_distri_train:
                        label_distri_train[label_name] = 1
                    else:
                        label_distri_train[label_name] += 1
    print(label_distri_train)
    for key in label_distri_train:
        label_distri_train[key] /= count_tok_train
    logger.info(label_distri_train)

    logger.info("label distribution for dev set")
    label_distri_dev = {}
    count_tok_test = 0
    for label_seq in labels_dev:
        for label in label_seq:
            if label != pad_token_label_id:
                label_name = domain2labels[params.tgt_dm][label]
                if "B" in label_name:
                    count_tok_test += 1
                    label_name = label_name.split("-")[1]
                    if label_name not in label_distri_dev:
                        label_distri_dev[label_name] = 1
                    else:
                        label_distri_dev[label_name] += 1
    print(label_distri_dev)
    for key in label_distri_dev:
        label_distri_dev[key] /= count_tok_test
    logger.info(label_distri_dev)

    logger.info("label distribution for test set")
    label_distri_test = {}
    count_tok_test = 0
    for label_seq in labels_test:
        for label in label_seq:
            if label != pad_token_label_id:
                label_name = domain2labels[params.tgt_dm][label]
                if "B" in label_name:
                    count_tok_test += 1
                    label_name = label_name.split("-")[1]
                    if label_name not in label_distri_test:
                        label_distri_test[label_name] = 1
                    else:
                        label_distri_test[label_name] += 1
    print(label_distri_test)
    for key in label_distri_test:
        label_distri_test[key] /= count_tok_test
    logger.info(label_distri_test)

    if params.conll and params.joint:
        conll_inputs_train, conll_labels_train = read_ner("ner_data/conll2003/train.txt", params.tgt_dm)
        inputs_train = inputs_train * 50    # augment the target domain data to balance the source and target domain data
        labels_train = labels_train * 50
        inputs_train = inputs_train + conll_inputs_train
        labels_train = labels_train + conll_labels_train

    logger.info("train size: %d; dev size %d; test size: %d;" % (len(inputs_train), len(inputs_dev), len(inputs_test)))

    dataset_train = Dataset(inputs_train, labels_train)
    dataset_dev = Dataset(inputs_dev, labels_dev)
    dataset_test = Dataset(inputs_test, labels_test)
    
    dataloader_train = DataLoader(dataset=dataset_train, batch_size=params.batch_size, shuffle=True, collate_fn=collate_fn)
    dataloader_dev = DataLoader(dataset=dataset_dev, batch_size=params.batch_size, shuffle=False, collate_fn=collate_fn)
    dataloader_test = DataLoader(dataset=dataset_test, batch_size=params.batch_size, shuffle=False, collate_fn=collate_fn)

    return dataloader_train, dataloader_dev, dataloader_test


def get_conll2003_dataloader(batch_size, tgt_dm):
    inputs_train, labels_train = read_ner("ner_data/conll2003/train.txt", tgt_dm)
    inputs_dev, labels_dev = read_ner("ner_data/conll2003/dev.txt", tgt_dm)
    inputs_test, labels_test = read_ner("ner_data/conll2003/test.txt", tgt_dm)

    logger.info("conll2003 dataset: train size: %d; dev size %d; test size: %d" % (len(inputs_train), len(inputs_dev), len(inputs_test)))

    dataset_train = Dataset(inputs_train, labels_train)
    dataset_dev = Dataset(inputs_dev, labels_dev)
    dataset_test = Dataset(inputs_test, labels_test)
    
    dataloader_train = DataLoader(dataset=dataset_train, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)
    dataloader_dev = DataLoader(dataset=dataset_dev, batch_size=batch_size, shuffle=False, collate_fn=collate_fn)
    dataloader_test = DataLoader(dataset=dataset_test, batch_size=batch_size, shuffle=False, collate_fn=collate_fn)

    return dataloader_train, dataloader_dev, dataloader_test


if __name__ == "__main__":
    read_ner("../ner_data/final_politics/politics.txt", "politics")
