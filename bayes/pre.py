import nltk
import os
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
path_default = './email/spam'
default_encoding = 'utf-8'


def read_from_file(file_path_rff):
    with open(file_path_rff, 'r', encoding=default_encoding) as f_rff:
        temp_rff = f_rff.read()
    return temp_rff


def each_file(file_path_ef):
    child_ef = []
    path_dir = os.listdir(file_path_ef)
    for allDir_ef in path_dir:
        child_temp = os.path.join('%s%s%s' % (file_path_ef, '/', allDir_ef))
        child_ef.append(child_temp)
    return child_ef


def save_to_file(file_name_stf, contents_stf):
    contents_stf = contents_stf.encode(default_encoding)
    fh_stf = open(file_name_stf, 'wb+')
    fh_stf.write(contents_stf)
    fh_stf.close()


def adjoin(c_adjoin, save_name_ad):
    temp_adjoin_list = []
    num_adjoin = len(c_adjoin)
    for i_adjoin in range(0, num_adjoin):
        j_adjoin = read_from_file(c_adjoin[i_adjoin])
        j_adjoin_2 = ''.join(j_adjoin.replace('\r\n', ' ').replace('\t', ' ').replace('\n', ' '))
        temp_adjoin_list.append(j_adjoin_2)
    temp_adjoin_str = ' '.join(temp_adjoin_list)
    # save_to_file('step1_adjoin.txt', temp_adjoin_str)
    save_to_file('step1_adjoin_'+save_name_ad, temp_adjoin_str)


def step_1_adjoin(path_step_1, s1_name_s1):
    path_2_step_1 = each_file(path_step_1)
    adjoin(path_2_step_1, s1_name_s1)


def eme_tokenize(str_ori_tokenize):
    str_tra_tokenize = nltk.word_tokenize(str_ori_tokenize)
    return str_tra_tokenize


def step_2_clean(file_name_s2_clean, save_name_s2_clean):
    # punctuations_cleaner = """,.<>()*&^#@!'";~`[]{}|、\\/~+_-=?:"""
    punctuations_cleaner = """,.<>()*&^#@!'";~`[]{}|、\\/~+_-=?:0123456789"""
    str_ori_cleaner = read_from_file(file_name_s2_clean)
    str_adj_cleaner = ''.join(str_ori_cleaner.replace('\r\n', ' ').replace('\t', ' ').replace('\n', ' '))
    clean_word_cleaner = []
    for punctuation_cleaner in punctuations_cleaner:
        str_adj_cleaner = (' '.join(str_adj_cleaner.split(punctuation_cleaner))).replace('  ', ' ')
        # clean_word_cleaner = [word.lower() for word in str_adj_cleaner.split(' ') if len(word) > 2]
        clean_word_cleaner = [word.lower() for word in str_adj_cleaner.split(' ')]
    temp_str_cleaner = ' '.join(clean_word_cleaner)
    if save_name_s2_clean == '1':
        return temp_str_cleaner
    else:
        save_to_file(save_name_s2_clean, temp_str_cleaner)


def step_3_snowball(snowball_s3_sb):
    snowball_s3_fun = SnowballStemmer('english')
    snowball_s3_result = snowball_s3_fun.stem(snowball_s3_sb)
    return snowball_s3_result


def step_3_stem(file_name_s3_stem, save_name_s3_stem):
    if save_name_s3_stem != '1':
        str_ori_stem = read_from_file(file_name_s3_stem)
    else:
        str_ori_stem = file_name_s3_stem
    str_token_stem = eme_tokenize(str_ori_stem)
    temp_str_stem = map(step_3_snowball, str_token_stem)
    temp_final_stem = ' '.join(temp_str_stem)
    if save_name_s3_stem == '1':
        return temp_final_stem
    else:
        # save_to_file('step3_stemming.txt', temp_final_stem)
        save_to_file(save_name_s3_stem, temp_final_stem)


def step_4_stopwords(word_list_s4):
    filtered_words_s4_ = [word for word in word_list_s4 if word not in stopwords.words('english')]
    return filtered_words_s4_


