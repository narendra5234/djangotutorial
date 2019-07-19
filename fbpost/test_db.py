from fbpost.models import *
from datetime import datetime
from fbpost.model_methods import *
from django.db.models import *
from django.db import connection
import pytest


# CREATE USER
class TestCreateUser:
    @pytest.mark.django_db
    def test_create_user(self):
        username = "user1"
        pic_url = "https://dummy.url.com/pic.png"
        user = create_user(username, pic_url)
        assert user.username == username
        assert user.pic_url == pic_url


# CREATE POST
class TestCreatePost:
    @pytest.mark.django_db
    def test_create_post_no_user(self, user_setup):
        user_id = 5
        post_content = "post1"
        with pytest.raises(User.DoesNotExist):
            create_post(user_id, post_content)

    @pytest.mark.django_db
    def test_create_post(self, user_setup):
        user_id = 1
        post_content = "post1"
        post_id = create_post(user_id, post_content)
        post = Post.objects.get(id=post_id)
        assert post.post_content == post_content
        assert post.user.id == user_id


# GET POST
class TestGetPost:
    @pytest.mark.django_db
    def test_create_post_no_post(self, user_setup, post_setup):
        post_id = 5
        with pytest.raises(Post.DoesNotExist):
            get_post(post_id)

    @pytest.mark.django_db
    def test_get_post(self, user_setup, post_setup):
        # ARRANGE
        post_id = 1
        post = Post.objects.get(id=1)

        # ACT
        post_dictionary = get_post(post_id)

        # ASSERT
        # post
        assert post_dictionary["post_id"] == post.id
        assert post_dictionary["posted_by"] == {"name": post.user.username, "user_id": post.user.id,
                                                "profile_pic_url": post.user.pic_url}
        assert post_dictionary["posted_at"] == post.post_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        assert post_dictionary["post_content"] == post.post_content
        post_reaction = post.reaction.all()
        assert post_dictionary["reactions"] == {"count": len(post_reaction), "type": [post_reaction[0].react_type]}

        # comment
        comment_queryset = post.comments.all()
        comment = post.comments.all()[0]
        comment_reaction = comment.reaction.all()
        comment_dictionary = post_dictionary["comments"][0]
        assert comment_dictionary["comment_id"] == comment.id
        assert comment_dictionary["commenter"] == {"name": comment.commented_by.username,
                                                   "user_id": comment.commented_by.id,
                                                   "profile_pic_url": comment.commented_by.pic_url}
        assert comment_dictionary["commented_at"] == comment.comment_at.strftime("%Y-%m-%d %H:%M:%S.%f")
        assert comment_dictionary["reactions"] == {"count": len(comment_reaction),
                                                   "type": [comment_reaction[0].react_type]}

        # reply
        reply_queryset = comment.reply.all()
        reply = comment.reply.all()[0]
        reply_reaction = reply.reaction.all()
        reply_dictionary = post_dictionary["comments"][0]["replies"][0]
        assert post_dictionary["comments"][0]["replies_count"] == len(reply_queryset)
        assert reply_dictionary["comment_id"] == reply.id
        assert reply_dictionary["commenter"] == {"name": reply.commented_by.username,
                                                 "user_id": reply.commented_by.id,
                                                 "profile_pic_url": reply.commented_by.pic_url}
        assert reply_dictionary["commented_at"] == reply.comment_at.strftime("%Y-%m-%d %H:%M:%S.%f")
        assert reply_dictionary["reactions"] == {"count": len(reply_reaction),
                                                 "type": [reply_reaction[0].react_type]}
        assert post_dictionary["comments_count"] == len(comment_queryset)


# DELETE POST
class TestDeletePost:
    @pytest.mark.django_db
    def test_delete_post_no_post(self, user_setup, post_setup):
        post_id = 5
        with pytest.raises(Post.DoesNotExist):
            delete_post(post_id)

    @pytest.mark.django_db
    def test_delete_post(self, user_setup, post_setup):
        post_id = 2
        delete_post(post_id)
        with pytest.raises(Post.DoesNotExist):
            Post.objects.get(id=post_id)


# ADD COMMENT
class TestAddComment:
    @pytest.mark.django_db
    def test_add_comment_no_user(self, user_setup, post_setup):
        with pytest.raises(Post.DoesNotExist):
            add_comment(5, 1, "comment1")

    @pytest.mark.django_db
    def test_add_comment_no_post(self, user_setup, post_setup):
        with pytest.raises(User.DoesNotExist):
            add_comment(1, 5, "comment1")

    @pytest.mark.django_db
    def test_add_comment(self, user_setup, post_setup):
        # ARRANGE
        user_id = 1
        post_id = 1
        comment_content = "comment1"
        comment_id = add_comment(post_id, user_id, "comment1")  # ACT
        comment = Comment.objects.get(id=comment_id)
        # ASSERT
        assert comment.comment_content == comment_content
        assert comment.commented_by.id == user_id
        assert comment.post.id == post_id


