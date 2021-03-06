# -*- coding: utf8 -*-
import os
import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine, inspect, or_, update


import datetime as dt
from config import Config
from model import Khung_gia_uy_ban, Data_MB, Data_chung_cu, BDS_biet_thu, Yeu_to, Mat_tien, Quy_mo, Hinh_dang, Do_rong_ngo, Khoang_cach_truc, Dac_diem_VT, User_SM, ID_auto, Id_ticket, Id_ticket_BT, Id_ticket_CC, Id_ticket_quy_hoach,Event_log, Quy_hoach, Loai_nha, Nam_su_dung, ROA_tho_cu, ROA_chung_cu, ROA_biet_thu, app, db

from Setting import *

app.config.from_object(Config)

app.secret_key = os.urandom(24)
app.permanent_session_lifetime = dt.timedelta(minutes=900)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:   
            return f(*args, **kwargs)            
        else:
            return redirect(url_for('login'))
    return wrap



def changepass_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['changepass'] == True:   
            return f(*args, **kwargs)            
        else:
            return redirect(url_for('changepass'))
    return wrap


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['role'] == 'Admin':   
            return f(*args, **kwargs)
        else:
            return redirect(url_for('home'))
    return wrap


@app.route('/ajax_get_dac_diem_vi_tri',methods=['GET', 'POST'])
def ajax_get_dac_diem_vi_tri():
    tinh_thanh = request.args['tinh_thanh']
    vi_tri = request.args['vi_tri']
    
    mien = db.session.query(Data_MB.Mien).filter_by(Tinh_thanh = tinh_thanh).distinct().all()[0][0]

    if mien == 'MB':
        yeu_to_loi_the = [r[0] for r in db.session.query(Yeu_to.yeu_to).filter_by(mien = mien, phan_loai = 'LT').distinct().order_by(Yeu_to.yeu_to.asc()).all()]

        yeu_to_bat_loi = [r[0] for r in db.session.query(Yeu_to.yeu_to).filter_by(mien = mien, phan_loai = 'BL').distinct().order_by(Yeu_to.yeu_to.asc()).all()]

    elif mien in ('MN', 'MN1'):
        yeu_to_loi_the = [r[0] for r in db.session.query(Yeu_to.yeu_to).filter_by(mien = mien, vi_tri = vi_tri, phan_loai = 'LT').distinct().order_by(Yeu_to.yeu_to.asc()).all()]
        
        yeu_to_bat_loi = [r[0] for r in db.session.query(Yeu_to.yeu_to).filter_by(mien = mien, vi_tri = vi_tri, phan_loai = 'BL').distinct().order_by(Yeu_to.yeu_to.asc()).all()]

    result = [r[0] for r in db.session.query(Dac_diem_VT.dac_diem).filter_by(thanh_pho = tinh_thanh, vi_tri = vi_tri).distinct().order_by(Dac_diem_VT.dac_diem.asc()).all()]

    return jsonify({'result' : result, 'loi_the' : yeu_to_loi_the, 'bat_loi' : yeu_to_bat_loi})


# -------------- BDS BIET THU --------------
@app.route('/ajax_get_option_ten_duong_biet_thu',methods=['GET', 'POST'])
def ajax_get_option_ten_duong_biet_thu():
    ten_du_an = request.args['ten_du_an']
    result = [r[0] for r in db.session.query(BDS_biet_thu.ten_duong).filter_by(ten_du_an = ten_du_an).distinct().order_by(BDS_biet_thu.ten_duong.asc()).all()]
    dia_chi = db.session.query(BDS_biet_thu.dia_chi).filter_by(ten_du_an = ten_du_an).first()
    return jsonify({'result':result, 'dia_chi' : dia_chi})


