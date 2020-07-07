# -*- coding=utf-8 -*-


from StringIO import StringIO
import csv
import json
import sys


def unicode_to_utf8(o):
    return o.encode('utf-8') if isinstance(o, unicode) else o


class CsvHelper(object):

    __bom_map__ = {
        "utf8": "\xEF\xBB\xBF",
    }

    @classmethod
    def bom_wrapped(cls, lines, code="utf8"):
        assert code in cls.__bom_map__.keys(), \
            "code must be in ({})".format(cls.__bom_map__.keys())
        yield cls.__bom_map__[code]
        for line in lines:
            yield line

    @classmethod
    def write_bom(cls, fp, code="utf8"):
        assert code in cls.__bom_map__.keys(), \
            "code must be in ({})".format(cls.__bom_map__.keys())
        fp.write(cls.__bom_map__[code])
        return fp

    @classmethod
    def encode_lines_item(cls, lines):
        return [[unicode_to_utf8(row) for row in line] for line in lines]

    @classmethod
    def data_to_records(cls, data, fields):
        """
        :params:
            raw_data:
                [{k1: v1, k2: v2}]
            fields:
                (
                    (key_name1, field_name1, default_value1),
                    (key_name2, field_name2, default_value2),
                )
        """
        return [f[1] for f in fields], \
            [[row.get(f[0], f[2])for f in fields] for row in data]

    @classmethod
    def records_to_file(cls, fields, records, filename):
        """
        :params:
            fields, records, filename
        :return:
            None
        """
        lines = [fields] + records
        with open(filename, "wb") as fp:
            cls.write_bom(fp)
            csv_writer = csv.writer(fp)
            csv_writer.writerows(cls.encode_lines_item(lines))

    @classmethod
    def fields_records_to_stream(cls, fields, records):
        """
        :params:
            fields, records
        :return:
            file-like-object
        """
        lines = [fields] + list(records) if fields else list(records)
        s = StringIO()
        cls.write_bom(s)
        csv_writer = csv.writer(s)
        csv_writer.writerows(cls.encode_lines_item(lines))
        s.seek(0)
        return s

    @classmethod
    def str_to_stream(cls, data):
        """将字符串转换为IO流."""
        s = StringIO()
        cls.write_bom(s)
        s.write(data)
        s.seek(0)
        return s

    @classmethod
    def data_to_stream(cls, fields_conf, data):
        """根据字段配置和字典列表数据生成文件流
        """
        fields, records = cls.data_to_records(data, fields_conf)
        return cls.fields_records_to_stream(fields, records)

    @classmethod
    def data_exclude_fields_to_stream(cls, fields_conf, data):
        """将去除标题的数据生成文件流."""
        records = cls.data_to_records(data, fields_conf)[1]
        return cls.fields_records_to_stream([], records)


def json_resp_to_csv(json_resp_path, output_path):
    content = None
    with open(json_resp_path, 'rb') as fp:
        content = fp.read()

    if not content:
        return

    resp = json.loads(content)
    records = resp['records']

    if len(records) == 0:
        print('records is empty.')

    fields = [(r, r, '') for r in records[0].keys()]

    fields, records = CsvHelper.data_to_records(records, fields)
    CsvHelper.records_to_file(fields, records, output_path)


if __name__ == "__main__":
    json_resp_to_csv(sys.argv[1], sys.argv[2])
