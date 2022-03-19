from django.urls import path
from .views import NoodlesView, CategoriesList, IngredientsList, TagsList, BrandsList, SingleCategory, Singlebrand, SingleTag, SingleIngredient, Home, NoodleView, SearchNoodle


urlpatterns = [
    path('', Home.as_view(), name='home'),
    # noodles  list
    path('noodles/', NoodlesView.as_view(), name='noodles'),
    # single noodle
    path('noodles/<str:slug>', NoodleView.as_view(), name='noodle'),
    # list
    path('categories/list', CategoriesList.as_view(), name='gategories'),
    path('ingredients/list', IngredientsList.as_view(), name='ingredients'),
    path('brand/list', BrandsList.as_view(), name='brands-list'),
    path('tags/list', TagsList.as_view(), name='tags-list'),
    # single details
    path('categories/<str:slug>', SingleCategory.as_view(), name='single-category'),
    path('brand/<str:slug>', Singlebrand.as_view(), name='single-brand'),
    path('tags/<str:slug>', SingleTag.as_view(), name='single-tag'),
    path('ingredients/<str:slug>', SingleIngredient.as_view(),
         name='single-ingredient'),
    #  serch
    path('search/', SearchNoodle.as_view(),
         name='search'),
]

handler404 = "api.views.page_not_found_view"