def step_4_sw(to_be_sw_s4, al_swed_s4):
    # str_ori_s4 = read_from_file('step3_stemming.txt')
    str_ori_s4 = read_from_file(to_be_sw_s4)
    str_tra_s4 = step_4_stopwords(eme_tokenize(str_ori_s4))
    # save_to_file('step4_stopwords.txt', ' '.join(str_tra_s4))
    save_to_file(al_swed_s4, ' '.join(str_tra_s4))


def add_to_dic(new_text_atd, dictionary_word_atd, dictionary_numb_atd):
    to_be_added_atd = step_2_clean(new_text_atd, '1')
    # print(to_be_added_atd)
    stemmed_list_atd = step_3_stem(to_be_added_atd, '1').split(' ')
    # print(stemmed_list_atd)
    # dic_atd = eme_tokenize(read_from_file('dictionary.txt'))
    if dictionary_numb_atd != '1' and dictionary_word_atd != '1':
        dic_atd = eme_tokenize(read_from_file(dictionary_word_atd))
        din_atd = eme_tokenize(read_from_file(dictionary_numb_atd))
    dictionary_atd = {}
    l_atd = 0
    for j_atd in dic_atd:
        dictionary_atd[j_atd] = int(din_atd[l_atd])
        l_atd += 1
    # print(dic_atd)
    # print(stemmed_list_atd.__len__())
    # for i_atd in range[0, len(stemmed_list_atd) - 1]:
    for i_atd in stemmed_list_atd:
        # print(i_atd)
        # if i_atd not in dic_atd and i_atd.strip() != '' and i_atd != None:
        if i_atd not in stopwords.words('english') and i_atd.strip() != '':
            if i_atd not in dic_atd:
                dic_atd.append(i_atd)
                din_atd.append(1)
                dictionary_atd.setdefault(i_atd, 1)
            else:
                dictionary_atd[i_atd] += 1
    # print(dictionary_atd)
    # print(dic_atd)
    n_atd = 0
    if dictionary_numb_atd != '1' and dictionary_word_atd != '1':
        for m_atd in dictionary_atd:
            dic_atd[n_atd] = m_atd
            din_atd[n_atd] = dictionary_atd[m_atd]
            n_atd += 1
        save_to_file(dictionary_word_atd, ' '.join(dic_atd))
        num_atd = []
        for p_atd in din_atd:
            num_atd.append(str(p_atd))
        save_to_file(dictionary_numb_atd, ' '.join(num_atd))
    else:
        return dictionary_atd


def word_stat(test_dic_stat, spam_dic_stat, norm_dic_stat, norm_num_stat, spam_num_stat):
    word_prob_dic = {}
    for words_stat, nums_stat in test_dic_stat.items():
        if words_stat in spam_dic_stat.keys() and words_stat in norm_dic_stat.keys():
            p_w_s_stat = spam_dic_stat[words_stat] / spam_num_stat
            p_w_n_stat = norm_dic_stat[words_stat] / norm_num_stat
            p_s_w_stat = p_w_s_stat / (p_w_s_stat + p_w_n_stat)
            word_prob_dic.setdefault(words_stat, p_s_w_stat)
        if words_stat in spam_dic_stat.keys() and words_stat not in norm_dic_stat.keys():
            p_w_s_stat = spam_dic_stat[words_stat] / spam_num_stat
            p_w_n_stat = 0.01
            p_s_w_stat = p_w_s_stat / (p_w_s_stat + p_w_n_stat)
            word_prob_dic.setdefault(words_stat, p_s_w_stat)
        if words_stat not in spam_dic_stat.keys() and words_stat in norm_dic_stat.keys():
            p_w_s_stat = 0.01
            p_w_n_stat = norm_dic_stat[words_stat] / norm_num_stat
            p_s_w_stat = p_w_s_stat / (p_w_s_stat + p_w_n_stat)
            word_prob_dic.setdefault(words_stat, p_s_w_stat)
        if words_stat not in spam_dic_stat.keys() and words_stat not in norm_dic_stat.keys():
            word_prob_dic.setdefault(words_stat, 0.4)
    # print(word_prob_dic)
    # sorted(word_prob_dic.items(), key=lambda d: d[1], reverse=True)[0:15]
    # print(word_prob_dic)
    return word_prob_dic


