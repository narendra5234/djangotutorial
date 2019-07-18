# def f():
#     return 3
#
#
# def test_function():
#     assert f() == 3
#
#
# import pytest
#
#
# def test_zero_division():
#     # with pytest.raises((ZeroDivisionError)):
#     1 / 0
#
# @pytest.mark.xfail(raises=RuntimeError)
# def test_recursion_depth():
#     # with pytest.raises(RuntimeError) as excinfo:
#     def f():
#         f()
#
#     f()
#     # assert "maximum recursion" in str(excinfo.value)
#
