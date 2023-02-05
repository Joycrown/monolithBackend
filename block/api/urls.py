from django.urls import path
from .views import ListBlocksUserIsModerator, ListBlocksUserJoined, RetrievePost, user_voted_comment, user_voted_post, user_saved_comment, user_reported_comment, RuleDeleteView, LinkDeleteView, CreateRuleView, CreateLinkView, ListRulesOfBlock, ListLinksOfBlock, user_joined_block, user_reported_post, user_saved_post, BlockDeleteView, BlockUpdateView, BlockDetailView, ListSavedPostsOfUser, ListSavedCommentsOfUser, CreateBlockView, ListBlocksOfUser, Block, join_block, CreatePostView, VoteOnPost, RePostView, report_post, save_post, ListPostsOfUser, ListPostsOfBlock, DetailPostOfUser, DetailPostOfBlock, CreateCommentView, VoteOnComment, report_comment, save_comment, ListCommentsOfUser, DetailCommentsOfUser, ListPopularCommentsOfPost, ListOldCommentsOfPost, ListNewCommentsOfPost, DetailCommentsOfPost


urlpatterns = [
    # BLOCK VIEWS
    path('block/create/', CreateBlockView.as_view(), name='create_block'),    
    path('block/create/link/', CreateLinkView.as_view(), name='create_link'),
    path('block/create/rule/', CreateRuleView.as_view(), name='create_rule'),
    path('block/link/<int:id>/delete/', LinkDeleteView.as_view(), name='delete_link'),
    path('block/rule/<int:id>/delete/', RuleDeleteView.as_view(), name='delete_rule'),
    path('block/<str:name>/retrieve/', BlockDetailView.as_view(), name='retrieve_block'),
    path('block/<str:name>/update/', BlockUpdateView.as_view(), name='update_block'),
    path('block/<str:name>/delete/', BlockDeleteView.as_view(), name='delete_block'),
    path('block/<str:name>/links/', ListLinksOfBlock.as_view(), name='blocks_links'),
    path('block/<str:name>/rules/', ListRulesOfBlock.as_view(), name='blocks_rules'),
    path("join/block/", join_block, name="join_block"),
    path('u/joined/block/', user_joined_block, name='user_joined_block'),
    path('u/<str:username>/joined/blocks/', ListBlocksUserJoined.as_view(), name='joined_blocks'),
    path('u/<str:username>/creator/blocks/', ListBlocksOfUser.as_view(), name='creator_blocks'),
    path('u/<str:username>/moderator/blocks/', ListBlocksUserIsModerator.as_view(), name='moderator_blocks'),
    # POST VIEWS    
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    path('post/vote/', VoteOnPost.as_view(), name='vote_post'),
    path('u/voted/post/', user_voted_post, name='user_voted_post'),
    path('retrieve/post/<int:pk>/', RetrievePost.as_view(), name='retrieve_post'),
    path("post/repost/", RePostView , name="repost-view"),
    path("report/post/", report_post, name="report_post"),
    path('u/reported/post/', user_reported_post, name='user_reported_post'),
    path("save/post/", save_post, name="save_post"),
    path('u/saved/post/', user_saved_post, name='user_saved_post'),
    path("users/saved/post/", ListSavedPostsOfUser.as_view(), name="users_saved_post"),
    path('u/<str:username>/posts/', ListPostsOfUser.as_view(), name='users_posts'), 
    path('u/<str:username>/posts/<int:p_id>/', DetailPostOfUser.as_view(), name='users_post_detail'),
    path('b/<str:b_name>/posts/', ListPostsOfBlock.as_view(), name='blocks_posts'),
    path('b/<str:b_name>/posts/<int:p_id>/', DetailPostOfBlock.as_view(), name='blocks_post_detail'),
    # COMMENT VIEWS
    path('create-comment/', CreateCommentView.as_view(), name='create_comment'),
    path('comment/vote/', VoteOnComment.as_view(), name='vote_comment'),
    path('u/voted/comment/', user_voted_comment, name='user_voted_comment'),
    path("report/comment/", report_comment, name="report_comment"),
    path('u/reported/comment/', user_reported_comment, name='user_reported_comment'),
    path("save/comment/", save_comment, name="save_comment"),
    path('u/saved/comment/', user_saved_comment, name='user_saved_comment'),
    path("users/saved/comment/", ListSavedCommentsOfUser.as_view(), name="users_saved_comment"),    
    path('u/<str:username>/comments/', ListCommentsOfUser.as_view(), name='users-comments'),
    path('u/<str:username>/comments/<int:c_id>/', DetailCommentsOfUser.as_view(), name='users-comments-detail'), 
    path('b/<str:b_name>/posts/<int:p_id>/popular-comments/', ListPopularCommentsOfPost.as_view(), name='popular-post-comments'),
    path('b/<str:b_name>/posts/<int:p_id>/old-comments/', ListOldCommentsOfPost.as_view(), name='old-post-comments'),
    path('b/<str:b_name>/posts/<int:p_id>/new-comments/', ListNewCommentsOfPost.as_view(), name='new-post-comments'),
    path('b/<str:b_name>/posts/<int:p_id>/comments/<int:c_id>/', DetailCommentsOfPost.as_view(), name='post-comments-detail'),
]