# REACTIONS TO POST
class TestReactToPost:
    @pytest.mark.django_db
    def test_react_to_post_no_user(self, user_setup, post_setup):
        # ARRANGE
        user_id = 5
        post_id = 1
        reaction_type = ReactionType.WOW.value

        # ACT
        with pytest.raises(User.DoesNotExist):
            react_to_post(user_id, post_id, reaction_type)

    @pytest.mark.django_db
    def test_react_to_post_no_post(self, user_setup, post_setup):
        # ARRANGE
        user_id = 1
        post_id = 5
        reaction_type = ReactionType.WOW.value

        # ACT
        with pytest.raises(Post.DoesNotExist):
            react_to_post(user_id, post_id, reaction_type)

    @pytest.mark.django_db
    def test_react_to_post_no_reaction(self, user_setup, post_setup):
        # ARRANGE
        user_id = 1
        post_id = 1
        reaction_type = "SUPER"

        # ACT
        with pytest.raises(Exception, match=r"Reaction"):
            react_to_post(user_id, post_id, reaction_type)

    @pytest.mark.django_db
    def test_react_to_post_same_reaction(self, user_setup, post_setup):
        # ARRANGE
        user_id = 1
        post_id = 1
        reaction_type = ReactionType.HAHA.value
        post = Post.objects.get(id=1)
        reaction = post.reaction.all()

        assert len(reaction) == 1  # ASSERT

        react_to_post(user_id, post_id, reaction_type)  # ACT
        reaction = post.reaction.all()

        assert len(reaction) == 0  # ASSERT

    @pytest.mark.django_db
    def test_react_to_post_different_reaction(self, user_setup, post_setup):
        # ARRANGE
        user_id = 1
        post_id = 1
        reaction_type = ReactionType.WOW.value
        post = Post.objects.get(id=1)
        reaction = post.reaction.all()

        assert len(reaction) == 1  # ASSERT

        react_to_post(user_id, post_id, reaction_type)  # ACT
        reaction = post.reaction.all()

        # ASSERT
        assert len(reaction) == 1
        assert reaction[0].react_type == reaction_type

    @pytest.mark.django_db
    def test_react_to_post_create_reaction(self, user_setup, post_without_reaction_setup):
        # ARRANGE
        user_id = 1
        post_id = 1
        reaction_type = ReactionType.WOW.value
        post = Post.objects.get(id=1)
        reaction = post.reaction.all()

        assert len(reaction) == 0  # ASSERT
        react_to_post(user_id, post_id, reaction_type)  # ACT
        reaction = post.reaction.all()

        # ASSERT
        assert len(reaction) == 1
        assert reaction[0].react_type == reaction_type

#
# class TestReactToComment:
#     @pytest.mark.django_db
#     def test_react_to_comment_no_user(self, user_setup, post_setup):
#         user_id = 5
#         comment_id = 1
#         reaction_type = ReactionType.WOW.value
#         with pytest.raises(User.DoesNotExist):
#             react_to_comment(user_id, comment_id, reaction_type)
#
#     @pytest.mark.django_db
#     def test_react_to_comment_no_post(self, user_setup, post_setup):
#         # ARRANGE
#         user_id = 1
#         comment_id = 5
#         reaction_type = ReactionType.WOW.value
#         # ACT
#         with pytest.raises(Comment.DoesNotExist):
#             react_to_comment(user_id, comment_id, reaction_type)
#
#     @pytest.mark.django_db
#     def test_react_to_comment_no_reaction(self, user_setup, post_setup):
#         # ARRANGE
#         user_id = 1
#         comment_id = 1
#         reaction_type = "SUPER"
#         # ACT
#         with pytest.raises(Exception, match=r"Reaction"):
#             react_to_comment(user_id, comment_id, reaction_type)
#
#     @pytest.mark.django_db
#     def test_react_to_comment_same_reaction(self, user_setup, post_setup):
#         # ARRANGE
#         user_id = 1
#         comment_id = 1
#         reaction_type = ReactionType.HAHA.value
#         comment = Comment.objects.get(id=1)
#         reaction = comment.reaction.all()
#         assert len(reaction) == 1  # ASSERT
#         react_to_comment(user_id, comment_id, reaction_type)  # ACT
#         reaction = comment.reaction.all()
#         assert len(reaction) == 0  # ASSERT
#
#     @pytest.mark.django_db
#     def test_react_to_comment_different_reaction(self, user_setup, post_setup):
#         # ARRANGE
#         user_id = 1
#         comment_id = 1
#         reaction_type = ReactionType.WOW.value
#         comment = Comment.objects.get(id=1)
#         reaction = comment.reaction.all()
#         assert len(reaction) == 1  # ASSERT
#         react_to_comment(user_id, post_id, reaction_type)  # ACT
#         reaction = comment.reaction.all()
#         # ASSERT
#         assert len(reaction) == 1
#         assert reaction[0].react_type == reaction_type
#
#     @pytest.mark.django_db
#     def test_react_to_comment_create_reaction(self, user_setup, post1_setup):
#         user_id = 1
#         comment_id = 1
#         reaction_type = ReactionType.WOW.value
#         comment = Comment.objects.get(id=1)
#         reaction = comment.reaction.all()
#         assert len(reaction) == 0  # ASSERT
#         react_to_comment(user_id, comment_id, reaction_type)  # ACT
#         reaction = post.reaction.all()
#         # ASSERT
#         assert len(reaction) == 1
#         assert reaction[0].react_type == reaction_type
