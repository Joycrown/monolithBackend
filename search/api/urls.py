from django.urls import path
from .views import GetBusinessNews, FeaturedBlocks, RecommendedUsers, FeaturedUsers, SearchLatest, GetCategoryNews, GetStockNews, GetCryptoNews, GetStockQuoteData, GetCompanySecondProfile, GetCryptoProfileBySymbol, GetCompanyFinancials, GetCompanyProfile, SearchStocks, GetStocksByThemes, GetCryptoPriceData, GetStockPriceData, SearchUsers, SearchBlocks, SearchPosts, BlockCategory, ListAllPosts

urlpatterns = [
    #SPOTLIGHT
    #path('spotlight-users', SearchTopUsers.as_view(), name='spotlight-users'),
    #LATEST
    path('latest', SearchLatest.as_view(), name='latest'),
    #PEOPLE
    path('users', SearchUsers.as_view(), name='users'),
    path('featured-users', FeaturedUsers.as_view(), name='featured-users'),
    path('recommended-users', RecommendedUsers.as_view(), name='recommended-users'),
    #BLOCKS
    path('featured-blocks', FeaturedBlocks.as_view(), name='featured-blocks'),
    path('block-category', BlockCategory.as_view(), name='block-category'),    
    path('blocks', SearchBlocks.as_view(), name='blocks'),
    #POSTS
    path('posts/all', ListAllPosts.as_view(), name='townsquare'),
    path('posts', SearchPosts.as_view(), name='posts'),
    #CRYPTO
    path('get-crypto-profile-by-symbol', GetCryptoProfileBySymbol.as_view(), name='get-crypto-profile-by-symbol'),
    path('get-crypto-price-data', GetCryptoPriceData.as_view(), name='get-crypto-price-data'),
    #STOCKS
    path('get-company-financials', GetCompanyFinancials.as_view(), name='get-company-financials'),
    path('get-company-profile', GetCompanyProfile.as_view(), name='get-company-profile'),
    path('get-company-second-profile', GetCompanySecondProfile.as_view(), name='get-company-second-profile'),
    path('search-stocks/<str:text>', SearchStocks.as_view(), name='search-stocks'),
    path('get-stocks-by-theme', GetStocksByThemes.as_view(), name='get-stocks-by-theme'),
    path('get-stock-quote-data', GetStockQuoteData.as_view(), name='get-stock-quote-data'),
    path('get-stock-price-data', GetStockPriceData.as_view(), name='get-stock-price-data'),
    #NEWS
    path('get-crypto-news', GetCryptoNews.as_view(), name='get-crypto-news'),
    path('get-stock-news', GetStockNews.as_view(), name='get-stock-news'),
    path('get-business-news', GetBusinessNews.as_view(), name='get-business-news'),
    path('get-category-news/<str:category>/', GetCategoryNews.as_view(), name='get-category-news'),
]
