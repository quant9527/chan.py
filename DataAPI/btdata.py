from Common.CEnum import AUTYPE, DATA_FIELD, KL_TYPE
from Common.CTime import CTime
from Common.func_util import kltype_lt_day, str2float
from DataAPI.CommonStockAPI import CCommonStockApi
from KLine.KLine_Unit import CKLine_Unit




def create_item_dict(data, column_name):
    for i in range(len(data)):
        data[i] = parse_time_column(data[i]) if i == 0 else str2float(data[i])
    return dict(zip(column_name, data))


def parse_time_column(inp):
    # 20210902113000000
    # 2021-09-13
    if len(inp) == 10:
        year = int(inp[:4])
        month = int(inp[5:7])
        day = int(inp[8:10])
        hour = minute = 0
    elif len(inp) == 17:
        year = int(inp[:4])
        month = int(inp[4:6])
        day = int(inp[6:8])
        hour = int(inp[8:10])
        minute = int(inp[10:12])
    elif len(inp) == 19:
        year = int(inp[:4])
        month = int(inp[5:7])
        day = int(inp[8:10])
        hour = int(inp[11:13])
        minute = int(inp[14:16])
    else:
        raise Exception(f"unknown time column from baostock:{inp}")
    return CTime(year, month, day, hour, minute)


def GetColumnNameFromFieldList(fileds: str):
    _dict = {
        "time": DATA_FIELD.FIELD_TIME,
        "date": DATA_FIELD.FIELD_TIME,
        "open": DATA_FIELD.FIELD_OPEN,
        "high": DATA_FIELD.FIELD_HIGH,
        "low": DATA_FIELD.FIELD_LOW,
        "close": DATA_FIELD.FIELD_CLOSE,
        "volume": DATA_FIELD.FIELD_VOLUME,
        "amount": DATA_FIELD.FIELD_TURNOVER,
        "turn": DATA_FIELD.FIELD_TURNRATE,
    }
    return [_dict[x] for x in fileds.split(",")]


class BtData(CCommonStockApi):
    is_connect = None

    def __init__(self,  code, k_type=KL_TYPE.K_DAY, begin_date=None, end_date=None, autype=AUTYPE.QFQ,data_src_v=None):
        super(BtData, self).__init__(code, k_type, begin_date, end_date, autype)
        self.data = data_src_v

    def get_kl_data(self):
        for i in range(self.data.close.idx):
            yield CKLine_Unit(create_item_dict(rs.get_row_data(), GetColumnNameFromFieldList(fields)))

    def SetBasciInfo(self):
        self.name = self.code
        self.is_stock =True


    @classmethod
    def do_init(cls):
        pass

    @classmethod
    def do_close(cls):
        pass

    def __convert_type(self):
        _dict = {
            KL_TYPE.K_DAY: 'd',
            KL_TYPE.K_WEEK: 'w',
            KL_TYPE.K_MON: 'm',
            KL_TYPE.K_5M: '5',
            KL_TYPE.K_15M: '15',
            KL_TYPE.K_30M: '30',
            KL_TYPE.K_60M: '60',
        }
        return _dict[self.k_type]