def bayes_cal(test_dic_bc):
    p_s_w_bc = 1
    p_s_n_bc = 1
    for word_bc, prob_bc in test_dic_bc.items():
        # print(word_bc + "/" + str(prob_bc))
        p_s_w_bc *= prob_bc
        p_s_n_bc *= (1 - prob_bc)
    p_final_bc = p_s_w_bc / (p_s_w_bc + p_s_n_bc)
    return p_final_bc


def preprocessing(path_pre, name_pre):
    save_to_file('dictionary_numb_'+name_pre, '')
    save_to_file('dictionary_word_'+name_pre, '')
    step_1_adjoin(path_pre, name_pre)
    step_2_clean(('step1_adjoin_'+name_pre), ('step2_cleaner_'+name_pre))
    step_3_stem(('step2_cleaner_'+name_pre), ('step3_stemming_'+name_pre))
    step_4_sw(('step3_stemming_'+name_pre), ('step4_stopwords_'+name_pre))
    add_to_dic('step4_stopwords_'+name_pre, 'dictionary_word_'+name_pre, 'dictionary_numb_'+name_pre)
    # step_2_clean('step1_adjoin.txt', 'step2_cleaner.txt')
    # step_3_stem('step2_cleaner.txt', 'step3_stemming.txt')
    # add_to_dic('step4_stopwords', 'dictionary_word', 'dictionary_numb')


def read_dic(dic_name_rd):
    dic_rd = eme_tokenize(read_from_file('dictionary_word_'+dic_name_rd))
    din_rd = eme_tokenize(read_from_file('dictionary_numb_'+dic_name_rd))
    dictionary_rd = {}
    t_rd = 0
    for i_rd in dic_rd:
        dictionary_rd[i_rd] = int(din_rd[t_rd])
        t_rd += 1
    return dictionary_rd


def get_file_list(file_path_gfl):
    file_name_gfl = os.listdir(file_path_gfl)
    return file_name_gfl


def cal_main():
    preprocessing('./email/spam', 'spam')
    preprocessing('./email/ham', 'norm')
    # spam_main_dic = {}
    # norm_main_dic = {}
    # test_main_dic
    spam_main_dic = read_dic('spam')
    norm_main_dic = read_dic('norm')
    preprocessing('./test', 'test')
    test_main_dic = read_dic('test')
    test_re_main = word_stat(test_main_dic, spam_main_dic, norm_main_dic, len(get_file_list('./email/spam')),
                             len(get_file_list('./email/ham')))
    if bayes_cal(test_re_main) > 0.9:
        print("超级瞄准已部署，垃圾邮件成功拦截")
    else:
        print("老铁没毛病")
    '''
    j_cm = 1
    for i_cm in  range[0, 1]:        
        preprocessing('./test', 'test'+str(j_cm))
        test_main_dic = read_dic('test')
        test_re_main = word_stat(test_main_dic, spam_main_dic, norm_main_dic, len(get_file_list('./email/spam')), len(get_file_list('./email/ham')))
        if bayes_cal(test_re_main) > 0.9:
            print("超级瞄准已部署，垃圾邮件成功拦截")
        else:
            print("老铁没毛病")
    '''


if __name__ == '__main__':
    cal_main()






"""
根目录
./20_newsgroups
./email
"""
"""
20_newsgroups
./20_newsgroups/alt.atheism
./20_newsgroups/comp.graphics
./20_newsgroups/comp.os.ms-windows.misc
./20_newsgroups/comp.sys.ibm.pc.hardware
./20_newsgroups/comp.sys.mac.hardware
./20_newsgroups/comp.windows.x
./20_newsgroups/misc.forsale
./20_newsgroups/rec.autos
./20_newsgroups/rec.motorcycles
./20_newsgroups/rec.sport.baseball
./20_newsgroups/rec.sport.hockey
./20_newsgroups/sci.crypt
./20_newsgroups/sci.electronics
./20_newsgroups/sci.med
./20_newsgroups/sci.space
./20_newsgroups/soc.religion.christian
./20_newsgroups/talk.politics.guns
./20_newsgroups/talk.politics.mideast
./20_newsgroups/talk.politics.misc
./20_newsgroups/talk.religion.misc
"""
"""
email
./email/ham
./email/spam
"""
