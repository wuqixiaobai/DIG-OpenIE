
import os
import re
from digoie.conf.storage import __elastic_search_dir__, __reverb_input_dir__, REVERB_INPUT_EXT



def extract(raw):
    print 'extract features...'
    featured = []
    for line in raw:
        line = line[:-1]
        line = line.split('\t')

        rvd_post = str(line[13]).split(' ')
        rvd_ct = str(line[14]).split(' ')
        
        rvd_arg1_val = str(line[15]).replace('.', '')
        rvd_arg1_start_idx = int(line[5])
        rvd_arg1_end_idx = int(line[6])

        rvd_rel_val  = str(line[16]).replace('.', '')
        rvd_rel_start_idx = int(line[7])
        rvd_rel_end_idx = int(line[8])

        rvd_arg2_val = str(line[17]).replace('.', '')
        rvd_arg2_start_idx = int(line[9])
        rvd_arg2_end_idx = int(line[10])

        # load post and chunk tags
        rvd_arg1_post_tags = rvd_post[rvd_arg1_start_idx:rvd_arg1_end_idx]
        rvd_arg1_ct_tags = rvd_ct[rvd_arg1_start_idx:rvd_arg1_end_idx]

        rvd_rel_post_tags = rvd_post[rvd_rel_start_idx:rvd_rel_end_idx]
        rvd_rel_ct_tags = rvd_ct[rvd_rel_start_idx:rvd_rel_end_idx]

        rvd_arg2_post_tags = rvd_post[rvd_arg2_start_idx:rvd_arg2_end_idx]
        rvd_arg2_ct_tags = rvd_ct[rvd_arg2_start_idx:rvd_arg2_end_idx]

        # format chunk tags
        rvd_arg1_ct_tags = [tag.replace('-','2') for tag in rvd_arg1_ct_tags]
        rvd_rel_ct_tags = [tag.replace('-','2') for tag in rvd_rel_ct_tags]
        rvd_arg2_ct_tags = [tag.replace('-','2') for tag in rvd_arg2_ct_tags]


        # add prefix for tags
        prefix = 'S4'
        rvd_arg1_post_tags = [prefix + elt for elt in rvd_arg1_post_tags]
        rvd_arg1_ct_tags = [prefix + elt for elt in rvd_arg1_ct_tags]

        prefix = 'P4'
        rvd_rel_post_tags = [prefix + elt for elt in rvd_rel_post_tags]
        rvd_rel_ct_tags = [prefix + elt for elt in rvd_rel_ct_tags]

        prefix = 'O4'
        rvd_arg2_post_tags = [prefix + elt for elt in rvd_arg2_post_tags]
        rvd_arg2_ct_tags = [prefix + elt for elt in rvd_arg2_ct_tags]


        # transfer list into string
        rvd_arg1_post_tags = ' '.join(rvd_arg1_post_tags)
        rvd_arg1_ct_tags = ' '.join(rvd_arg1_ct_tags)

        rvd_rel_post_tags = ' '.join(rvd_rel_post_tags)
        rvd_rel_ct_tags = ' '.join(rvd_rel_ct_tags)

        rvd_arg2_post_tags = ' '.join(rvd_arg2_post_tags)
        rvd_arg2_ct_tags = ' '.join(rvd_arg2_ct_tags)

        # remove names from feature
        # rvd_arg1_val = remove_names(rvd_arg1_val)
        # rvd_rel_val = remove_names(rvd_rel_val)
        # rvd_arg2_val = remove_names(rvd_arg2_val)

        # filter features
        filter = FeatureFilter()
        rvd_arg1_val = filter.filtering(rvd_arg1_val)
        rvd_rel_val = filter.filtering(rvd_rel_val)
        rvd_arg2_val = filter.filtering(rvd_arg2_val)
        

        var_list = [
                        rvd_arg1_val, 
                        rvd_arg1_post_tags, 
                        rvd_arg1_ct_tags,
                        rvd_rel_val, 
                        rvd_rel_post_tags, 
                        rvd_rel_ct_tags,
                        rvd_arg2_val, 
                        rvd_arg2_post_tags, 
                        rvd_arg2_ct_tags
                    ]

        rv4fe_data = ' '.join(var_list)
        featured.append(rv4fe_data)
    return featured


class FeatureFilter():
    def __init__(self):
        self.names = None

    def filtering(self, sentence):
        result = []
        self.names = self.load_name()
        word_list = sentence.split(' ')
        for word in word_list:
            word = self.refine_word(word)
            if self.is_valid_word(word):
                result.append(word)
        return ' '.join(result)


    def refine_word(self, word):
        word = word.lower()
        return word

    def is_valid_word(self, word):
        result = True
        if self.is_contain_name(word):
            result = False
        if len(word) < 2:
            result = False

        reg = re.compile("^[a_zA-Z]*$")
        if re.match(reg, word):
            result = False
        return result


    def is_contain_name(self, word):
        if word in self.names:
            return True
        else:
            return False

    def load_name(self):
        path = os.path.join(__elastic_search_dir__, 'names')
        names_file = open(path, 'rU')
        names = list([name[:-1] for name in names_file])
        names_file.close()
        return names






"""
def remove_names(vals):
    result = []
    # load name
    path = os.path.join(__elastic_search_dir__, 'names')
    names_file = open(path, 'rU')
    names = list([name[:-1] for name in names_file])
    names_file.close()

    val_list = vals.split(' ')
    for val in val_list:
        if val.lower() not in names:
            result.append(val.lower())
    return ' '.join(result)
"""








