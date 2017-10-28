import datetime
from haystack import indexes
from Earth.models import Article


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # author = indexes.CharField(model_attr='author,')
    # pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(published_date__lte=datetime.datetime.now())