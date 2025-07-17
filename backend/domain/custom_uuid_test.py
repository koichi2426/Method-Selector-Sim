# uuid_test.py
import unittest
import uuid as std_uuid  # 標準のuuidモジュールを別名でインポート

# 変更後のファイル名 'custom_uuid' からインポートします
from custom_uuid import NewUUID, UUID

class TestCustomUUID(unittest.TestCase):

    def test_new_uuid_returns_correct_type(self):
        """
        NewUUID()が正しいUUIDクラスのインスタンスを返すことをテストします。
        """
        new_id = NewUUID()
        self.assertIsInstance(new_id, UUID, "返り値がUUIDクラスのインスタンスではありません。")

    def test_new_uuid_value_is_valid_format(self):
        """
        NewUUID()が生成する値が有効なUUID形式であることをテストします。
        """
        new_id = NewUUID()
        try:
            # 標準のuuid.UUID()で解釈できるか試すことで、形式を検証する
            std_uuid.UUID(new_id.value)
        except ValueError:
            self.fail(f"'{new_id.value}' は有効なUUID形式ではありません。")

    def test_new_uuid_generates_unique_values(self):
        """
        NewUUID()を2回呼び出した際に、異なる値が生成されることをテストします。
        """
        id_1 = NewUUID()
        id_2 = NewUUID()
        self.assertNotEqual(id_1.value, id_2.value, "2つのUUIDが同じ値です。")

if __name__ == '__main__':
    unittest.main()