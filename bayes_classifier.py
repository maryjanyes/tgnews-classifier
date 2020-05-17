# create Bayes classifier
# apply factors of category for each item in data-set
class NaiveBayesClassifier:

    def __init__(self, classifier_options):

        self.c_categories = classifier_options.get('categories')
        self.c_data = classifier_options.get('data')
        self.output = self.apply()
        self.items_belongs_to_other_category = []

    # apply even data item to category
    def apply_data_to_category_factors(self, category):

        data_matches = []
        category_name = category.get('category_name')

        for data in self.c_data:

            item_name = data.get('name')
            item_content = data.get('file').read()

            category_match_to_item = dict(
                score=0,
                item_name=item_name,
                category_name=category_name
            )

            # apply each category factor to data item context
            for c_factor in category.get('apply_factors'):

                factor_text = c_factor.get('text')
                factor_text_ru = c_factor.get('ru')
                factor_text_en = c_factor.get('en')
                factor_relevance = c_factor.get('priority')

                if factor_text_en in item_content or factor_text_ru in item_content:
                    category_match_to_item['score'] = category_match_to_item.get('score') + factor_relevance
                else:
                    self.classify_item_to_other_category(item_name)

            print('score', category_match_to_item.get('score'))
            if category_match_to_item.get('score') >= 3:
                data_matches.append(item_name)

            return data_matches

    # do each on data items and return classify True for each factor if score >=3 (minimal match score)
    def apply(self):

        category_matches = []

        for category in self.c_categories:
            items_by_category = self.apply_data_to_category_factors(category)
            category_matches.append(dict(
                category=category.get('category_name'),
                articles=items_by_category
            ))

        return category_matches

    def classify_item_to_other_category(self, item_name):

        if not item_name in self.items_belongs_to_other_category:
            self.items_belongs_to_other_category.append(item_name)
