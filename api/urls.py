from .views import NoodlesView, CategoriesList, IngredientsList, TagsList, BrandsList, SingleCategory, Singlebrand, SingleTag, SingleIngredient
from django.urls import path


urlpatterns = [
    path('noodles/', NoodlesView.as_view(), name='noodles'),
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
]

handler404 = "api.views.page_not_found_view"
