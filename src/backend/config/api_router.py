from rest_framework.routers import SimpleRouter

from django.urls import include
from django.urls import path

from apps.ingredients.api.views import IngredientViewSet
from apps.tags.api.views import TagViewSet
from apps.users.api.views import UserViewSet
from apps.recipes.api.views import RecipeViewSet

app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
