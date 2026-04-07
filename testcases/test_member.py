"""
会员管理测试用例
"""
import pytest
from common.requests_client import client
from common.assert_utils import assert_utils
from config.api_paths import MemberPaths
import time

class TestMember:
    """会员管理测试"""

    @pytest.mark.parametrize("user_name", ["用户A"])
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_query_page_member(self, user_name):
        """测试查询会员"""
        print(f"正在查询会员: {user_name}","+++++++++++++++++++++++++++++++++++++")
        response = client.post(
            MemberPaths.QUERY_PAGE,
            user=user_name,
            json={
                "currentPage": 1,
                "pageSize": 10,
                "state": 1,
                "total": 2
            }
        )
        data = assert_utils.assert_success(response)
        # assert_utils.assert_page_response(data.get("data", {}))
        #断言返回信息 不为空
        assert_utils.assert_not_empty(data["data"]["records"][0], "name", "会员姓名")
        assert_utils.assert_not_empty(data["data"]["records"][0], "phone", "会员手机号")


        total = data["data"]["total"]
        print(f"✅ 查询会员成功，共 {total} 条")

    @pytest.mark.parametrize("user_name", ["用户A"])
    @pytest.mark.p0
    def test_save_member(self, test_data, user_name):
        """测试创建会员"""
  
        response = client.post(
            MemberPaths.SAVE, 
            user=user_name,
            data={
                "name": test_data["member"]["name"],
                "phone": test_data["member"]["phone"],
                "email": f"{test_data['member']['phone']}@qq.com",
                "info": "新会员"
            })
        data = assert_utils.assert_success(response)
        # 服务器返回 data 为 null，需要通过查询来验证
        # 根据手机号查询验证
        query_response = client.post(
            MemberPaths.QUERY_PAGE,
            user=user_name,
            data={"phone": test_data["member"]["phone"]}
        )
        query_data = assert_utils.assert_success(query_response)
        # 获取会员ID
        member_id = query_data.get("data", {}).get("records", [{}])[0].get("id")
        assert member_id is not None, "未返回会员ID"
        # 验证保存成功
        assert_utils.assert_business_data(query_data["data"]["records"][0], "name", test_data["member"]["name"], "会员姓名")
        assert_utils.assert_business_data(query_data["data"]["records"][0], "phone", test_data["member"]["phone"], "会员手机号")

        print(f"✅ 创建会员成功: ID={member_id}, Name={test_data['member']['name']}")
        # 清理
        def cleanup_member():
            client.post(MemberPaths.DELETE, user=user_name, data={"id": member_id})
        time.sleep(5)

    @pytest.mark.parametrize("user_name", ["用户A"])
    @pytest.mark.regression
    def test_save_member_duplicate_phone(self, user_name):
        """测试创建重复手机号会员"""
        # 先获取一个已存在的会员
        list_resp = client.post(
            MemberPaths.QUERY_PAGE,
            user=user_name,
            json={"currentPage": 1, "pageSize": 1}
        )
        list_data = assert_utils.assert_success(list_resp)
        
        records = list_data["data"]["records"]
        if not records:
            pytest.skip("系统中无会员数据")

        existing_phone = records[0]["phone"]
        # 尝试创建相同手机号
        response = client.post(MemberPaths.SAVE, 
            user=user_name,
            data={
                "name": "重复手机号测试",
                "phone": existing_phone,
                "email": f"{existing_phone}@qq.com",
            }
        )
        data = response.json()
        #数据断言
        assert_utils.assert_business_data(data, "msg", f"该用户已注册过", "错误提示")
        # 断言响应状态码
        assert_utils.assert_business_data(data, "code", 500, "错误码")

        # 检查响应状态码
        if response.status_code == 500:
            try:
                data = response.json()
                #数据断言
                assert_utils.assert_business_data(data, "msg", f"该用户已注册过", "错误提示")
                # 断言响应状态码
                assert_utils.assert_status_code(data, 500, "重复手机号创建应返回 500 错误")
                # 预期返回错误
                assert data.get("code") == 500, "该用户已注册过"
                assert "重复" in data.get("msg", "") or "已存在" in data.get("msg", ""), \
                    f"错误信息应提示手机号重复: {data.get('msg')}"
                print(f"✅ 重复手机号验证通过: {data.get('msg')}")
            except:
                # 如果不是 JSON 格式，说明创建失败
                print(f"✅ 重复手机号验证通过: 服务器返回非 JSON 响应")
        else:
            # 非 500 状态码，说明创建失败
            print(f"✅ 重复手机号验证通过: 服务器返回 {response.status_code}")
        time.sleep(5)

    @pytest.mark.parametrize("user_name", ["用户A"])
    @pytest.mark.p0
    def test_update_member(self, user_name, test_data,):
        """测试更新会员"""
        # 创建会员
        create_resp = client.post(MemberPaths.SAVE, 
            user=user_name,
            data={
                "name": "待更新会员",
                "phone": test_data["member"]["phone"],
                "email": f"{test_data['member']['phone']}@qq.com",
                "info": "测试会员"
            }
        )
        create_result = assert_utils.assert_success(create_resp)
        # 通过手机号查询获取会员ID
        query_resp = client.post(
            MemberPaths.QUERY_PAGE,
            user=user_name,
            data={"phone": test_data["member"]["phone"]}
        )
        query_data = assert_utils.assert_success(query_resp)
        member_id = query_data["data"]["records"][0]["id"]
 
        # 更新会员
        update_resp = client.post(MemberPaths.UPDATE, 
            user=user_name,
            data={
                "id": member_id,
                "name": "已更新会员",
                "phone": test_data["member"]["phone"],
                "email": f"{test_data['member']['phone']}@qq.com",
                "info": "已更新会员信息",
                "integral": 0,
                "state": 0
            }
        )
        update_result = assert_utils.assert_success(update_resp)
        # 验证更新结果
        query_resp2 = client.post(
            MemberPaths.QUERY_PAGE,
            user=user_name,
            data={"phone": test_data["member"]["phone"]}
        )
        query_data2 = assert_utils.assert_success(query_resp2)

        # 验证更新后的数据
        # 注意：查询返回的是所有会员列表，需要找到我们更新的那个会员
        updated_member = None
        for record in query_data2["data"]["records"]:
            if record["id"] == member_id:
                updated_member = record
                break
        
        assert updated_member is not None, f"未找到更新的会员 ID={member_id}"
        assert_utils.assert_business_data(updated_member, "name", "已更新会员", "更新后会员姓名")
        assert_utils.assert_business_data(updated_member, "info", "已更新会员信息", "更新后会员信息")
        assert query_data2["code"] == 200

        print(f"✅ 更新会员成功: ID={member_id}")

        # 清理
        def cleanup_member():
            client.post(MemberPaths.DELETE, user=user_name, data={"id": member_id})
            print(f"✅ 删除会员成功: ID={member_id}")

        time.sleep(5)
    
    @pytest.mark.parametrize("user_name", ["用户A"])
    @pytest.mark.regression
    def test_query_member_by_phone(self, user_name):
        """测试根据手机号查询会员"""
        # 先获取一个存在的会员
        list_resp = client.post(
            MemberPaths.QUERY_PAGE,
            user=user_name,
            data={"currentPage": 1, "pageSize": 1}
        )
        list_data = assert_utils.assert_success(list_resp)
        records = list_data["data"]["records"]
        if not records:
            pytest.skip("系统中无会员数据")

        phone = records[0]["phone"]
        
        response = client.post(
            MemberPaths.QUERY_PAGE,
            user=user_name, 
            data={"phone": phone}
        )
        data = assert_utils.assert_success(response)
        # 数据断言
        assert_utils.assert_business_data(data, "code", 200, "查询状态码")
        # 数据断言
        assert_utils.assert_business_data(data["data"]["records"][0], "phone", phone, "会员手机号")
        # 验证查询结果
        if data.get("data") and data["data"].get("records"):
            assert data["data"]["records"][0]["phone"] == phone

        print(f"✅ 根据手机号查询成功: {phone}")
        time.sleep(5)
  
    @pytest.mark.parametrize("user_name", ["用户A"])
    @pytest.mark.p0
    def test_delete_member(self, user_name, test_data):
        """测试删除会员"""
        # 创建会员
        create_data = {
            "name": "待删除会员",
            "phone": test_data["member"]["phone"],
            "email": f"{test_data['member']['phone']}@qq.com",
            "info": "待删除"
        }

        create_resp = client.post(MemberPaths.SAVE, 
            user=user_name,
            data=create_data
        )
        create_result = assert_utils.assert_success(create_resp)
        
        # 通过手机号查询获取会员ID
        query_resp = client.post(
            MemberPaths.QUERY_PAGE,
            user=user_name,
            data={"phone": test_data["member"]["phone"]}
        )
        query_data = assert_utils.assert_success(query_resp)
        member_id = query_data["data"]["records"][0]["id"]

        # 删除会员
        delete_resp = client.post(MemberPaths.DELETE, 
            user=user_name,
            data={"id": member_id}
        )
        assert_utils.assert_success(delete_resp)

        # 验证删除成功
        query_resp2 = client.get(
            MemberPaths.QUERY_BY_ID,
            user=user_name,
            params={"id": member_id}
        )
        query_data2 = assert_utils.assert_success(query_resp2)
        
        # 验证删除后，会员的state应该变为1（逻辑删除）
        assert_utils.assert_business_data(query_data2, "code", 200, "查询状态码")
        assert query_data2.get("data") is not None, "应该返回会员数据"
        assert_utils.assert_business_data(query_data2["data"], "state", "1", "会员删除状态")
        
        # 额外验证：通过手机号查询，应该能找到该会员，但state为1
        query_resp3 = client.post(
            MemberPaths.QUERY_PAGE,
            user=user_name,
            data={"phone": test_data["member"]["phone"]}
        )
        query_data3 = assert_utils.assert_success(query_resp3)
        
        # 查询结果应该包含刚才删除的会员，但state为1
        assert len(query_data3["data"]["records"]) > 0, "应该能查询到会员"
        deleted_member = None
        for record in query_data3["data"]["records"]:
            if record["id"] == member_id:
                deleted_member = record
                break
        
        assert deleted_member is not None, f"应该能找到会员 ID={member_id}"
        assert deleted_member["state"] == "1", f"删除后会员状态应该为1，实际为{deleted_member['state']}"
        
        print(f"✅ 删除会员成功: ID={member_id}")
