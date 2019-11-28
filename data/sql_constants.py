# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: sql_constants.py
date: 2019/11/27 12:57
Desc: 相关sql封装
"""


def address_on_hazard_sql(hazard_name):
    """重大风险清单：危险源关联的风险点sql"""
    return "SELECT a.address FROM t_b_address_info a " \
           "WHERE a.id IN (SELECT dar.address_id FROM t_b_danger_address_rel dar " \
           "INNER JOIN t_b_danger_source ds ON ds.id = dar.danger_id " \
           "WHERE ds.hazard_manage_id = (SELECT hm.id FROM t_b_hazard_manage hm WHERE hm.hazard_name = '{}') AND ds.ismajor = '1')".format(
        hazard_name.strip())


def manage_on_hazard_sql(hazard_name):
    """重大风险清单：危险源关联的管控措施sql"""
    return "select u.realname,mr.achieve_effect,mr.work_content FROM t_b_ds_manage_record mr " \
           "inner join t_b_danger_source ds on ds.id = mr.danger_id " \
           "inner join t_s_base_user u on u.id = mr.controller " \
           "inner join (select hm.hazard_name,ds1.id from t_b_hazard_manage hm inner join t_b_danger_source ds1 on ds1.hazard_manage_id= hm.id ) " \
           "hm1 on hm1.id = mr.danger_id WHERE hm1.hazard_name = '{}'".format(hazard_name.strip())


def detail_of_risk_sql(hazard_name):
    """重大风险清单：风险详情sql"""
    return "select CAST(ds.ye_recognize_time as CHAR) as 辨识时间,ds.ye_mhazard_desc as 隐患描述,profess.typename as 专业,hm.hazard_name as 危险源名称," \
           "tba.activity_name as 作业活动,ds.ye_possibly_hazard as 风险描述,riskgrade.typename as 风险等级,hazardcate.typename as 风险类型," \
           "ds.doc_source as 管控标准来源,ds.section_name as 章节条款,ds.ye_standard as 标准内容,ds.manage_measure as 管控措施,pm.post_name as 责任岗位," \
           "ds.fine_money as 罚款金额 from t_b_danger_source ds " \
           "inner join (select tsy.typename,tsy.typecode from t_s_type tsy left join t_s_typegroup tsp on tsy.typegroupid=tsp.id " \
           "where tsp.typegroupcode='proCate_gradeControl') profess on profess.typecode = ds.ye_profession " \
           "inner join t_b_hazard_manage hm ON hm.id = ds.hazard_manage_id inner join t_b_activity_manage tba on tba.id = ds.activity_id " \
           "inner join (select tsy.typename,tsy.typecode from t_s_type tsy left join t_s_typegroup tsp on tsy.typegroupid=tsp.id " \
           "where tsp.typegroupcode='riskLevel') riskgrade on riskgrade.typecode = ds.ye_risk_grade " \
           "inner join (select tsy.typename,tsy.typecode from t_s_type tsy left join t_s_typegroup tsp on tsy.typegroupid=tsp.id " \
           "where tsp.typegroupcode='hazardCate') hazardcate on hazardcate.typecode = ds.ye_hazard_cate inner join t_b_post_manage pm " \
           "on pm.id = ds.post_id where ds.ismajor = 1 and hm.hazard_name = '{}' and ds.is_delete = '0' and ds.origin = '2';".format(
        hazard_name.strip())


def damage_type_code_sql(hazard_name):
    """查询风险对应的伤害类别编号代码"""
    return "SELECT ds.damage_type FROM t_b_danger_source ds INNER JOIN t_b_hazard_manage hm ON hm.id = ds.hazard_manage_id " \
           "WHERE ds.ismajor = '1' and ds.is_delete = '0' and hm.hazard_name = '{}'".format(hazard_name.strip())


def damage_type_value_sql(damage_type_code):
    """查询风险对应的伤害类别"""
    return "select tsy.typename from t_s_type tsy left join t_s_typegroup tsp on tsy.typegroupid=tsp.id " \
           "where tsp.typegroupcode='danger_Category' and tsy.typecode in {}".format(damage_type_code)


def ye_accident_code_sql(hazard_name):
    """风险对应的事故类型代码"""
    return "SELECT ds.ye_accident FROM t_b_danger_source ds INNER JOIN t_b_hazard_manage hm ON hm.id = ds.hazard_manage_id " \
           "WHERE ds.ismajor = '1' and ds.is_delete = '0' and hm.hazard_name = '{}';".format(hazard_name.strip())


def ye_accident_value_sql(accident_code):
    """风险对应的事故类型"""
    return "select tsy.typename from t_s_type tsy left join t_s_typegroup tsp on tsy.typegroupid=tsp.id " \
           "where tsp.typegroupcode='accidentCate' and tsy.typecode in {}".format(accident_code)


def risk_level_value_sql(hazard_name):
    """风险对应隐患等级"""
    return """select tsy.typename from t_s_type tsy
              left join t_s_typegroup tsp on tsy.typegroupid=tsp.id
              INNER JOIN (SELECT ds.hidden_level from t_b_danger_source ds LEFT JOIN t_b_hazard_manage hm ON hm.id = ds.hazard_manage_id
              where ds.ismajor = '1' and ds.is_delete = '0' and ds.origin = '2' and hm.hazard_name = '{}') leve on leve.hidden_level = tsy.typecode
              where tsp.typegroupcode='hiddenLevel'""".format(hazard_name.strip())


def depart_on_address(address):
    """风险点关联的责任部门"""
    return "select dep.departname from t_b_address_depart_rel adr1 inner join t_s_depart dep on adr1.depart_id = dep.ID " \
           "inner join t_b_address_info a on a.id = adr1.address_id WHERE a.address='{}'".format(address.strip())


def hazard_on_address(address):
    """风险点关联的危险源"""
    return "SELECT hm.hazard_name from t_b_danger_address_rel dar inner join t_b_danger_source ds on ds.id= dar.danger_id " \
           "inner join t_b_address_info a on a.id = dar.address_id inner join t_b_hazard_manage hm on hm.id = ds.hazard_manage_id " \
           "WHERE a.address = '{}';".format(address.strip())


def risk_on_address(address):
    """风险点关联风险数据"""
    return "SELECT p.typename,ds.ye_mhazard_desc from t_b_danger_source ds inner join t_b_danger_address_rel dar  on ds.id = dar.danger_id " \
           "inner join t_b_address_info a on a.id = dar.address_id inner JOIN (select t.typecode, t.typename FROM t_s_type t " \
           "INNER JOIN t_s_typegroup tg on tg.id = t.typegroupid WHERE tg.typegroupcode = 'proCate_gradeControl') p on p.typecode = ds.ye_profession " \
           "WHERE a.address = '{}'".format(address.strip())
