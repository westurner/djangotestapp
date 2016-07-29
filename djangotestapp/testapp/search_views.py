
from haystack.generic_views import SearchView


class TestSearchView(SearchView):
    pass
    # def get_context_data(self, *args, **kwargs):
    #     context = super(TestSearchView, self).get_context_data(*args, **kwargs)
    #     print(('context', context))
    #     print(('context.keys()', context.keys()))
    #     print('context.page_obj', context['page_obj'])
    #     print('context.page_obj', context['page_obj'].__dict__)
    #     return context

    # def get_queryset(self):
    #     queryset = super(TestSearchView, self).get_queryset()
    #     print(('queryset', queryset))
    #     # print(('queryset.all()', list(queryset.all())))
    #     # import pprint
    #     # for x in queryset.all():
    #     #     print(pprint.pformat(x.__dict__))
    #     return queryset

    # def get_results(self):
    #     results = super(TestSearchView, self).get_results()
    #     print(('get_results', results))
    #     return results

    # def dispatch(self, *args, **kwargs):
    #     response = super(TestSearchView, self).dispatch(*args, **kwargs)
    #     print(('dispatch', response))
    #     return response
