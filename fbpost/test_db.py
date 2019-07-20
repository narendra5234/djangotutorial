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
        # ARRANGE
        username = "user1"
        pic_url = "https://dummy.url.com/pic.png"

        # ACT
        user = create_user(username, pic_url)

        # ASSERT
        assert user.username == username
        assert user.pic_url == pic_url


# CREATE POST
class TestCreatePost:
    @pytest.mark.django_db
    def test_create_post_no_user(self, user_setup):
        # ARRANGE
        user_id = 5
        post_content = "post1"

        # ACT
        with pytest.raises(User.DoesNotExist):
            create_post(user_id, post_content)

    @pytest.mark.django_db
    def test_create_post(self, user_setup):
        # ARRANGE
        user_id = 1
        post_content = "post1"

        # ACT
        post_id = create_post(user_id, post_content)
        post = Post.objects.get(id=post_id)

        # ASSERT
        assert post.post_content == post_content
        assert post.user.id == user_id


# GET POST
class TestGetPost:
    @pytest.mark.django_db
    def test_get_post_invalid_post_raise_exception(self, user_setup, post_setup):
        # ARRANGE
        post_id = 5

        # ACT
        with pytest.raises(Post.DoesNotExist):
            get_post(post_id)

    @pytest.mark.django_db
    def test_get_post_valid_post_id(self, user_setup, post_setup):
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

        assert len(comment_reaction) == 1
        assert len(post_dictionary["comments"]) == 1

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

        assert len(reply_reaction) == 1
        assert len(post_dictionary["comments"][0]["replies"]) == 1

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
    def test_delete_post_invalid_post_raises_exception(self, user_setup, post_setup):
        # ARRANGE
        post_id = 5

        # ACT
        with pytest.raises(Post.DoesNotExist):
            delete_post(post_id)

    @pytest.mark.django_db
    def test_delete_post_raises_exception(self, user_setup, post_setup):
        # ARRANGE
        post_id = 2

        # ACT
        delete_post(post_id)
        with pytest.raises(Post.DoesNotExist):
            Post.objects.get(id=post_id)


# ADD COMMENT
class TestAddComment:
    @pytest.mark.django_db
    def test_add_comment_invalid_post_raise_exception(self, user_setup, post_setup):
        # ARRANGE
        post_id = 5
        user_id = 1
        comment_content = "comment1"

        # ACT
        with pytest.raises(Post.DoesNotExist):
            add_comment(post_id, user_id, comment_content)

    @pytest.mark.django_db
    def test_add_comment_invalid_user_raise_exception(self, user_setup, post_setup):
        # ARRANGE
        post_id = 1
        user_id = 5
        comment_content = "comment1"

        # ACT
        with pytest.raises(User.DoesNotExist):
            add_comment(post_id, user_id, comment_content)

    @pytest.mark.django_db
    def test_add_comment_valid_post_id_and_user_id(self, user_setup, post_setup):
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
    def test_react_to_post_invalid_user_raise_exception(self, user_setup, post_setup):
        # ARRANGE
        user_id = 5
        post_id = 1
        reaction_type = ReactionType.WOW.value

        # ACT
        with pytest.raises(User.DoesNotExist):
            react_to_post(user_id, post_id, reaction_type)

    @pytest.mark.django_db
    def test_react_to_post_invalid_post_raise_exception(self, user_setup, post_setup):
        # ARRANGE
        user_id = 1
        post_id = 5
        reaction_type = ReactionType.WOW.value

        # ACT
        with pytest.raises(Post.DoesNotExist):
            react_to_post(user_id, post_id, reaction_type)

    @pytest.mark.django_db
    def test_react_to_post_invalid_reaction_raise_exception(self, user_setup, post_setup):
        # ARRANGE
        user_id = 1
        post_id = 1
        reaction_type = "SUPER"

        # ACT
        with pytest.raises(Exception, match=r"Reaction"):
            react_to_post(user_id, post_id, reaction_type)

    @pytest.mark.django_db
    def test_react_to_post_corresponding_to_same_reaction(self, user_setup, post_setup):
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
    def test_react_to_post_corresponding_to_different_reaction(self, user_setup, post_setup):
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
    def test_react_to_post_create_reaction(self, user_setup, post_and_comment_without_reaction_setup):
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


