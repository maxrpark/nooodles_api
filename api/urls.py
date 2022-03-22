from django.urls import path
from .views import NoodlesView, CategoriesList, IngredientsList, TagsList, BrandsList, SingleCategory, Singlebrand, SingleTag, SingleIngredient, Home, NoodleView, SearchNoodle


urlpatterns = [
    path('', Home.as_view(), name='home'),
    # All Noodles
    path('noodles/', NoodlesView.as_view(), name='noodles'),
    # Single noodle
    path('noodles/<str:slug>', NoodleView.as_view(), name='noodle'),
    # LIST RESULTS
    path('categories/list', CategoriesList.as_view(),
         name='gategories'),  # Categories
    path('ingredients/list', IngredientsList.as_view(),
         name='ingredients'),  # Ingredients
    path('brand/list', BrandsList.as_view(), name='brands-list'),  # Brands
    path('tags/list', TagsList.as_view(), name='tags-list'),  # Tags
    # SINGLE RESULTS
    path('categories/<str:slug>', SingleCategory.as_view(),
         name='single-category'),  # Category
    path('brand/<str:slug>', Singlebrand.as_view(), name='single-brand'),  # Brand
    path('ingredients/<str:slug>', SingleIngredient.as_view(),  # Ingredient
         name='single-ingredient'),
    path('tags/<str:slug>', SingleTag.as_view(), name='single-tag'),  # Tag
    #  SEARCH
    path('search/', SearchNoodle.as_view(),
         name='search'),
]

handler404 = "api.views.page_not_found_view"