@app.route('/ajax_get_option_tang_biet_thu',methods=['GET', 'POST'])
def ajax_get_option_tang_biet_thu():
    ten_du_an = request.args['ten_du_an']
    ten_duong = request.args['ten_duong']

    result = [r[0] for r in db.session.query(BDS_biet_thu.ten_tang).filter_by(ten_du_an = ten_du_an, ten_duong = ten_duong).distinct().order_by(BDS_biet_thu.ten_tang.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_option_ma_biet_thu',methods=['GET', 'POST'])
def ajax_get_option_ma_biet_thu():
    ten_du_an = request.args['ten_du_an']
    ten_duong = request.args['ten_duong']
    ten_tang = request.args['ten_tang']

    result = [r[0] for r in db.session.query(BDS_biet_thu.ma_can).filter_by(ten_du_an = ten_du_an, ten_duong = ten_duong, ten_tang = ten_tang).distinct().order_by(BDS_biet_thu.ma_can.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_option_gia_biet_thu',methods=['GET', 'POST'])
def ajax_get_option_gia_biet_thu():
    ten_du_an = request.args['ten_du_an']
    ten_duong = request.args['ten_duong']
    ten_tang = request.args['ten_tang']
    ma_can = request.args['ma_can']

    result = db.session.query(BDS_biet_thu.dien_tich_dat, BDS_biet_thu.dien_tich_san_xay_dung, BDS_biet_thu.tong_gia_tri_xay_tho, BDS_biet_thu.tong_gia_tri_hoan_thien, BDS_biet_thu.don_gia_dat, BDS_biet_thu.don_gia_ctxd).filter_by(ten_du_an = ten_du_an, ten_duong = ten_duong, ten_tang = ten_tang, ma_can = ma_can).distinct().all()[0]


    dien_tich_dat_raw = result.dien_tich_dat
    dien_tich_san_xay_dung_raw = result.dien_tich_san_xay_dung
    tong_gia_tri_xay_tho_raw = result.tong_gia_tri_xay_tho
    tong_gia_tri_hoan_thien_raw = result.tong_gia_tri_hoan_thien
    don_gia_dat_raw = result.don_gia_dat
    don_gia_ctxd_raw = result.don_gia_ctxd

    dia_chi = db.session.query(BDS_biet_thu.dia_chi).filter_by(ten_du_an = ten_du_an).first()
    # NEW TICKET
    dia_chi_cu_the = ma_can + ", " + ten_tang + ", " + ten_duong + ", " + ten_du_an 
    du_lieu_nhap = "|>TT 1|" + str(dia_chi_cu_the) + "*|*"
    dien_tich_dat = "|>KQ 3|" + str(result.dien_tich_dat) + "*|*"
    dien_tich_san_xay_dung = "|>KQ 4|" + str(result.dien_tich_san_xay_dung) + "*|*"
    tong_gia_tri_xay_tho = "|>KQ 5|" + str(result.tong_gia_tri_xay_tho) + "*|*"
    tong_gia_tri_hoan_thien = "|>KQ 6|" + str(result.tong_gia_tri_hoan_thien) + "*|*"
    don_gia_dat = "|>KQ 7|" + str(result.don_gia_dat) + "*|*"
    don_gia_ctxd = "|>KQ 8|" + str(result.don_gia_ctxd) + "*|*"
    ket_qua = dien_tich_dat + dien_tich_san_xay_dung + tong_gia_tri_xay_tho + tong_gia_tri_hoan_thien + don_gia_dat + don_gia_ctxd

    ngay_khoi_tao = dt.datetime.now()
    new_id = ID_auto_create()
    new_ticket = Id_ticket_BT(
                new_id,
                dia_chi_cu_the,
                result.dien_tich_dat,
                result.dien_tich_san_xay_dung,
                result.don_gia_dat,
                result.don_gia_ctxd,
                result.tong_gia_tri_xay_tho,
                result.tong_gia_tri_hoan_thien,
                session['username'],
                ngay_khoi_tao,
                dia_chi[0]
            )

    db.session.add(new_ticket)
    db.session.commit()

    # EVENT LOG
    event_log = Event_log(new_id, session['username'], ngay_khoi_tao, 'bds_biet_thu', du_lieu_nhap, ket_qua)
    db.session.add(event_log)
    db.session.commit()
    return jsonify({
                    'result':result,
                    'dia_chi' : dia_chi,
                    'ten_du_an' : ten_du_an,
                    'ten_duong' : ten_duong,
                    'ten_tang' : ten_tang,
                    'ma_can' : ma_can,
                    'ngay_khoi_tao' : ngay_khoi_tao,
                    'new_id' : new_id,
                    'dien_tich_dat' : dien_tich_dat_raw,
                    'dien_tich_san_xay_dung' : dien_tich_san_xay_dung_raw,
                    'tong_gia_tri_xay_tho' : tong_gia_tri_xay_tho_raw,
                    'tong_gia_tri_hoan_thien' : tong_gia_tri_hoan_thien_raw,
                    'don_gia_dat' : don_gia_dat_raw,
                    'don_gia_ctxd' : don_gia_ctxd_raw,
                    })


# -------------- BDS CAN HO ----------------
@app.route('/ajax_get_option_du_an_can_ho',methods=['GET', 'POST'])
def ajax_get_option_du_an_can_ho():
    ten_du_an = request.args['ten_du_an']
    result = [r[0] for r in db.session.query(Data_chung_cu.ten_toa_duong_day_khu).filter_by(ten_du_an = ten_du_an).distinct().order_by(Data_chung_cu.ten_toa_duong_day_khu.asc()).all()]
    dia_chi = db.session.query(Data_chung_cu.dia_chi).filter_by(ten_du_an = ten_du_an).first()
    return jsonify({'result' : result, 'dia_chi' : dia_chi})


@app.route('/ajax_get_option_tang_can_ho',methods=['GET', 'POST'])
def ajax_get_option_tang_can_ho():
    ten_du_an = request.args['ten_du_an']
    ten_toa_nha = request.args['ten_toa_nha']


    list_1 = [r[0] for r in db.session.query(Data_chung_cu.ten_tang_loai_nha).filter_by(ten_du_an = ten_du_an, ten_toa_duong_day_khu = ten_toa_nha).distinct().order_by(Data_chung_cu.ten_tang_loai_nha.asc()).all()]
    print(list_1)
    result = sorted([r if 'A' not in r and 'B' not in r and ',' not in r  and r != '' else 0 if r == '' else r for r in list_1], key=lambda x: int(str(x).split("A")[0].split("B")[0].split(",")[0]))

    # result = sorted(list_1)

    return jsonify({'result':result})


@app.route('/ajax_get_option_ma_can_ho',methods=['GET', 'POST'])
def ajax_get_option_ma_can_ho():
    ten_du_an = request.args['ten_du_an']
    ten_toa_nha = request.args['ten_toa_nha']
    so_tang = request.args['so_tang']

    result = [r[0] for r in db.session.query(Data_chung_cu.ma_can).filter_by(ten_du_an = ten_du_an, ten_toa_duong_day_khu = ten_toa_nha, ten_tang_loai_nha = so_tang).distinct().order_by(Data_chung_cu.ma_can.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_option_gia_can_ho',methods=['GET', 'POST'])
def ajax_get_option_gia_can_ho():
    ten_du_an = request.args['ten_du_an']
    ten_toa_nha = request.args['ten_toa_nha']
    so_tang = request.args['so_tang']
    ma_can = request.args['ma_can']

    result = db.session.query(Data_chung_cu.dien_tich, Data_chung_cu.loai_dien_tich ,Data_chung_cu.don_gia).filter_by(ten_du_an = ten_du_an, ten_toa_duong_day_khu = ten_toa_nha, ten_tang_loai_nha = so_tang, ma_can = ma_can).distinct().order_by(Data_chung_cu.ma_can.asc()).all()[0]
    dia_chi = db.session.query(Data_chung_cu.dia_chi).filter_by(ten_du_an = ten_du_an).first()
    tong_gia = float(result[0])*float(result[2])

    dien_tich = "|>KQ 9|" + str(result.dien_tich) + "*|*"
    loai_dien_tich = "|>KQ 10|" + str(result.loai_dien_tich) + "*|*"
    don_gia = "|>KQ 11|" + str(result.don_gia) + "*|*"
    tong_gia_log = "|>KQ 12|" + str(tong_gia) + "*|*"
    dia_chi_cu_the = ma_can + ", " + so_tang + ", " + ten_toa_nha + ", " + ten_du_an 
    du_lieu_nhap = "|>TT 1|" + str(dia_chi_cu_the) + "*|*"
    ket_qua = dien_tich + loai_dien_tich + don_gia + tong_gia_log

    # NEW TICKET
    ngay_khoi_tao = dt.datetime.now()
    new_id = ID_auto_create()
    new_ticket = Id_ticket_CC(
                new_id,
                dia_chi_cu_the,
                result.dien_tich,
                result.loai_dien_tich,
                result.don_gia,
                tong_gia,
                session['username'],
                ngay_khoi_tao,
                dia_chi[0]
            )

    db.session.add(new_ticket)
    db.session.commit()

    # EVENT LOG
    event_log = Event_log(new_id, session['username'], ngay_khoi_tao, 'bds_chung_cu', du_lieu_nhap, ket_qua)
    db.session.add(event_log)
    db.session.commit()
    return jsonify({
                    'result':result,
                    'tong_gia' : tong_gia,
                    'dia_chi' : dia_chi,
                    'ten_du_an' : ten_du_an,
                    'ten_toa_nha' : ten_toa_nha,
                    'so_tang' : so_tang,
                    'ma_can' : ma_can,
                    'ngay_khoi_tao' : ngay_khoi_tao,
                    'new_id' : new_id,
                    })


# ---------------GET OPTION UY BAN-------------
@app.route('/ajax_get_option_quan_huyen_uy_ban',methods=['GET', 'POST'])
def ajax_get_option_quan_huyen_uy_ban():
    tinh_thanh = request.args['tinh_thanh']
    result = [r[0] for r in db.session.query(Khung_gia_uy_ban.quan_huyen).filter_by(thanh_pho = tinh_thanh).distinct().order_by(Khung_gia_uy_ban.quan_huyen.asc()).all()]

    return jsonify({'result' : result})


@app.route('/ajax_get_option_duong_pho_uy_ban',methods=['GET', 'POST'])
def ajax_get_option_duong_pho_uy_ban():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    result = [r[0] for r in db.session.query(Khung_gia_uy_ban.tuyen_duong).filter_by(thanh_pho = tinh_thanh, quan_huyen = quan_huyen).distinct().order_by(Khung_gia_uy_ban.tuyen_duong.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_option_tuyen_duong_uy_ban',methods=['GET', 'POST'])
def ajax_get_option_tuyen_duong_uy_ban():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']
    result = [r[0] for r in db.session.query(Khung_gia_uy_ban.doan_tu_den).filter_by(thanh_pho = tinh_thanh, quan_huyen = quan_huyen, tuyen_duong = ten_duong).distinct().order_by(Khung_gia_uy_ban.doan_tu_den.asc()).all()]

    value = db.session.query(Khung_gia_uy_ban.VT1, Khung_gia_uy_ban.VT2, Khung_gia_uy_ban.VT3, Khung_gia_uy_ban.VT4, Khung_gia_uy_ban.VT5).filter_by(thanh_pho = tinh_thanh, quan_huyen = quan_huyen, tuyen_duong = ten_duong).distinct().all()[0]
    return jsonify({'result' : result, 'value' : value})


@app.route('/ajax_get_option_vi_tri_bds_uy_ban',methods=['GET', 'POST'])
def ajax_get_option_vi_tri_bds_uy_ban():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']
    tuyen_duong = request.args['tuyen_duong']

    result = db.session.query(Khung_gia_uy_ban.VT1, Khung_gia_uy_ban.VT2, Khung_gia_uy_ban.VT3, Khung_gia_uy_ban.VT4, Khung_gia_uy_ban.VT5).filter_by(thanh_pho = tinh_thanh, quan_huyen = quan_huyen, tuyen_duong = ten_duong, doan_tu_den = tuyen_duong).distinct().all()[0]

    return jsonify({'result':result})



# --------------THONG TIN QUY HOACH------------------
@app.route('/ajax_get_option_quan_huyen_quy_hoach',methods=['GET', 'POST'])
def ajax_get_option_quan_huyen_quy_hoach():
    thanh_pho = request.args['thanh_pho']
    result = [r[0] for r in db.session.query(Quy_hoach.quan).filter_by(thanh_pho = thanh_pho).distinct().order_by(Quy_hoach.quan.asc()).all()]
    return jsonify({'result' : result})


@app.route('/ajax_get_option_duong_pho_quy_hoach',methods=['GET', 'POST'])
def ajax_get_option_duong_pho_quy_hoach():
    thanh_pho = request.args['thanh_pho']
    quan_huyen = request.args['quan_huyen']

    result = [r[0] for r in db.session.query(Quy_hoach.duong).filter_by(thanh_pho = thanh_pho, quan = quan_huyen).distinct().order_by(Quy_hoach.duong.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_option_doan_duong_quy_hoach',methods=['GET', 'POST'])
def ajax_get_option_doan_duong_quy_hoach():
    thanh_pho = request.args['thanh_pho']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']

    result = [r[0] for r in db.session.query(Quy_hoach.doan_duong).filter_by(thanh_pho = thanh_pho, quan = quan_huyen, duong = ten_duong).distinct().order_by(Quy_hoach.doan_duong.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_thong_tin_quy_hoach', methods=['GET', 'POST'])
def ajax_get_thong_tin_quy_hoach():
    # DATA REQUEST
    thanh_pho = request.args['thanh_pho']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']
    doan_duong = request.args['doan_duong']

    # DATA RESULT
    result = db.session.query(Quy_hoach.quy_hoach_hien_huu, Quy_hoach.quy_hoach_moi, Quy_hoach.quy_hoach_thoat_lu, Quy_hoach.quy_hoach_cong_trinh).filter_by(thanh_pho = thanh_pho,quan = quan_huyen, duong = ten_duong, doan_duong = doan_duong).distinct().order_by(Quy_hoach.doan_duong.asc()).all()[0]
    ngay_khoi_tao = dt.datetime.now()
    new_id = ID_auto_create()
    dia_chi = doan_duong + ', ' + ten_duong + ', ' + quan_huyen + ', ' + thanh_pho
    quy_hoach_hien_huu = result.quy_hoach_hien_huu
    quy_hoach_moi = result.quy_hoach_moi
    quy_hoach_thoat_lu = result.quy_hoach_thoat_lu
    quy_hoach_cong_trinh = result.quy_hoach_cong_trinh
    ket_qua = quy_hoach_hien_huu + '*|*' + quy_hoach_moi + '*|*' + quy_hoach_thoat_lu + '*|*' + quy_hoach_cong_trinh

    count_quy_hoach_hien_huu = db.session.query(Quy_hoach.quy_hoach_hien_huu).filter_by(thanh_pho = thanh_pho,quan = quan_huyen).filter(Quy_hoach.quy_hoach_hien_huu != "Chưa xác định").count()
    count_quy_hoach_moi = db.session.query(Quy_hoach.quy_hoach_moi).filter_by(thanh_pho = thanh_pho,quan = quan_huyen).filter(Quy_hoach.quy_hoach_moi != "Chưa xác định").count()
    count_quy_hoach_thoat_lu = db.session.query(Quy_hoach.quy_hoach_thoat_lu).filter_by(thanh_pho = thanh_pho,quan = quan_huyen).filter(Quy_hoach.quy_hoach_thoat_lu != "Chưa xác định").count()
    count_quy_hoach_cong_trinh = db.session.query(Quy_hoach.quy_hoach_cong_trinh).filter_by(thanh_pho = thanh_pho,quan = quan_huyen).filter(Quy_hoach.quy_hoach_cong_trinh != "Chưa xác định").count()

    list_count_quy_hoach = [count_quy_hoach_hien_huu, count_quy_hoach_moi, count_quy_hoach_thoat_lu, count_quy_hoach_cong_trinh]

    count_all_quy_hoach = sum(list_count_quy_hoach)
    try:
        list_percent_quy_hoach = [
                             count_quy_hoach_hien_huu/count_all_quy_hoach*100,
                             count_quy_hoach_moi/count_all_quy_hoach*100,
                             count_quy_hoach_thoat_lu/count_all_quy_hoach*100,
                             count_quy_hoach_cong_trinh/count_all_quy_hoach*100
                             ]
    except:
        list_percent_quy_hoach = [0, 0, 0, 0]
    list_label = ["Quy hoạch mở đường " + "<br>" + " hiện hữu",
                "Quy hoạch " + "<br>" + "mở đường mới" ,
                "Quy hoạch hành lang " + "<br>" + " thoát lũ",
                "Quy hoạch liên quan đến " + "<br>" + " các công trình công cộng, " + "<br>" + " công trình Nhà nước"]
    dict_label_value = [{"label" : list_label[i], "value" : r} for i,r in enumerate(list_percent_quy_hoach) if r != 0]
    # NEW TICKET
    new_ticket = Id_ticket_quy_hoach(
                                    new_id,
                                    dia_chi,
                                    '',
                                    ket_qua,
                                    session['username'],
                                    ngay_khoi_tao
                                    )
    db.session.add(new_ticket)
    db.session.commit()

    # LOG
    event_log = Event_log(new_id, session['username'], ngay_khoi_tao, 'quy_hoach', dia_chi, ket_qua)
    db.session.add(event_log)
    db.session.commit()

    return jsonify({
                    'new_id' : new_id,
                    'ngay_khoi_tao' : ngay_khoi_tao,
                    'dia_chi' : dia_chi,
                    'quy_hoach_hien_huu' : quy_hoach_hien_huu,
                    'quy_hoach_moi' : quy_hoach_moi,
                    'quy_hoach_thoat_lu' : quy_hoach_thoat_lu,
                    'quy_hoach_cong_trinh' : quy_hoach_cong_trinh,
                    'list_percent_quy_hoach' : list_percent_quy_hoach,
                    'dict_label_value' : dict_label_value,
                    'thanh_pho' : thanh_pho,
                    'quan_huyen' : quan_huyen,
                    })



# -------------- BDS NHA THO CU ------------
@app.route('/ajax_get_option_quan_huyen',methods=['GET', 'POST'])
def ajax_get_option_quan_huyen():
    tinh_thanh = request.args['tinh_thanh']
    result = [r[0] for r in db.session.query(Data_MB.Quan).filter_by(Tinh_thanh = tinh_thanh).distinct().order_by(Data_MB.Quan.asc()).all()]

    mien = [r[0] for r in db.session.query(Data_MB.Mien).filter_by(Tinh_thanh = tinh_thanh).distinct().order_by(Data_MB.Mien.asc()).all()]
    return jsonify({'result' : result, 'mien' : mien})


@app.route('/ajax_get_option_duong_pho',methods=['GET', 'POST'])
def ajax_get_option_duong_pho():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']

    result = [r[0] for r in db.session.query(Data_MB.Duong).filter_by(Tinh_thanh = tinh_thanh, Quan = quan_huyen).distinct().order_by(Data_MB.Duong.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_option_tuyen_duong',methods=['GET', 'POST'])
def ajax_get_option_tuyen_duong():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']

    result = [r[0] for r in db.session.query(Data_MB.Doan_duong).filter_by(Tinh_thanh = tinh_thanh, Quan = quan_huyen, Duong = ten_duong).distinct().order_by(Data_MB.Doan_duong.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_option_vi_tri_bds',methods=['GET', 'POST'])
def ajax_get_option_vi_tri_bds():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']
    tuyen_duong = request.args['tuyen_duong']

    result = [r[0] for r in db.session.query(Data_MB.Vi_tri).filter_by(Tinh_thanh = tinh_thanh, Quan = quan_huyen, Duong = ten_duong, Doan_duong = tuyen_duong ) .distinct().order_by(Data_MB.Vi_tri.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_gia_uy_ban', methods=['GET', 'POST'])
def ajax_get_gia_uy_ban():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']
    tuyen_duong = request.args['tuyen_duong']
    vi_tri_bds = request.args['vi_tri_bds']
    
    result = db.session.query(Data_MB.Thong_tin_quy_hoach, Data_MB.Gia_thi_truong).filter_by(Tinh_thanh = tinh_thanh,Quan = quan_huyen, Duong = ten_duong, Doan_duong = tuyen_duong, Vi_tri = vi_tri_bds).distinct().order_by(Data_MB.Doan_duong.asc()).all()[0]

    return jsonify({'result' : result})


# ---------------- SEARCH TICKET ----------------
@app.route('/ajax_search_ticket', methods=['GET', 'POST'])
def ajax_search_ticket():
    id_ticket = request.args['id_ticket']
    phan_loai = db.session.query(Event_log.phan_loai).filter_by(id_ticket = id_ticket).all()[0].phan_loai

    if phan_loai == 'bds_tho_cu':
        result = db.session.query(Id_ticket.id_ticket, Id_ticket.dia_chi, Id_ticket.vi_tri, Id_ticket.dien_tich, Id_ticket.mat_tien, Id_ticket.hinh_dang, Id_ticket.do_rong_ngo, Id_ticket.kcach_truc_chinh, Id_ticket.yeu_to_loi_the, Id_ticket.yeu_to_bat_loi, Id_ticket.gia_truoc, Id_ticket.gia_sau, Id_ticket.loai_nha, Id_ticket.thoi_gian_su_dung, Id_ticket.don_gia_ctxd, Id_ticket.dien_tich_san_xd, Id_ticket.username, Id_ticket.time).filter_by(id_ticket = id_ticket).all()[0]
        thanh_pho = result.dia_chi.split(", ")[-1]
        vi_tri = result.vi_tri
        try:
            dac_diem_VT = db.session.query(Dac_diem_VT.dac_diem).filter_by(thanh_pho = thanh_pho, vi_tri = vi_tri).all()[0].dac_diem
        except:
            dac_diem_VT = ''
        return jsonify({'result' : result, 'phan_loai' : phan_loai, 'dac_diem_VT': dac_diem_VT})

    if phan_loai == 'quy_hoach':
        result = db.session.query(Id_ticket_quy_hoach.id_ticket, Id_ticket_quy_hoach.dia_chi, Id_ticket_quy_hoach.vi_tri, Id_ticket_quy_hoach.ket_qua, Id_ticket_quy_hoach.username, Id_ticket_quy_hoach.time).filter_by(id_ticket = id_ticket).all()[0]
        thanh_pho = result.dia_chi.split(", ")[-1]
        quan_huyen = result.dia_chi.split(", ")[-2]
        print(thanh_pho)
        print(quan_huyen)
        count_quy_hoach_hien_huu = db.session.query(Quy_hoach.quy_hoach_hien_huu).filter_by(thanh_pho = thanh_pho,quan = quan_huyen).filter(Quy_hoach.quy_hoach_hien_huu != "Chưa xác định").count()
        count_quy_hoach_moi = db.session.query(Quy_hoach.quy_hoach_moi).filter_by(thanh_pho = thanh_pho,quan = quan_huyen).filter(Quy_hoach.quy_hoach_moi != "Chưa xác định").count()
        count_quy_hoach_thoat_lu = db.session.query(Quy_hoach.quy_hoach_thoat_lu).filter_by(thanh_pho = thanh_pho,quan = quan_huyen).filter(Quy_hoach.quy_hoach_thoat_lu != "Chưa xác định").count()
        count_quy_hoach_cong_trinh = db.session.query(Quy_hoach.quy_hoach_cong_trinh).filter_by(thanh_pho = thanh_pho,quan = quan_huyen).filter(Quy_hoach.quy_hoach_cong_trinh != "Chưa xác định").count()

        list_count_quy_hoach = [count_quy_hoach_hien_huu, count_quy_hoach_moi, count_quy_hoach_thoat_lu, count_quy_hoach_cong_trinh]

        count_all_quy_hoach = sum(list_count_quy_hoach)
        try:
            list_percent_quy_hoach = [
                                 count_quy_hoach_hien_huu/count_all_quy_hoach*100,
                                 count_quy_hoach_moi/count_all_quy_hoach*100,
                                 count_quy_hoach_thoat_lu/count_all_quy_hoach*100,
                                 count_quy_hoach_cong_trinh/count_all_quy_hoach*100
                                 ]
        except:
            list_percent_quy_hoach = [0, 0, 0, 0]
        list_label = ["Quy hoạch mở đường " + "<br>" + " hiện hữu",
                    "Quy hoạch " + "<br>" + "mở đường mới" ,
                    "Quy hoạch hành lang " + "<br>" + " thoát lũ",
                    "Quy hoạch liên quan đến " + "<br>" + " các công trình công cộng, " + "<br>" + " công trình Nhà nước"]
        dict_label_value = [{"label" : list_label[i], "value" : r} for i,r in enumerate(list_percent_quy_hoach) if r != 0]        
        return jsonify({'result' : result, 'phan_loai' : phan_loai, 'dict_label_value' : dict_label_value})

    if phan_loai == 'bds_chung_cu':
        result = db.session.query(Id_ticket_CC.id_ticket, Id_ticket_CC.ten_du_an, Id_ticket_CC.dien_tich, Id_ticket_CC.loai_dien_tich, Id_ticket_CC.don_gia, Id_ticket_CC.tong_gia, Id_ticket_CC.username, Id_ticket_CC.time, Id_ticket_CC.dia_chi).filter_by(id_ticket = id_ticket).all()[0]

    if phan_loai == 'bds_biet_thu':
        result = db.session.query(Id_ticket_BT.id_ticket, Id_ticket_BT.ten_du_an, Id_ticket_BT.dien_tich_dat, Id_ticket_BT.dien_tich_san_xd, Id_ticket_BT.don_gia_dat, Id_ticket_BT.don_gia_ctxd, Id_ticket_BT.tong_gia_xay_tho, Id_ticket_BT.tong_gia_hoan_thien, Id_ticket_BT.username, Id_ticket_BT.time,  Id_ticket_BT.dia_chi).filter_by(id_ticket = id_ticket).all()[0]

    return jsonify({'result' : result, 'phan_loai' : phan_loai})


# GET RESULT
def he_so_dieu_chinh(value,percent):
    if percent == 0:
        return 0
    else:
        return float(value)*(1-float(percent))/float(percent)


# TINH HE SO DIEN TICH
def quy_mo(x, mien, vi_tri):
    if x == 0 or x == '':
        return 0
    if mien == 'MB':
        quy_mo_data = db.session.query(Quy_mo).filter_by(mien = mien).all()
    elif mien in ('MN', 'MN1'):
        quy_mo_data = db.session.query(Quy_mo).filter_by(mien = mien, vi_tri = vi_tri).all()


    for r in range(len(quy_mo_data)):
        data_0 = float(quy_mo_data[r].quy_mo)
        data_1 = float(quy_mo_data[r].ti_le)
        data_2 = float(quy_mo_data[r+1].ti_le)
        data_3 = float(quy_mo_data[r+1].quy_mo)
        data_4 = float(quy_mo_data[-1].quy_mo)
        data_5 = float(quy_mo_data[-1].ti_le)

        if x < data_0:
            return data_1
        elif x == data_0:
            return data_1
        elif data_0 < x < data_3:
            y = data_2 - (data_3 - x)*(data_2 - data_1)/(data_3 - data_0)
            return y
        elif x > data_4:
            return data_5


# HE SO MAT TIEN
def mat_tien(x, mien, vi_tri):
    if x == 0 or x == '':
        return 0
    if mien == 'MB':
        mat_tien_data = db.session.query(Mat_tien).filter_by(mien = mien).all()

    elif mien in ('MN', 'MN1'):
        mat_tien_data = db.session.query(Mat_tien).filter_by(mien = mien, vi_tri = vi_tri).all()


    for r in range(len(mat_tien_data)):
        if x < float(mat_tien_data[r].mat_tien):
            return mat_tien_data[r].ti_le
        elif x == float(mat_tien_data[r].mat_tien):
            return mat_tien_data[r].ti_le
        elif float(mat_tien_data[r].mat_tien) < x < float(mat_tien_data[r+1].mat_tien):
            y = float(mat_tien_data[r+1].ti_le) - ((float(mat_tien_data[r+1].mat_tien) - x)*(float(mat_tien_data[r+1].ti_le) - float(mat_tien_data[r].ti_le))/(float(mat_tien_data[r+1].mat_tien) - float(mat_tien_data[r].mat_tien))) 
            return y
        elif x > float(mat_tien_data[-1].mat_tien):
            return mat_tien_data[-1].ti_le


#DO RONG NGO
def do_rong_ngo(a, b, x, mien):
    x = float(x)
    if x == 0 or x == '':
        return 0
    do_rong_ngo_data = db.session.query(Do_rong_ngo).filter_by(Tinh_thanh = a, vi_tri = b).all()

    if not do_rong_ngo_data and mien == 'MB':
        do_rong_ngo_data = db.session.query(Do_rong_ngo).filter_by(Tinh_thanh = 'TP. Hà Nội', vi_tri = b).all()

    elif not do_rong_ngo_data and mien == 'MN':
        do_rong_ngo_data = db.session.query(Do_rong_ngo).filter_by(Tinh_thanh = 'TP. Hồ Chí Minh', vi_tri = b).all()
    for r in range(len(do_rong_ngo_data)):
        if x < float(do_rong_ngo_data[r].khoang_cach):
            return do_rong_ngo_data[r].ti_le
        elif x == float(do_rong_ngo_data[r].khoang_cach):
            return do_rong_ngo_data[r].ti_le
        elif float(do_rong_ngo_data[r].khoang_cach) < x < float(do_rong_ngo_data[r+1].khoang_cach):
            y = float(do_rong_ngo_data[r+1].ti_le) - ((float(do_rong_ngo_data[r+1].khoang_cach) - x)*(float(do_rong_ngo_data[r+1].ti_le) - float(do_rong_ngo_data[r].ti_le))/(float(do_rong_ngo_data[r+1].khoang_cach) - float(do_rong_ngo_data[r].khoang_cach)))
            return y
        elif x > float(do_rong_ngo_data[-1].khoang_cach):
            return do_rong_ngo_data[-1].ti_le
  

#KC TRUC CHINH  
def khoang_cach_den_truc_chinh(a, b, x, mien):
    x = float(x)
    if x == 0 or x == '':
        return 0
    khoang_cach_den_truc_chinh_data = db.session.query(Khoang_cach_truc).filter_by(Tinh_thanh = a, vi_tri = b).all()
    if not khoang_cach_den_truc_chinh_data and mien == 'MB':
        khoang_cach_den_truc_chinh_data = db.session.query(Khoang_cach_truc).filter_by(Tinh_thanh = 'TP. Hà Nội', vi_tri = b).all()
    elif not khoang_cach_den_truc_chinh_data and mien == 'MN':
        khoang_cach_den_truc_chinh_data = db.session.query(Khoang_cach_truc).filter_by(Tinh_thanh = 'TP. Hồ Chí Minh', vi_tri = b).all()
    for r in range(len(khoang_cach_den_truc_chinh_data)):
        if x < float(khoang_cach_den_truc_chinh_data[r].khoang_cach):
            return khoang_cach_den_truc_chinh_data[r].ti_le
        elif x == float(khoang_cach_den_truc_chinh_data[r].khoang_cach):
            return khoang_cach_den_truc_chinh_data[r].ti_le
        elif float(khoang_cach_den_truc_chinh_data[r].khoang_cach) < x < float(khoang_cach_den_truc_chinh_data[r+1].khoang_cach):
            y = float(khoang_cach_den_truc_chinh_data[r+1].ti_le) - ((float(khoang_cach_den_truc_chinh_data[r+1].khoang_cach) - x)*(float(khoang_cach_den_truc_chinh_data[r+1].ti_le) - float(khoang_cach_den_truc_chinh_data[r].ti_le))/(float(khoang_cach_den_truc_chinh_data[r+1].khoang_cach) - float(khoang_cach_den_truc_chinh_data[r].khoang_cach))) 
            return y
        elif x > float(khoang_cach_den_truc_chinh_data[-1].khoang_cach):
            return khoang_cach_den_truc_chinh_data[-1].ti_le


def ID_auto_create():
    id_old = db.session.query(ID_auto).all()[0].id__
    id_sub = str(int(id_old)+1)
    id_new = '0'*(8-len(id_sub)) + id_sub
    db.session.query(ID_auto).update({ID_auto.id__ : id_new})
    db.session.commit()
    return id_new


@app.route('/ajax_get_result', methods=['GET', 'POST'])
def ajax_get_result():
    # GET DATA
    tinh_thanh = request.args['tinh_thanh_thi_truong']
    quan_huyen = request.args['quan_huyen_thi_truong']
    ten_duong = request.args['ten_duong_thi_truong']
    tuyen_duong = request.args['tuyen_duong_thi_truong']
    vi_tri_bds = request.args['vi_tri_bds_thi_truong']

    try:
        do_rong_ngo_thi_truong = float(request.args['do_rong_ngo_thi_truong'])
    except:
        do_rong_ngo_thi_truong = 0
    try:
        kcach_truc_chinh_thi_truong = float(request.args['kcach_truc_chinh_thi_truong'])
    except:
        kcach_truc_chinh_thi_truong = 0
    try:
        dien_tich_dat_thi_truong = float(request.args['dien_tich_dat_thi_truong'])
    except:
        dien_tich_dat_thi_truong = 0
    try:
        do_rong_mat_tien_thi_truong = float(request.args['do_rong_mat_tien_thi_truong'])
    except:
        do_rong_mat_tien_thi_truong = 0
    hinh_dang = request.args['hinh_dang']
    loai_nha_tho_cu = request.args['loai_nha_tho_cu']
    try:
        thoi_gian_su_dung = request.args['thoi_gian_su_dung']
    except:
        thoi_gian_su_dung = 'Chưa xác định'
    try:
        dien_tich_san_xd = request.args['dien_tich_san_xd']
    except:
        dien_tich_san_xd = 0
    try:
        tang_ham_ctxd = request.args['tang_ham_ctxd']
    except:
        tang_ham_ctxd = 0
    try:
        don_gia_loai_nha = db.session.query(Loai_nha.don_gia).filter_by(loai_nha = loai_nha_tho_cu).all()[0].don_gia
    except:
        don_gia_loai_nha = 0
    try:
        ti_le_nam_su_dung = db.session.query(Nam_su_dung.ti_le).filter_by(thoi_gian = thoi_gian_su_dung).all()[0].ti_le
    except:
        ti_le_nam_su_dung = 0
    list_yeu_to = request.args['data_yeu_to'].split("|")
    list_loi_the = request.args['data_loi_the'].split("|")
    list_bat_loi = request.args['data_bat_loi'].split("|")
    try:
        dac_diem_VT = db.session.query(Dac_diem_VT.dac_diem).filter_by(thanh_pho = tinh_thanh, vi_tri = vi_tri_bds).all()[0].dac_diem
    except:
        dac_diem_VT = ''

    # TINH HE SO
    gia_tri_du_lieu = db.session.query(Data_MB.Gia_thi_truong, Data_MB.Mien, Data_MB.Dia_chi).filter_by(Tinh_thanh = tinh_thanh, Quan = quan_huyen, Duong = ten_duong, Doan_duong = tuyen_duong, Vi_tri = vi_tri_bds).all()


    gia_thi_truong = int(gia_tri_du_lieu[0][0].split(".")[0])
    mien = gia_tri_du_lieu[0][1]
    dia_chi = gia_tri_du_lieu[0][2]

    he_so_dien_tich = quy_mo(dien_tich_dat_thi_truong, mien, vi_tri_bds)
    he_so_mat_tien = mat_tien(do_rong_mat_tien_thi_truong, mien, vi_tri_bds)
    if vi_tri_bds in ['Vị trí 2', 'Vị trí 3', 'Vị trí 4']:
        he_so_rong_ngo = do_rong_ngo(tinh_thanh, vi_tri_bds, do_rong_ngo_thi_truong, mien)
        he_so_kc_truc_chinh = khoang_cach_den_truc_chinh(tinh_thanh, vi_tri_bds, kcach_truc_chinh_thi_truong, mien)
    else:
        he_so_rong_ngo = 0
        he_so_kc_truc_chinh = 0

    try:
        if mien == 'MB':
            vi_tri = 'Vị trí 0'
            he_so_hinh_dang = float(db.session.query(Hinh_dang).filter_by(hinh_dang = hinh_dang, mien = mien).all()[0].ti_le)

        elif mien in ('MN', 'MN1'):
            vi_tri = vi_tri_bds
            he_so_hinh_dang = float(db.session.query(Hinh_dang).filter_by(hinh_dang = hinh_dang, mien = mien, vi_tri = vi_tri_bds).all()[0].ti_le)     

    except:
        he_so_hinh_dang = 0

    # TINH GIA CTXD
    don_gia_ctxd = float(don_gia_loai_nha)*float(ti_le_nam_su_dung)
    if tang_ham_ctxd == 'Có':
        don_gia_ctxd = float(don_gia_loai_nha)*float(ti_le_nam_su_dung)*1.5
    
    try:
        tong_gia_ctxd = float(dien_tich_san_xd)*don_gia_ctxd
    except:
        tong_gia_ctxd = 0
    # TINH GIA DIEU CHINH DAT
    gia_tri_dieu_chinh_dien_tich = he_so_dieu_chinh(gia_thi_truong, he_so_dien_tich)
    gia_tri_dieu_chinh_mat_tien = he_so_dieu_chinh(gia_thi_truong, he_so_mat_tien)
    gia_tri_dieu_chinh_hinh_dang = he_so_dieu_chinh(gia_thi_truong, he_so_hinh_dang)
    if list_yeu_to != [u'']:
        gia_tri_dieu_chinh_yeu_to = sum([he_so_dieu_chinh(gia_thi_truong, db.session.query(Yeu_to.ti_le).filter_by(yeu_to = r, mien = mien, vi_tri = vi_tri).all()[0].ti_le) for r in list_yeu_to])
    else:
        gia_tri_dieu_chinh_yeu_to = 0
    gia_dieu_chinh_rong_ngo = he_so_dieu_chinh(gia_thi_truong, he_so_rong_ngo)
    gia_dieu_kc_truc_chinh = he_so_dieu_chinh(gia_thi_truong, he_so_kc_truc_chinh)

    # SUM GIA
    gia_dieu_chinh = round(sum([gia_tri_dieu_chinh_dien_tich,
                        gia_tri_dieu_chinh_mat_tien,
                        gia_tri_dieu_chinh_hinh_dang,
                        gia_dieu_chinh_rong_ngo,
                        gia_dieu_kc_truc_chinh,
                        gia_tri_dieu_chinh_yeu_to]) + gia_thi_truong)
    tong_gia_dat = float(gia_dieu_chinh)*float(dien_tich_dat_thi_truong)
    tong_gia_tai_san = tong_gia_dat + tong_gia_ctxd
    # TAO TICKET
    ngay_khoi_tao = dt.datetime.now()
    new_id = ID_auto_create()



    new_ticket = Id_ticket(
                new_id,
                dia_chi,
                vi_tri_bds,
                dien_tich_dat_thi_truong,
                do_rong_mat_tien_thi_truong,
                hinh_dang,
                do_rong_ngo_thi_truong,
                kcach_truc_chinh_thi_truong,
                "|".join(list_loi_the),
                "|".join(list_bat_loi),
                gia_thi_truong,
                gia_dieu_chinh,
                loai_nha_tho_cu,
                thoi_gian_su_dung,
                don_gia_ctxd,
                dien_tich_san_xd,
                session['username'],
                ngay_khoi_tao,
            )

    db.session.add(new_ticket)
    db.session.commit()

    # EVENT LOG
    # DU LIEU NHAP
    dia_chi_log = "|>TT1|" + str(dia_chi) + "*|*" 
    vi_tri_bds_log = "|>TT2|" + str(vi_tri_bds) + "*|*" 
    dien_tich_log = "|>TT3|" + str(dien_tich_dat_thi_truong) + "*|*" 
    mat_tien_log = "|>TT4|" + str(do_rong_mat_tien_thi_truong) + "*|*" 
    hinh_dang_log = "|>TT5|" + str(hinh_dang) + "*|*" 
    do_rong_ngo_log = "|>TT6|" + str(do_rong_ngo_thi_truong) + "*|*" 
    truc_chinh_log = "|>TT7|" + str(kcach_truc_chinh_thi_truong) + "*|*" 
    loi_the_log = "|>TT8|" + str("|".join(list_loi_the)) + "*|*" 
    bat_loi_log = "|>TT9|" + str("|".join(list_bat_loi)) + "*|*" 
    loai_nha_tho_cu_log = "|>TT 10|" + str(loai_nha_tho_cu) + "*|*"
    thoi_gian_su_dung_log = "|>TT 11|" + str(thoi_gian_su_dung) + "*|*"
    dien_tich_san_xd_log = "|>TT 12|" + str(dien_tich_san_xd) + "*|*"
    # KET QUA
    gia_truoc_log = "|>KQ1|" + str(gia_thi_truong) + "*|*" 
    gia_sau_log = "|>KQ2|" + str(gia_dieu_chinh) + "*|*" 
    don_gia_ctxd_log = "|>KQ 14|" + str(don_gia_ctxd) + "*|*"
    tong_gia_ctxd_log = "|>KQ 15|" + str(tong_gia_ctxd) + "*|*"
    tong_gia_tai_san_log = "|>KQ 16|" + str(tong_gia_tai_san) + "*|*"

    du_lieu_nhap = dia_chi_log + vi_tri_bds_log + dien_tich_log + mat_tien_log + hinh_dang_log + do_rong_ngo_log + truc_chinh_log + loi_the_log + bat_loi_log + loai_nha_tho_cu_log + thoi_gian_su_dung_log + dien_tich_san_xd_log
    ket_qua = gia_truoc_log + gia_sau_log + don_gia_ctxd_log + tong_gia_ctxd_log + tong_gia_tai_san_log

    event_log = Event_log(new_id, session['username'], ngay_khoi_tao, 'bds_tho_cu', du_lieu_nhap, ket_qua)
    db.session.add(event_log)
    db.session.commit()

    return jsonify({ 
                    'new_id' : new_id,
                    'ngay_khoi_tao' : ngay_khoi_tao,
                    'gia_truoc' : gia_thi_truong,
                    'gia_sau' : gia_dieu_chinh,
                    'dia_chi' : dia_chi,
                    'vi_tri' : vi_tri_bds,
                    'dac_diem_vi_tri' : dac_diem_VT,
                    'do_rong_ngo' : do_rong_ngo_thi_truong,
                    'kcach' : kcach_truc_chinh_thi_truong,
                    'mat_tien' : do_rong_mat_tien_thi_truong,
                    'hinh_dang' : hinh_dang,
                    'dien_tich' : dien_tich_dat_thi_truong,
                    'list_yeu_to' : list_yeu_to,
                    'tong_gia_dat' : tong_gia_dat,
                    'list_loi_the' : list_loi_the,
                    'list_bat_loi' : list_bat_loi,
                    'loai_nha_tho_cu' : loai_nha_tho_cu,
                    'thoi_gian_su_dung' : thoi_gian_su_dung,
                    'dien_tich_san_xd' : dien_tich_san_xd,
                    'don_gia_ctxd' : don_gia_ctxd,
                    'tong_gia_ctxd' : tong_gia_ctxd,
                    'tong_gia_tai_san' : tong_gia_tai_san,
                    })


#---------------- PAGE ------------------
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# ----------------ADMIN -----------------
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():    
    return render_template('login.html')
    

@app.route('/authentication', methods=['GET', 'POST'])
def authentication():
    user = request.args["usn"].lower()
    pwd = request.args["pd"]
    check_user = db.session.query(User_SM.phan_quyen, User_SM.name).filter_by(username = user, passhash = hash_user(pwd)).distinct().all()
    if check_user:
        session['username'] = user
        session['password'] = pwd
        session['role'] = check_user[0].phan_quyen
        session['name'] = check_user[0].name
        session['logged_in'] = True
        user = db.session.query(User_SM.name, User_SM.cmnd, User_SM.mail, User_SM.sdt, User_SM.username, User_SM.ngay_khoi_tao, User_SM.phan_quyen, User_SM.trang_thai, User_SM.ngay_doi_pass).filter_by(username = session['username']).all()[0]
        ngay_tao = dt.datetime.now()
        ngay_doi = str_to_dt(user.ngay_doi_pass.split(".")[0])
        thoi_gian_doi_pass = ngay_tao - ngay_doi
        print(thoi_gian_doi_pass)
        if 'days' in str(thoi_gian_doi_pass):
            if int(str(thoi_gian_doi_pass).split(" day")[0]) > 60:
                print(int(str(thoi_gian_doi_pass).split(" day")[0]))
                session['changepass'] = False
                return jsonify({'result' : 'changepass'})
            else:
                session['changepass'] = True  
        else:

            session['changepass'] = True    
        return jsonify({'result' : 'check_gia'})
    else:
        return jsonify({'result' : 'login'})


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


# ----------------ADMIN -----------------
@app.route('/ad_cnb_min',methods=['GET', 'POST'])
@login_required
@changepass_required
@admin_required
def ad_cnb_min():
    return render_template(
        "trang-chu/admin.html",
        
    )

###################
@app.route('/check_gia',methods=['GET', 'POST'])
@login_required
@changepass_required
# @admin_required
def check_gia():
    list_tinh_thanh = [r[0] for r in db.session.query(Data_MB.Tinh_thanh).distinct().order_by(Data_MB.Tinh_thanh.asc()).all()]
    list_tinh_thanh_uy_ban = [r[0] for r in db.session.query(Khung_gia_uy_ban.thanh_pho).distinct().order_by(Khung_gia_uy_ban.thanh_pho.asc()).all()]
    list_thanh_pho_quy_hoach = [r[0] for r in db.session.query(Quy_hoach.thanh_pho).distinct().order_by(Quy_hoach.thanh_pho.asc()).all()]
    list_can_ho = [r[0] for r in db.session.query(Data_chung_cu.ten_du_an).distinct().order_by(Data_chung_cu.ten_du_an.asc()).all()]
    list_biet_thu = [r[0] for r in db.session.query(BDS_biet_thu.ten_du_an).distinct().order_by(BDS_biet_thu.ten_du_an.asc()).all()]
    list_hinh_dang_bds = [r[0] for r in db.session.query(Hinh_dang.hinh_dang).distinct().order_by(Hinh_dang.hinh_dang.asc()).all()]
    list_loai_nha  = [r[0] for r in db.session.query(Loai_nha.loai_nha).distinct().order_by(Loai_nha.loai_nha.asc()).all()]
    list_nam_su_dung  = [r[0] for r in db.session.query(Nam_su_dung.thoi_gian).distinct().order_by(Nam_su_dung.thoi_gian.asc()).all()]
    Id_ticket = [r[0] for r in db.session.query(Event_log.id_ticket).filter_by(username = session['username']).order_by(Event_log.id_ticket.desc()).all()]
    return render_template(
        "tool_calculate_template/check_gia.html",
        list_tinh_thanh = list_tinh_thanh,
        list_biet_thu = list_biet_thu,
        list_can_ho = list_can_ho,
        list_hinh_dang_bds = list_hinh_dang_bds,
        list_tinh_thanh_uy_ban = list_tinh_thanh_uy_ban,
        list_thanh_pho_quy_hoach = list_thanh_pho_quy_hoach,
        list_loai_nha = list_loai_nha,
        list_nam_su_dung = list_nam_su_dung,
        Id_ticket = Id_ticket,
    )


@app.route('/tin_tuc/danh_muc_tin_tuc',methods=['GET', 'POST'])
@login_required
@admin_required
def form_tin_tuc():
    return render_template(
        "trang-chu/tin_tuc/danh_muc_tin_tuc.html",
        
    )

#
@app.route('/user/profile',methods=['GET', 'POST'])
@login_required
@changepass_required
def profile():
    user = db.session.query(User_SM.name, User_SM.cmnd, User_SM.mail, User_SM.sdt, User_SM.username, User_SM.ngay_khoi_tao, User_SM.phan_quyen, User_SM.trang_thai, User_SM.ngay_doi_pass).filter_by(username = session['username']).all()[0]
    ngay_tao = dt.datetime.now()
    # ngay_doi = str_to_dt(user.ngay_doi_pass.split(".")[0])
    ngay_doi = dt.datetime(2018, 5, 14)


    print(ngay_tao - ngay_doi)
    return render_template(
        "user/profile.html", user = user      
    )


@app.route('/user/changepass',methods=['GET', 'POST'])
@login_required
def changepass():
    user = db.session.query(User_SM.name, User_SM.cmnd, User_SM.mail, User_SM.sdt, User_SM.username, User_SM.ngay_khoi_tao, User_SM.phan_quyen, User_SM.trang_thai, User_SM.ngay_doi_pass).filter_by(username = session['username']).all()[0]    
    return render_template(
        "user/changepass.html", user = user      
    )


@app.route('/ajax_change_pass', methods=['GET', 'POST'])
def ajax_change_pass():
    new_pass = request.args["new_pass"]
    user = db.session.query(User_SM).filter_by(username = session['username']).update({User_SM.password : new_pass, User_SM.passhash : hash_user(new_pass), User_SM.ngay_doi_pass : dt.datetime.now()})
    db.session.commit()
    session['changepass'] = True
    return 'Đổi mật khẩu thành công.'

@app.route('/user/quan_ly_user', methods=['GET', 'POST'])
@login_required
@changepass_required
@admin_required
def quan_ly_user():
    list_user = db.session.query(User_SM.name, User_SM.cmnd, User_SM.mail, User_SM.sdt, User_SM.username, User_SM.ngay_khoi_tao, User_SM.phan_quyen, User_SM.trang_thai).all()
    return render_template(
        "user/quan_ly_user.html", list_user = list_user        
    )


@app.route('/user/tao_moi_user',methods=['GET', 'POST'])
@login_required
@admin_required
def tao_moi_user():
    user_field = ['name', 'cmnd', 'mail', 'sdt', 'username', 'password', 'passhash', 'ngay_khoi_tao', 'phan_quyen', 'trang_thai']
    if request.method == 'POST':
        name = request.form.get("name")
        cmnd = request.form.get("cmnd")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        status = request.form.get("status")
        sdt = request.form.get("sdt")
        new_user = User_SM(name, cmnd, email, sdt, username, password, hash_user(password), str(dt.datetime.now()), role, status, dt.datetime(2000,1,1))
        db.session.add(new_user)
        db.session.commit()
    return render_template(
        "user/tao_moi_user.html",        
    )


# if __name__ == '__main__':
#     app.debug = True
#     HOST = environ.get('server_host', 'localhost')
#     # HOST = environ.get('server_host', '192.168.0.105')

#     # HOST = environ.get('server_host', 'localhost')
#     try:
#         # PORT = int(environ.get('8080', '8888'))
#         PORT = int(environ.get('server_port', '33507'))
#     except ValueError:
#         PORT = 33507
#     app.run(HOST, PORT, threaded = True)


if __name__ == '__main__':
    # Run the app on all available interfaces on port 80 which is the
    # standard port for HTTP
    db.create_all()
    app.debug = True
    port = int(os.environ.get("PORT", 33507))
    app.run(
        host="0.0.0.0",
        port=port,
    )