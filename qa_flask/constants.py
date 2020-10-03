from enum import Enum

class UserStatus(Enum):
    """用户表，用户状态"""
    # 启用，可以登陆系统
    USER_ACTIVE = 0
    # 禁用，不能登陆系统
    USER_ACTIVE = 1


class UserRole(Enum):
    """用户表，用户角色"""
    # 普通用户，可以使用前台功能
    COMMON = 0
    # 管理员用户，可以使用后台管理功能
    ADMIN = 1
    # 超级管理员，可以删除敏感数据，如用户信息等
    SUPER_ADMIN = 2

class Valid(Enum):
    """逻辑删除"""
    # 生效
    IS_VALID = 0
    # 无效
    IS_VALID = 1


class QaPublic(Enum):
    """是否公开"""
    # 公开
    IS_PUBLIC = 0
    # 不公开
    IS_PUBLIC