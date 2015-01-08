# coding:utf-8
__author__ = 'shenshen'

import os
import sys
import sqlitedb
import math


def txt2sqlite(txt_name, db_name, table_name, cml_status):
    #create database
    conn = sqlitedb.get_conn(db_name)
    create_table_sql = '''create table %s(id integer primary key,
        vehid integer not null, time real, accel real,
        desv real, dv real, vel real,
        x real, y real, z real);''' % (table_name,)
    sqlitedb.create_table(conn, create_table_sql)
    insert_flag = '''INSERT INTO %s (id, vehid) values (?, ?)''' % (table_name,)
    insert_rec = '''INSERT INTO %s values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''' % (table_name,)
    create_index_sql = '''create index record_id on %s(id)''' % (table_name,)
    cur = sqlitedb.get_cursor(conn)

    with open(txt_name, 'r') as fp:
        buffer = []
        last_time = 0
        rec_indx = 1
        for index, line in enumerate(fp):
            if index < 18:
                continue

            print('converting %d...' % index)
            items = ''.join(line.strip(' ')).split(';')
            time = float(items[0])
            vehid = int(items[1])
            accl = float(items[2])
            desv = float(items[3])
            dv = float(items[4])
            vel = float(items[5])
            x = float(items[6])
            y = float(items[7])
            z = float(items[8])
            data = [vehid, time, accl, desv, dv, vel, x, y, z]

            if index == 18:
                buffer.append(data)
                last_time = time
                continue

            if math.fabs(time - last_time) <= 1e-6:
                buffer.append(data)
                continue
            else:
                # 插入标记行
                sqlitedb.insert_one(conn, insert_flag, [rec_indx, len(buffer)])
                rec_indx += 1
                # 插入数据行
                for i in buffer:
                    i.insert(0, rec_indx)
                    rec_indx += 1
                sqlitedb.insert_many(conn, insert_rec, buffer)
                buffer = []
                buffer.append(data)
                last_time = time
        else:
            # 插入标记行
            sqlitedb.insert_one(conn, insert_flag, [rec_indx, len(buffer)])
            rec_indx += 1
            # 插入数据行
            for i in buffer:
                i.insert(0, rec_indx)
                rec_indx += 1
            sqlitedb.insert_many(conn, insert_rec, buffer)

    cur.execute(create_index_sql)
    conn.commit()
    print('finish!!!')


if __name__ == '__main__':
    # txt_path = sys.argv[1]
    # db_path = sys.argv[2]
    # table_name = sys.argv[3]
    # txt2sqlite(txt_path, db_path, table_name, True)
    txt2sqlite('test1.fzp', '../system/data.db', 'trafficsim', True)