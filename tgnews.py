import os
import re
import sys
import json
import time
import math

import configs
import bayes_classifier


# create Classifier
class TgNewsClassifier:

    def __init__(self):

        # assign classifier_configs variable that represent start configs
        # for classifier work-options
        self.classifier_configs = configs.ClassifierConfigs()
        self.classify_folder = 0
        classify_by = self.classifier_configs.source_options.get('classify_by')
        classify_option = None

        if sys.argv and len(sys.argv) > 1:
            classify_factor = str(sys.argv[1])
            source_dir = str(sys.argv[2])
            source_dir_child = str(sys.argv[3])

            if source_dir:
                self.source_dir = source_dir

            if source_dir_child:
                self.classify_folder = source_dir_child

            if classify_factor:
                self.classify_option = classify_factor
            else:
                self.classify_option = 'news'


    def fetch_data_source(self):

        # get train directories content
        # that contain article files in .html format
        s_dir_path1 = self.source_dir or self.classifier_configs.source_dir
        s_dirs = os.listdir(s_dir_path1)
        s_dir_files = []
        file_mess = []
        s_dir_len = len(s_dirs)
        s_dir_files_count = 0
        print(s_dir_len)

        if s_dir_len > 0:
            for i1 in range(s_dir_len):
                s_dir = s_dirs[i1]

                if i1 == self.classify_folder:
                    s_dir_path = s_dir_path1 + '/' + s_dir
                    s_dirs_child = os.listdir(s_dir_path)

                    for child_dir_path in s_dirs_child:

                        s_dir_files_as_directory = os.listdir(s_dir_path + '/' + child_dir_path)
                        s_dir_files_as_directory_len = len(s_dir_files_as_directory)

                        if s_dir_files_as_directory_len > 3000:
                            mid_count = math.ceil(s_dir_files_as_directory_len / 2)
                            s_dir_files_as_directory = s_dir_files_as_directory[0:mid_count]
                            s_dir_files_left = s_dir_files_as_directory[mid_count:s_dir_files_as_directory_len-1]
                            file_mess = [file_mess, s_dir_files_left]

                        for i_file in s_dir_files_as_directory:
                            s_dir_files_count = s_dir_files_count + 1
                            file_path = s_dir_path + '/' + child_dir_path + '/' + i_file
                            s_dir_files.append(dict(
                                file=open(file_path, 'r', encoding='utf-8'),
                                name=file_path
                            ))

                        self.map_classify_by_factor(s_dir_files, s_dir_files_count)
                        s_dir_files = []
                        s_dir_files_count = 0

                        time.sleep(30)


    # do classify depends from <factor>
    def map_classify_by_factor(self, files, files_count):

        print('classify files', files_count)
        if self.classify_option == 'languages':
            self.do_language_classify(files)
        if self.classify_option == 'is_news':
            self.do_only_articles_classify(files, files_count)
        if self.classify_option == 'categories':
            self.do_classify_by_categories(files)
        if self.classify_option == 'threads':
            self.do_classify_by_threads(files)
        if self.classify_option == 'thread_relevance':
            self.do_classify_by_threads(files, True)

    # classify data to an threads
    # using Neural network
    def do_classify_by_threads(self, files, with_relevance = False):
        print('with relevance', with_relevance)
        return dict()

    # apply relevance to classified threads
    # using probability of importance
    def apply_relevance(self, files):
        initial_importance = 0
        threads_output = self.do_classify_by_threads(files)
        return dict()

    # classify articles depends from <categories> factor
    # using Diffie Hellman classifier
    def do_classify_by_categories(self, files):

        def apply_diffie_hellman_classifier(data_options):
            classified = bayes_classifier.NaiveBayesClassifier(data_options)
            return classified.output

        if files:
            data_options = dict(
                data=files,
                categories=self.classifier_configs.article_classify_categories
            )
            classified_output = apply_diffie_hellman_classifier(data_options)

            # print classified output
            print(classified_output)

            classified_output = json.dumps(classified_output)
            classified_json_output = open('./output_dir/categories.json', 'a')
            classified_json_output.write(classified_output)
            classified_json_output.close()


    # classify articles depends from <languages> factor
    def do_language_classify(self, files):

        en_article_list = dict(
            lang_code='en',
            articles=[]
        )
        ru_article_list = dict(
            lang_code='ru',
            articles=[]
        )

        def complete_file_classify(
            file_name,
            is_en_matched,
            is_ru_matched
        ):
            if is_ru_matched:
                ru_article_list.get('articles').append(file_name)
            elif is_en_matched:
                en_article_list.get('articles').append(file_name)

        if files:
            for article in files:
                article_text = article.get('file').read()
                is_en = self.is_matched_to_language('en', article_text)
                is_ru = self.is_matched_to_language('ru', article_text)

                complete_file_classify(article.get('name'), is_en, is_ru)

        output_json = json.dumps([en_article_list, ru_article_list])

        # print classified output
        print(output_json)

        sorted_by_language_json_output = open('./output_dir/languages_articles.json', 'a')
        sorted_by_language_json_output.write(output_json)
        sorted_by_language_json_output.close()

    # classify articles depends from <is_article> factor
    def do_only_articles_classify(self, files, general_files_count):

        articles_collection = dict(
            articles=[]
        )

        if files:
            for article in files:
                is_article = self.is_text_article(article.get('file').read())
                if is_article:
                    articles_collection.get('articles').append(article.get('name'))

        output_json = json.dumps(articles_collection)

        # print classified output
        print(output_json)

        left_count = general_files_count - len(articles_collection.get('articles'))
        articles_collection['left_count'] = left_count
        sorted_only_articles_output = open('./output_dir/only_articles.json', 'a')
        sorted_only_articles_output.write(output_json)
        sorted_only_articles_output.close()

    # check if file content is represent an article
    def is_text_article(self, text_content):

        head_pattern = '<meta property="og:url"(.+?)/>'
        text_head = re.search(head_pattern, text_content)
        is_news_in_text_content = 'news' in text_content
        is_news_content_len_more_then_200 = len(text_content) > 1000

        if text_head:
            text_head = text_head.group(1)
            is_news_in_head = 'news' in text_head
            if is_news_in_head: return True
            else:
                return is_news_in_text_content or is_news_content_len_more_then_200
        else:
            return is_news_in_text_content or is_news_content_len_more_then_200

    # check if article match specified language
    def is_matched_to_language(self, language_code, text):
        matched_words = []
        language_stop_words = self.classifier_configs.article_languages[language_code]
        stop_words = language_stop_words.get('stop_words')

        for i in range(len(stop_words)):
            stop_word = stop_words[i]
            stop_word_pattern = re.compile(stop_word)
            if (stop_word_pattern.match(text, 0, len(text))):
                matched_words.append(stop_word)
            elif stop_word in text:
                matched_words.append(stop_word)

        return len(matched_words) > 2


classifier = TgNewsClassifier()
classifier.fetch_data_source()
