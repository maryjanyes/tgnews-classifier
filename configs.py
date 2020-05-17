from nltk.corpus import stopwords


# create configs for use by classifier
class ClassifierConfigs:

    def __init__(self):

         Society = dict(category_name='society', apply_factors=[
              dict(priority=1, text=self.form_international_factor('социаль', 'social')),
              dict(priority=1, text=self.form_international_factor('публичны', 'public')),
              dict(priority=3, text=self.form_international_factor('публичное событие', 'public event')),
              dict(priority=3, text=self.form_international_factor('публичная новость', 'public news')),
              dict(priority=3, text=self.form_international_factor('социальный клуб', 'social club')),
              dict(priority=3, text=self.form_international_factor('полити', 'political')),
              dict(priority=3, text=self.form_international_factor('ситуация в стране', 'country situation'))
         ])
         Economy = dict(category_name='economy', apply_factors=[
              dict(priority=1, text=self.form_international_factor('экономика', 'economy')),
              dict(priority=3, text=self.form_international_factor('экономическая ситуация', 'economy situation')),
              dict(priority=3, text=self.form_international_factor('доллар', 'dollar')),
              dict(priority=3, text=self.form_international_factor('валюта', 'currency')),
              dict(priority=3, text=self.form_international_factor('повышение курса', 'currency rate'))
         ])
         Technology = dict(category_name='technology', apply_factors=[
              dict(priority=1, text=self.form_international_factor('техника', 'tech')),
              dict(priority=2, text=self.form_international_factor('инновации', 'innovation')),
              dict(priority=3, text=self.form_international_factor('алгоритм', 'algorithm')),
              dict(priority=3, text=self.form_international_factor('IT-сфера', 'IT-company')),
              dict(priority=3, text=self.form_international_factor('технологический', 'technological')),
              dict(priority=3, text=self.form_international_factor('программи', 'programming'))
         ])
         Sport = dict(category_name='sport', apply_factors=[
              dict(priority=1, text=self.form_international_factor('спорт', 'sport')),
              dict(priority=4, text=self.form_international_factor('плав', 'swimming')),
              dict(priority=3, text=self.form_international_factor('плыть', 'swim')),
              dict(priority=4, text=self.form_international_factor('футбол', 'football')),
              dict(priority=4, text=self.form_international_factor('бокс', 'boxing')),
              dict(priority=3, text=self.form_international_factor('спортивное соревновани', 'sports competition')),
              dict(priority=3, text=self.form_international_factor('медал', 'medals')),
              dict(priority=3, text=self.form_international_factor('победител', 'winners')),
         ])
         Science = dict(category_name='science', apply_factors=[
              dict(priority=1, text=self.form_international_factor('наука', 'science')),
              dict(priority=4, text=self.form_international_factor('открытие', 'discovery')),
              dict(priority=3, text=self.form_international_factor('расскопки', 'excavations')),
              dict(priority=3, text=self.form_international_factor('археология', 'archaeological')),
              dict(priority=3, text=self.form_international_factor('изобретени', 'invention')),
              dict(priority=4, text=self.form_international_factor('ученый', 'scientist')),
         ])
         Entertaiment = dict(category_name='entertainment', apply_factors=[
              dict(priority=1, text=self.form_international_factor('игры', 'games')),
              dict(priority=3, text=self.form_international_factor('игровая индустрия', 'game industry')),
              dict(priority=3, text=self.form_international_factor('груповые развлечения', 'group entertainment')),
              dict(priority=3, text=self.form_international_factor('аттракцион', 'rides')),
              dict(priority=3, text=self.form_international_factor('музыкальн', 'music')),
              dict(priority=3, text=self.form_international_factor('фестиваль', 'fest')),
         ])
         Other=dict(category_name='other', apply_factors=[])

         self.article_classify_categories = [Society, Economy, Technology, Sport, Science, Entertaiment, Other]

         En = dict(lang_name='En', stop_words=stopwords.words('english'))
         Ru = dict(lang_name='Ru', stop_words=stopwords.words('russian'))

         self.article_languages = dict(en=En, ru=Ru)

         self.source_dir = './source_dir'

         self.source_options = dict(classify_by=[
              'news',
              'languages',
              'categories',
              'theads',
              'thread_relevance'
         ])

    def form_international_factor(self, ru_text, en_text):
         return dict(
              ru=ru_text,
              en=en_text
         )