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
           "on pm.id = ds.post_id where ds.ismajor = 1 and hm.hazard_name = '{}' and ds.is_delete = '0' and ds.origin = '2';".format(hazard_name.strip())


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


def detail_of_vio_sql(vio_date, vio_address, vio_unit, vio_desc):
    """
    三违详情查询sql
    :param vio_date: 三违时间
    :param vio_address: 三违地点
    :param vio_unit: 违章单位
    :param vio_desc: 三违描述内容
    :return:
    """
    return """SELECT CAST(three.vio_date as CHAR) AS 违章时间,address.address AS 违章地点,three.vio_people AS 违章人员,qualitative.typename AS 违章定性,
    three.stop_people AS 制止人,tsd.departname AS 违章单位,category.typename AS 违章分类,level1.typename AS 三违级别,tsd1.departname AS 查处单位,
    three.vio_fact_desc AS 三违事实描述,three.remark AS 备注 FROM t_b_three_violations three INNER JOIN t_b_address_info address ON address.id = three.vio_address 
    INNER JOIN (SELECT tst.typecode,tst.typename FROM t_s_type tst INNER JOIN t_s_typegroup tsg ON tsg.id = tst.typegroupid WHERE tsg.typegroupname = '违章定性') 
    qualitative ON qualitative.typecode = three.vio_qualitative INNER JOIN t_s_depart tsd ON tsd.id = three.vio_units LEFT JOIN t_s_depart tsd1 ON 
    tsd1.id = three.find_units INNER JOIN (SELECT tst.typecode,tst.typename FROM t_s_type tst INNER JOIN t_s_typegroup tsg ON tsg.id = tst.typegroupid  
    WHERE tsg.typegroupname = '违章分类') category ON category.typecode = three.vio_category INNER JOIN (SELECT tst.typecode,tst.typename FROM t_s_type tst 
    INNER JOIN t_s_typegroup tsg ON tsg.id = tst.typegroupid WHERE tsg.typegroupname = '三违级别') level1 ON level1.typecode = three.vio_level 
    WHERE three.vio_date LIKE '{_date}%' AND address.address = '{_address}'AND tsd.departname = '{_unit}'AND three.vio_fact_desc = '{_desc}'""" \
        .format(**{"_date": vio_date, "_address": vio_address, '_unit': vio_unit, '_desc': vio_desc})


def detail_of_hidden_sql(hidden_desc, exam_type, exam_date, **kwargs):
    """
    隐患详情查询sql
    :param hidden_desc: 隐患描述内容
    :param exam_type: 检查类型
    :param exam_date: 检查时间
    :param kwargs: 其他参数，比如责任单位/检查人。可为空
    :return:
    """

    global _kw_not_none, _kw_none
    from common.mysql_operation import ConnMysql
    # 先获取隐患整改方式
    if not kwargs:
        deal_type = ConnMysql().get_info(get_deal_type_sql(hidden_desc=hidden_desc, exam_type=exam_type, exam_date=exam_date))
    else:
        deal_type = ConnMysql().get_info(get_deal_type_sql(hidden_desc=hidden_desc, exam_type=exam_type, exam_date=exam_date, kwargs=kwargs[list(kwargs)[0]]))

    limit_param = "cast(hd.limit_date as CHAR) as 限期日期,"
    current_param = "reviewman.realname as 复查人,"

    _tem_sql_1 = "SELECT examtype1.typename as 检查类型,CAST(hd.exam_date as CHAR) as 检查时间,shift1.typename as 班次,ai.address as 地点,examman.realname AS 检查人," \
                 "tsd.departname as 责任单位,hd.duty_man as 责任人,category1.typename as 隐患类别,hid.typename as 隐患等级,category.typename as 隐患类型,"

    _tem_sql_2 = "hd.problem_desc as 问题描述 FROM t_b_hidden_danger_exam hd INNER JOIN t_b_address_info ai ON ai.id = hd.address left join t_s_depart tsd " \
                 "on hd.duty_unit=tsd.id left join(select tsy.typename,tsy.typecode from t_s_type tsy left join t_s_typegroup tsp on tsy.typegroupid=tsp.id " \
                 "where tsp.typegroupname='问题分类') examtype1 on examtype1.typecode=hd.exam_type left join(select tsy.typename,tsy.typecode from t_s_type tsy " \
                 "left join t_s_typegroup tsp on tsy.typegroupid=tsp.id where tsp.typegroupname='班次') shift1 on shift1.typecode=hd.shift " \
                 "left join(select tsy.typename,tsy.typecode from t_s_type tsy left join t_s_typegroup tsp on tsy.typegroupid=tsp.id " \
                 "where tsp.typegroupname='隐患类别') category1 on category1.typecode=hd.hidden_category left join (SELECT bu.realname,bu.id " \
                 "FROM t_s_base_user bu) examman ON examman.id = hd.fill_card_manids LEFT JOIN (SELECT tsy.typename,tsy.typecode FROM t_s_type tsy " \
                 "LEFT JOIN t_s_typegroup tsp ON tsy.typegroupid = tsp.id WHERE tsp.typegroupcode = 'hiddenType')category ON category.typecode = hd.hidden_type " \
                 "left join (SELECT bu.realname,bu.id FROM t_s_base_user bu)reviewman " \
                 "ON reviewman.id = hd.review_man left join(select tsy.typename,tsy.typecode from t_s_type tsy left join t_s_typegroup tsp " \
                 "on tsy.typegroupid=tsp.id where tsp.typegroupcode='hiddenLevel') hid on hid.typecode = hd.hidden_nature "

    if deal_type == '1':  # 限时整改
        if kwargs:
            if 'depart' in kwargs[list(kwargs)[0]]:  # 隐患整改
                _kw_not_none = "WHERE hd.problem_desc = '{}' AND hd.exam_type = (SELECT tsp.typecode FROM t_s_type tsp WHERE tsp.typename = '{}') " \
                               "AND hd.exam_date LIKE '{}%' and tsd.departname='{}'".format(hidden_desc, exam_type, exam_date, kwargs[list(kwargs)[0]][7:])
            if 'check' in kwargs[list(kwargs)[0]]:  # 隐患复查
                _kw_not_none = "WHERE hd.problem_desc = '{}' AND hd.duty_unit = (SELECT tsp.id FROM t_s_depart tsp WHERE tsp.departname = '{}') " \
                               "AND hd.exam_date LIKE '{}%' and examman.realname='{}'".format(hidden_desc, exam_type, exam_date, kwargs[list(kwargs)[0]][6:])
            return _tem_sql_1 + limit_param + _tem_sql_2 + _kw_not_none
        else:
            _kw_none = "WHERE hd.problem_desc = '{}' AND hd.exam_type =(SELECT tsp.typecode FROM t_s_type tsp WHERE tsp.typename = '{}')AND hd.exam_date " \
                       "LIKE '{}%'".format(hidden_desc, exam_type, exam_date)
            return _tem_sql_1 + limit_param + _tem_sql_2 + _kw_none

    if deal_type == '2':  # 现场处理
        if kwargs:
            if 'depart' in kwargs[list(kwargs)[0]]:  # 隐患整改
                _kw_not_none = "WHERE hd.problem_desc = '{}' AND hd.exam_type = (SELECT tsp.typecode FROM t_s_type tsp WHERE tsp.typename = '{}') " \
                               "AND hd.exam_date LIKE '{}%' and tsd.departname='{}'".format(hidden_desc, exam_type, exam_date, kwargs[list(kwargs)[0]])
            if 'check' in kwargs[list(kwargs)[0]]:  # 隐患复查
                _kw_not_none = "WHERE hd.problem_desc = '{}' AND hd.duty_unit = (SELECT tsp.id FROM t_s_depart tsp WHERE tsp.departname = '{}') " \
                               "AND hd.exam_date LIKE '{}%' and examman.realname='{}'".format(hidden_desc, exam_type, exam_date, kwargs[list(kwargs)[0]])
            return _tem_sql_1 + current_param + _tem_sql_2 + _kw_not_none
        else:
            _kw_none = "WHERE hd.problem_desc = '{}' AND hd.exam_type =(SELECT tsp.typecode FROM t_s_type tsp WHERE tsp.typename = '{}')AND hd.exam_date " \
                       "LIKE '{}%'".format(hidden_desc, exam_type, exam_date)
            return _tem_sql_1 + current_param + _tem_sql_2 + _kw_none