# REACTIONS TO COMMENT
class TestReactToComment:
    @pytest.mark.django_db
    def test_react_to_comment_invalid_user_raise_exception(self, user_setup, post_setup):
        # ARRANGE
        user_id = 5
        comment_id = 1
        reaction_type = ReactionType.WOW.value

        # ACT
        with pytest.raises(User.DoesNotExist):
            react_to_comment(user_id, comment_id, reaction_type)

    @pytest.mark.django_db
    def test_react_to_comment_invalid_comment_raise_exception(self, user_setup, post_setup):
        # ARRANGE
        user_id = 1
        comment_id = 5
        reaction_type = ReactionType.WOW.value

        # ACT
        with pytest.raises(Comment.DoesNotExist):
            react_to_comment(user_id, comment_id, reaction_type)

    @pytest.mark.django_db
    def test_react_to_comment_invalid_reaction_raise_exception(self, user_setup, post_setup):
        # ARRANGE
        user_id = 1
        comment_id = 1
        reaction_type = "SUPER"

        # ACT
        with pytest.raises(Exception, match=r"Reaction"):
            react_to_comment(user_id, comment_id, reaction_type)

    @pytest.mark.django_db
    def test_react_to_comment_corresponding_to_same_reaction(self, user_setup, post_setup):
        # ARRANGE
        user_id = 1
        comment_id = 1
        reaction_type = ReactionType.WOW.value
        comment = Comment.objects.get(id=1)
        reaction = comment.reaction.all()

        assert len(reaction) == 1  # ASSERT

        react_to_comment(user_id, comment_id, reaction_type)  # ACT
        reaction = comment.reaction.all()

        assert len(reaction) == 0  # ASSERT

    @pytest.mark.django_db
    def test_react_to_comment_corresponding_to_different_reaction(self, user_setup, post_setup):
        # ARRANGE
        user_id = 1
        comment_id = 1
        reaction_type = ReactionType.HAHA.value
        comment = Comment.objects.get(id=1)
        reaction = comment.reaction.all()

        assert len(reaction) == 1  # ASSERT
        react_to_comment(user_id, comment_id, reaction_type)  # ACT
        reaction = comment.reaction.all()

        # ASSERT
        assert len(reaction) == 1
        assert reaction[0].react_type == reaction_type

    @pytest.mark.django_db
    def test_react_to_comment_create_reaction(self, user_setup, post_and_comment_without_reaction_setup):
        user_id = 1
        comment_id = 1
        reaction_type = ReactionType.WOW.value
        comment = Comment.objects.get(id=1)
        reaction = comment.reaction.all()

        assert len(reaction) == 0  # ASSERT
        react_to_comment(user_id, comment_id, reaction_type)  # ACT
        reaction = comment.reaction.all()

        # ASSERT
        assert len(reaction) == 1
        assert reaction[0].react_type == reaction_type


# POST REACTED USERS
class TestPostReactedByUser:
    @pytest.mark.django_db
    def test_get_posts_reacted_by_user_invalid_user_raise_exception(self, user_setup,
                                                                    more_positive_reaction_post_setup):
        # ARRANGE
        user_id = 5

        # ACT
        with pytest.raises(User.DoesNotExist):
            get_posts_reacted_by_user(user_id)

    @pytest.mark.django_db
    def test_get_posts_reacted_by_user_valid_user_id(self, user_setup, more_positive_reaction_post_setup):
        # ARRANGE
        user_id = 1
        list_of_post_ids = [1, 3]

        # ACT
        returned_list_of_post_ids = get_posts_reacted_by_user(user_id)

        # ASSERT
        assert returned_list_of_post_ids == list_of_post_ids


# REACTIONS TO POST
class TestReactionsToPost:
    @pytest.mark.django_db
    def test_get_reactions_to_post_invalid_post_raise_exception(self, user_setup, more_positive_reaction_post_setup):
        # ARRANGE
        post_id = 5

        # ACT
        with pytest.raises(Post.DoesNotExist):
            get_reactions_to_post(post_id)

    @pytest.mark.django_db
    def test_get_reactions_to_post_valid_post_id(self, user_setup, more_positive_reaction_post_setup):
        # ARRANGE
        post_id = 1
        post = Post.objects.get(id=post_id)
        # ACT
        list_of_reaction_dictionary = get_reactions_to_post(post_id)
        reaction_queryset = post.reaction.all()
        i = 0
        for reaction in reaction_queryset:
            reaction_dictionary = {}
            reaction_dictionary = list_of_reaction_dictionary[i]
            print(reaction.user.username, reaction_dictionary["name"])
            assert reaction_dictionary["name"] == reaction.user.username
            assert reaction_dictionary["user_id"] == reaction.user.id
            assert reaction_dictionary["profile_pic_url"] == reaction.user.pic_url
            assert reaction_dictionary["reaction"] == reaction.react_type
            i += 1


