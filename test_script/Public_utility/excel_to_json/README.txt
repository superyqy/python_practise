��������API json��ʽ���������ɽű�
���ߣ�������
����ʱ�䣺2018-06-22
��Ҫ���ܣ�����Ŀ���ļ��У���ȡ.xls��׺��excel�ļ���������template������sheet�е�API������������ת��ΪJson��ʽ���洢��TXT�ı���
Ӧ�ó�����API��Ҫpost���ݣ���post�������ֶκܶ࣬ͨ�����ýű��Զ�����json�壬������˹���װJson��ʽЧ�ʵ͡��׳��������
�����ű���Python


ǰ�᣺
1.excel����ʽʹ��.xls
2.����template��ʽ����װ��������
3.ͨ�������з�ʽ���ýű�
4.����δ֪�����봫��excel�ļ���������·��ʹ��Ӣ��


�ű�ʹ�÷�����
��1. ����������������ļ���
python E:\excel_to_json\excel_to_json.py E:\excel_to_json\testcase
python E:\excel_to_json\excel_to_json.py E:\\excel_to_json\\testcase  ##���ýű����ڻ�����windowsϵͳʱ�����ⲿ�������·���У�ʹ��˫б��
��2. ����������������ļ�·��
python E:\excel_to_json\excel_to_json.py E:\excel_to_json\testcase\api_testcase_template.xls

�ű������
1. �Զ������ļ��в㼶�� �������������ļ���\ʱ��\excel�ļ���\
2. ����sheet���ƣ�����sheet.txt��ÿ��TXT�а�����ǰsheet�����еĲ������������json����


Excel����д��(���ϸ���template�е�Ԫ�������ɫ�ĸ�ʽ¼����������������������㼶�ṹ)��
1. Test case Name: ������������������Ҳ��ܴ�����ͬ�ظ�����������
2. 1st_level: ��һ�㼶�����json���޲㼶֮�֣�ֱ��ɾ��1st_level�������ĵ�Ԫ������ڣ�������������������ӣ����������ж�Ӧ��Ԫ����Ҫ��д��һ����ֵ�� ��һ�㼶��ɴ��ڵڶ��㼶��Ҳ�ɲ�����
3. 2rd_level: �ڶ��㼶��ֻ�е�һ�㼶���ڣ��������ӵڶ��㼶�������еڶ��㼶��Ӧ��Ԫ������д�κ����ݣ�
4. ����1st_level��2rd_level֮����Ƕ�Ӧ�Ĳ�����������ֵ

���ɽ��ʾ����
��������1���޲㼶_1:{"overdueAmount": -10000.05, "cardType": "credit card", "cardid": 12332145698754656, "creditCardCount": 3, "bankName": "ZhaoShang Bank"}

��������2�� ���������㼶���ڶ����㼶�ж��:{"creditBankCardInfoList_one": [{"overdueAmount": -10000.05, "cardid": 111111145698754656, "bankName": "��������"}, {"overdueAmount": 5000, "cardid": 22222222416456165156, "bankName": "ũҵ����"}], "creditBaseInfo": [{"cardNo": "CD1234", "cardType": "ID Card", "creditCardCount": 3}]}

��������3�� �����㼶��һ���㼶���������:{"creditBankCardInfoList": [{"overdueAmount": -10000.05, "cardid": 12333333333333388, "bankName": "��������"}, {"overdueAmount": 5000, "cardid": 12314545416456165156, "bankName": "�������"}], "creditBaseInfo": {"cardNo": "CD1234", "cardType": "ID Card", "creditCardCount": 3}}

��������4��ֻ����һ���㼶�����ж��:{"creditBankCardInfoList": {"overdueAmount": -10000.05, "cardid": 12332145698754656, "bankName": "ũҵ����"}, "anotherBankcardinfolist": {"overdueAmount": 5000, "cardid": 12314545416456165156, "bankName": "�������"}, "creditBaseInfo": {"cardNo": "CD1234", "cardType": "ID Card", "creditCardCount": 3}}