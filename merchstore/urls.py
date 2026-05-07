from django.urls import include, path
from .views import ProductListView, ProductDetailView, CartListView, ProductCreateView, ProductUpdateView, TransactionListView

app_name = 'merchstore'

urlpatterns = [
    path('items', ProductListView.as_view(), name='product-list'),
    path('item/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('cart', CartListView.as_view(), name='cart'),
    path('transactions', TransactionListView.as_view(), name='transactions'),
    path('item/add', ProductCreateView.as_view(), name='add'),
    path('item/<int:pk>/update', ProductUpdateView.as_view(), name='update'),
]