def get_deal_type_sql(hidden_desc, exam_type, exam_date, **kwargs):
    """
    查询隐患数据的处理状态,kwargs参数中主要是判断是否包含责任单位或者检查人
    :param hidden_desc: 隐患描述内容
    :param exam_type: 检查类型
    :param exam_date: 检查时间
    :param kwargs: 其他参数，比如责任单位/检查人。可为空
    :return:
    """
    if not kwargs:  # 不包含责任单位 隐患录入时使用
        return "select hd.deal_type from t_b_hidden_danger_exam hd where hd.problem_desc = '{}' AND hd.exam_type = ( SELECT tsp.typecode FROM t_s_type tsp " \
               "WHERE tsp.typename = '{}' ) AND hd.exam_date LIKE '{}%'".format(hidden_desc, exam_type, exam_date)
    else:
        if 'depart' in kwargs[list(kwargs)[0]]:  # 隐患整改使用
            return "select hd.deal_type from t_b_hidden_danger_exam hd INNER join t_s_depart d on d.id = hd.duty_unit where hd.problem_desc = '{}' " \
                   "AND hd.exam_type = (SELECT tsp.typecode FROM t_s_type tsp WHERE tsp.typename = '{}' ) AND hd.exam_date LIKE '{}%' " \
                   "and d.departname = '{}';".format(hidden_desc, exam_type, exam_date, kwargs[list(kwargs)[0]][7:])
        if 'check' in kwargs[list(kwargs)[0]]:  # 包含检查人，隐患复查使用
            return "SELECT d.deal_type FROM t_b_hidden_danger_exam d INNER JOIN t_s_base_user u on u.id = d.fill_card_manids INNER JOIN " \
                   "(SELECT tsp.id FROM t_s_depart tsp WHERE tsp.departname = '{}' ) type ON type.id = d.duty_unit WHERE d.exam_date LIKE '{}%' " \
                   "AND d.problem_desc = '{}' AND u.realname = '{}'".format(exam_type, exam_date, hidden_desc, kwargs[list(kwargs)[0]][6:])


def get_hazard_name_of_danger_sql():
    """获取重大风险清单中危险源名称"""
    return "select d.hazard_name from t_b_hazard_manage d INNER JOIN t_b_danger_source ds on d.id = ds.hazard_manage_id where ds.ismajor = '1';"


def danger_address_rel_sql():
    """风险与风险点关系：存在关联风险的地点"""
    return "SELECT distinct a.address FROM t_b_address_info a INNER JOIN t_b_danger_address_rel da on da.address_id = a.id"


if __name__ == '__main__':
    print(detail_of_hidden_sql(hidden_desc='现场', exam_type='矿领导带班', exam_date='2019-11-29', examUnit='x'))
