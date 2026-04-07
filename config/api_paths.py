"""
API 接口路径常量
"""

class LoginPaths:
    """登录相关接口"""
    LOGIN = "/login"
    EXIT = "/exit"
    LOGOUT = "/logout"
    EMP_MENU = "/empMenu"
    CHECKED_TOKEN = "/checkedToken"

class MemberPaths:
    """会员管理接口"""
    QUERY_PAGE = "/member_management/member/queryPageByQo"
    DELETE = "/member_management/member/delMember"
    SAVE = "/member_management/member/save"
    QUERY_BY_ID = "/member_management/member/queryMemberById"
    UPDATE = "/member_management/member/update"
    QUERY_BY_PHONE = "/member_management/member/queryMemberByPhone"

class GoodsPaths:
    """商品管理接口"""
    QUERY_PAGE = "/goods_management/goods/queryPageByQo"
    UPLOAD_IMG = "/goods_management/goods/uploadImg"
    SAVE = "/goods_management/goods/save"
    UP_OR_DOWN = "/goods_management/goods/upOrdown"
    QUERY_BY_ID = "/goods_management/goods/queryGoodsById"
    UPDATE = "/goods_management/goods/update"
    SELECTED_GOODS_ALL = "/goods_management/goods/selected_goodsAll"
    SELECTED_STORE_ALL = "/goods_management/goods/selected_storeAll"
    RETURN_GOODS = "/goods_management/goods/returnGoods"

class SaleRecordPaths:
    """销售记录接口"""
    GET_CN = "/sale_management/sale_record/getCn"
    GET_OPTION_GOODS = "/sale_management/sale_record/getOptionSaleRecordsGoods"
    SAVE = "/sale_management/sale_record/saveSaleRecords"
    QUERY_PAGE = "/sale_management/sale_record/queryPageByQoSaleRecords"
    DELETE = "/sale_management/sale_record/delSaleRecords"

class StoreInPaths:
    """入库管理接口"""
    SAVE = "/inventory_management/detail_store_goods_in/save"
    QUERY_PAGE = "/inventory_management/detail_store_goods_in/queryPageByQo"
    DELETE = "/inventory_management/detail_store_goods_in/delIn"
    QUERY_OPTIONS_SUPPLIERS = "/inventory_management/detail_store_goods_in/queryOptionsSuppliers"

class StoreOutPaths:
    """出库管理接口"""
    QUERY_PAGE = "/inventory_management/detail_store_goods_out/queryPageByQoOut"
    INIT_OPTIONS = "/inventory_management/detail_store_goods_out/initOutOptions"
    CHANGE_OUT_GOODS = "/inventory_management/detail_store_goods_out/changeOutGoods"
    CHANGE_OUT_STORE = "/inventory_management/detail_store_goods_out/changeOutStore"
    QUERY_OUT_GOODS = "/inventory_management/detail_store_goods_out/queryOutGoods"
    SAVE = "/inventory_management/detail_store_goods_out/save"
    DELETE = "/inventory_management/detail_store_goods_out/delOut"

class RolePaths:
    """角色管理接口"""
    LIST = "/system/role/list"
    FORBIDDEN = "/system/role/forbiddenRole"
    EDIT = "/system/role/edit_role"
    SAVE = "/system/role/save"
    CHECK_PERMISSIONS = "/system/role/checkPermissons"
    SAVE_ROLE_PERMISSIONS = "/system/role/saveRolePermissons"
    ALL = "/system/role/all"
    QUERY_ROLE_IDS_BY_EID = "/system/role/queryRoleIdsByEid"
    SAVE_ROLE_EMP = "/system/role/saveRoleEmp"

class EmployeePaths:
    """员工管理接口"""
    LIST = "/personnel_management/employee/list"
    DETAIL = "/personnel_management/employee/detail"
    UPLOAD_IMG = "/personnel_management/employee/uploadImg"
    SAVE = "/personnel_management/employee/save"
    EDIT_BTN = "/personnel_management/employee/editbtn"
    UPDATE = "/personnel_management/employee/update"
    DEACTIVATE = "/personnel_management/employee/deactivate"
    RESET_PWD = "/personnel_management/employee/resetPwd"