# REACTION METRICS
class TestReactionMetrics:
    @pytest.mark.django_db
    def test_reaction_metrics_invalid_post_raise_exception(self, user_setup, reaction_metrics_setup):
        # ARRANGE
        post_id = 5

        # ACT
        with pytest.raises(Post.DoesNotExist):
            get_reaction_metrics(post_id)

    @pytest.mark.django_db
    def test_reaction_metrics_valid_post_id(self, user_setup, reaction_metrics_setup):
        # ARRANGE
        post_id = 1

        # ACT
        metric_dictionary = get_reaction_metrics(post_id)

        # ASSERT
        assert metric_dictionary[ReactionType.LIKE.value] == 1
        assert metric_dictionary[ReactionType.HAHA.value] == 2
        assert metric_dictionary[ReactionType.WOW.value] == 1
        assert metric_dictionary[ReactionType.SAD.value] == 1


# POSTS WITH MORE POSITIVE REACTIONS
class TestMorePositivePosts:
    @pytest.mark.django_db
    def test_posts_with_more_positive_reactions(self, user_setup, more_positive_reaction_post_setup):
        # ARRANGE
        list_of_post_ids = [1]

        # ACT
        returned_list_of_post_ids = get_posts_with_positive_reactions()

        # ASSERT
        assert returned_list_of_post_ids == list_of_post_ids


# REPLY TO COMMENT
class TestReplyToComment:
    @pytest.mark.django_db
    def test_reply_to_comment_invalid_user_raise_exception(self, user_setup, post_setup):
        # ARRANGE
        comment_id = 1
        user_id = 5
        reply_text = "reply1"

        # ACT
        with pytest.raises(User.DoesNotExist):
            reply_to_comment(comment_id, user_id, reply_text)

    @pytest.mark.django_db
    def test_reply_to_comment_invalid_comment_raise_exception(self, user_setup, post_setup):
        # ARRANGE
        comment_id = 5
        user_id = 1
        reply_text = "reply1"

        # ACT
        with pytest.raises(Comment.DoesNotExist):
            reply_to_comment(comment_id, user_id, reply_text)

    @pytest.mark.django_db
    def test_reply_to_comment_valid_comment_id_and_user_id(self, user_setup, post_setup):
        # ARRANGE
        user_id = 1
        comment_id = 1
        reply_text = "reply1"

        reply_id = reply_to_comment(comment_id, user_id, reply_text)  # ACT
        reply = Comment.objects.get(id=reply_id)

        # ASSERT
        assert reply.comment_content == reply_text
        assert reply.commented_by.id == user_id


# GET REPLIES FOR COMMENT
class TestRepliesForComment:
    @pytest.mark.django_db
    def test_replies_for_comment_invalid_comment_raise_exception(self, user_setup, post_setup):
        # ARRANGE
        comment_id = 5

        # ACT
        with pytest.raises(Comment.DoesNotExist):
            get_replies_for_comment(comment_id)

    @pytest.mark.django_db
    def test_replies_for_comment_valid_comment_id(self, user_setup, post_setup):
        # ARRANGE
        comment_id = 1
        comment = Comment.objects.get(id=comment_id)

        # ACT
        list_of_reply_dictionary = get_replies_for_comment(comment_id)
        reply_query_set = comment.reply.all()
        i = 0
        for reply in reply_query_set:
            reply_dictionary = {}
            reply_dictionary = list_of_reply_dictionary[i]
            assert reply_dictionary["comment_id"] == reply.id
            assert reply_dictionary["commenter"] == {"name": reply.commented_by.username,
                                                     "user_id": reply.commented_by.id,
                                                     "profile_pic_url": reply.commented_by.pic_url}
            assert reply_dictionary["commented_at"] == reply.comment_at.strftime("%Y-%m-%d %H:%M:%S.%f")
            assert reply_dictionary["comment_content"] == reply.comment_content
            i += 1


# GET USER POSTS
class TestGetUserPosts:
    @pytest.mark.django_db
    def test_get_user_posts_invalid_user_raise_exception(self, user_setup, post_setup):
        # ARRANGE
        user_id = 5

        # ACT
        with pytest.raises(User.DoesNotExist):
            get_user_posts(user_id)

    @pytest.mark.django_db
    def test_get_user_posts_valid_user_id(self, user_setup, post_setup):
        # ARRANGE
        user_id = 1
        user = User.objects.get(id=user_id)

        # ACT
        list_of_user_posts = get_user_posts(user_id)
        post_query_set = user.posts.all()
        i = 0
        for post in post_query_set:
            post_dictionary = list_of_user_posts[i]
            # ASSERT
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
            i += 1
