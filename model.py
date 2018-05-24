from flask_sqlalchemy  import SQLAlchemy
from flask import Flask
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Sequence, VARCHAR,NVARCHAR, DateTime, update
app = Flask(__name__,static_url_path='/static')

db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# ID AUTO
# USER
class ID_auto(db.Model):
    __tablename__ = "ID_auto"
    id__ = db.Column('id__', String, nullable = False, primary_key = True)
    def __init__(self, id__):
        self.id__ = id__
    def __repr__(self):
        return str([self.id__])

 

# THONG TIN QUY HOACH
class Quy_hoach(db.Model):
    __tablename__ = "thong_tin_quy_hoach"
    thanh_pho = db.Column('thanh_pho', String, nullable = False, primary_key = True)
    quan = db.Column('quan', String, nullable = False, primary_key = True)
    duong = db.Column('duong', String, nullable = False, primary_key = True)
    doan_duong = db.Column('doan_duong', String, nullable = False, primary_key = True)
    quy_hoach_hien_huu = db.Column('quy_hoach_hien_huu', String, nullable = False, primary_key = True)
    quy_hoach_moi = db.Column('quy_hoach_moi', String, nullable = False, primary_key = True)
    quy_hoach_thoat_lu = db.Column('quy_hoach_thoat_lu', String, nullable = False, primary_key = True)
    quy_hoach_cong_trinh = db.Column('quy_hoach_cong_trinh', String, nullable = False, primary_key = True)
    ghi_chu = db.Column('ghi_chu', String, nullable = False, primary_key = True)

    def __init__(self, thanh_pho, quan, duong, doan_duong, quy_hoach_hien_huu, quy_hoach_moi, quy_hoach_thoat_lu, quy_hoach_cong_trinh, ghi_chu):
        self.thanh_pho = thanh_pho
        self.quan = quan
        self.duong = duong
        self.doan_duong = doan_duong
        self.quy_hoach_hien_huu = quy_hoach_hien_huu
        self.quy_hoach_moi = quy_hoach_moi
        self.quy_hoach_thoat_lu = quy_hoach_thoat_lu
        self.quy_hoach_cong_trinh = quy_hoach_cong_trinh
        self.ghi_chu = ghi_chu

    def __repr__(self):
        return str([self.thanh_pho, self.quan, self.duong, self.doan_duong, self.quy_hoach_hien_huu, self.quy_hoach_moi, self.quy_hoach_thoat_lu, self.quy_hoach_cong_trinh, self.ghi_chu])


# USER
class User_SM(db.Model):
    __tablename__ = "sm_user"
    name = db.Column('name', String, nullable = False)
    cmnd = db.Column('cmnd', String, nullable = False)
    mail = db.Column('mail', String, nullable = False)
    sdt = db.Column('sdt', String, nullable = False)
    username = db.Column('username', String, primary_key = True, nullable = False)
    password = db.Column('password', String, nullable = False)
    passhash = db.Column('passhash', String, nullable = False)
    ngay_khoi_tao = db.Column('ngay_khoi_tao', String, nullable = False)
    phan_quyen = db.Column('phan_quyen', String, nullable = False)
    trang_thai = db.Column('trang_thai', String, nullable = False)
    ngay_doi_pass = db.Column('ngay_doi_pass', String, nullable = False)

    def __init__(self, name, cmnd, mail, sdt, username, password, passhash, ngay_khoi_tao, phan_quyen, trang_thai, ngay_doi_pass):
        self.name = name
        self.cmnd = cmnd
        self.mail = mail
        self.sdt = sdt
        self.username = username
        self.password = password
        self.passhash = passhash
        self.ngay_khoi_tao = ngay_khoi_tao
        self.phan_quyen = phan_quyen
        self.trang_thai = trang_thai
        self.ngay_doi_pass = ngay_doi_pass

    def __repr__(self):
        return str([self.name, self.cmnd, self.mail, self.sdt, self.username, self.password, self.passhash, self.ngay_khoi_tao, self.phan_quyen, self.trang_thai, self.ngay_doi_pass])


# LOAI NHA
class Loai_nha(db.Model):
    __tablename__ = "loai_nha_tho_cu"
    loai_nha = db.Column('loai_nha', String, nullable = False, primary_key = True)
    don_gia = db.Column('don_gia', String, nullable = False, primary_key = True)
    def __init__(self, loai_nha, don_gia):
        self.loai_nha = loai_nha
        self.don_gia = don_gia
    def __repr__(self):
        return str([self.loai_nha, self.don_gia])


# NAM SU DUNG
class Nam_su_dung(db.Model):
    __tablename__ = "thoi_gian_su_dung"
    thoi_gian = db.Column('thoi_gian', String, nullable = False, primary_key = True)
    ti_le = db.Column('ti_le', String, nullable = False, primary_key = True)
    def __init__(self, thoi_gian, ti_le):
        self.thoi_gian = thoi_gian
        self.ti_le = ti_le
    def __repr__(self):
        return str([self.thoi_gian, self.ti_le])


# EVENT LOG
class Event_log(db.Model):
    __tablename__ = "event_log"
    id_ticket = db.Column('id_ticket', String, nullable = False, primary_key= True)
    username = db.Column('username', String, nullable = False)
    time_process = db.Column('time_process', String, nullable = False)
    phan_loai = db.Column('phan_loai', String, nullable = False)
    du_lieu_nhap = db.Column('du_lieu_nhap', String, nullable = False)
    ket_qua = db.Column('ket_qua', String, nullable = False)
    def __init__(self, id_ticket, username, time_process, phan_loai, du_lieu_nhap, ket_qua):
        self.id_ticket = id_ticket
        self.username = username
        self.time_process = time_process
        self.phan_loai = phan_loai
        self.du_lieu_nhap = du_lieu_nhap
        self.ket_qua = ket_qua

    def __repr__(self):
        return str([self.id_ticket, self.username, self.time_process, self.phan_loai, self.du_lieu_nhap, self.ket_qua])


# ID TICKET THO CU
class Id_ticket(db.Model):
    __tablename__ = "id_ticket"
    id_ticket = db.Column('id_ticket', String, nullable = False, primary_key= True)
    dia_chi = db.Column('dia_chi', String, nullable = False)
    vi_tri = db.Column('vi_tri', String, nullable = False)
    dien_tich = db.Column('dien_tich', String, nullable = False)
    mat_tien = db.Column('mat_tien', String, nullable = False)
    hinh_dang = db.Column('hinh_dang', String, nullable = False)
    do_rong_ngo = db.Column('do_rong_ngo', String, nullable = False)
    kcach_truc_chinh = db.Column('kcach_truc_chinh', String, nullable = False)
    yeu_to_loi_the = db.Column('yeu_to_loi_the', String, nullable = False)
    yeu_to_bat_loi = db.Column('yeu_to_bat_loi', String, nullable = False)
    gia_truoc = db.Column('gia_truoc', String, nullable = False)
    gia_sau = db.Column('gia_sau', String, nullable = False)
    
    loai_nha = db.Column('loai_nha', String, nullable = False, primary_key = True)
    thoi_gian_su_dung = db.Column('thoi_gian_su_dung', String, nullable = False, primary_key = True)
    don_gia_ctxd = db.Column('don_gia_ctxd', String, nullable = False, primary_key = True)
    dien_tich_san_xd = db.Column('dien_tich_san_xd', String, nullable = False, primary_key = True)
    username = db.Column('username', String, nullable = False)
    time = db.Column('time', String, nullable = False)    

    def __init__(self, id_ticket, dia_chi, vi_tri, dien_tich, mat_tien, hinh_dang, do_rong_ngo, kcach_truc_chinh, yeu_to_loi_the, yeu_to_bat_loi, gia_truoc, gia_sau, loai_nha, thoi_gian_su_dung, don_gia_ctxd, dien_tich_san_xd,username, time):
        self.id_ticket = id_ticket        
        self.dia_chi = dia_chi
        self.vi_tri = vi_tri
        self.dien_tich = dien_tich
        self.mat_tien = mat_tien
        self.hinh_dang = hinh_dang
        self.do_rong_ngo = do_rong_ngo
        self.kcach_truc_chinh = kcach_truc_chinh
        self.yeu_to_loi_the = yeu_to_loi_the
        self.yeu_to_bat_loi = yeu_to_bat_loi
        self.gia_truoc = gia_truoc
        self.gia_sau = gia_sau
        self.loai_nha = loai_nha
        self.thoi_gian_su_dung = thoi_gian_su_dung
        self.don_gia_ctxd = don_gia_ctxd
        self.dien_tich_san_xd = dien_tich_san_xd
        self.username = username
        self.time = time

    def __repr__(self):
        return str([self.id_ticket, self.dia_chi, self.vi_tri, self.dien_tich, self.mat_tien, self.hinh_dang, self.do_rong_ngo, self.kcach_truc_chinh, self.yeu_to_loi_the, self.yeu_to_bat_loi, self.gia_truoc, self.gia_sau, self.loai_nha, self.thoi_gian_su_dung, self.don_gia_ctxd, self.dien_tich_san_xd, self.username, self.time])


# ID TICKET BIET THU
class Id_ticket_BT(db.Model):
    __tablename__ = "id_ticket_biet_thu"
    id_ticket = db.Column('id_ticket', String, nullable = False, primary_key = True)
    ten_du_an = db.Column('ten_du_an', String, nullable = False)
    dien_tich_dat = db.Column('dien_tich_dat', String, nullable = False)
    dien_tich_san_xd = db.Column('dien_tich_san_xd', String, nullable = False)
    don_gia_dat = db.Column('don_gia_dat', String, nullable = False)
    don_gia_ctxd = db.Column('don_gia_ctxd', String, nullable = False)
    tong_gia_xay_tho = db.Column('tong_gia_xay_tho', String, nullable = False)
    tong_gia_hoan_thien = db.Column('tong_gia_hoan_thien', String, nullable = False)
    username = db.Column('username', String, nullable = False)
    time = db.Column('time', String, nullable = False)
    dia_chi = db.Column('dia_chi', String, nullable = False)

    def __init__(self, id_ticket, ten_du_an, dien_tich_dat, dien_tich_san_xd, don_gia_dat, don_gia_ctxd, tong_gia_xay_tho, tong_gia_hoan_thien, username, time, dia_chi):
        self.id_ticket = id_ticket
        self.ten_du_an = ten_du_an
        self.dien_tich_dat = dien_tich_dat
        self.dien_tich_san_xd = dien_tich_san_xd
        self.don_gia_dat = don_gia_dat
        self.don_gia_ctxd = don_gia_ctxd
        self.tong_gia_xay_tho = tong_gia_xay_tho
        self.tong_gia_hoan_thien = tong_gia_hoan_thien
        self.username = username
        self.time = time
        self.dia_chi = dia_chi

    def __repr__(self):
        return str([self.id_ticket, self.ten_du_an, self.dien_tich_dat, self.dien_tich_san_xd, self.don_gia_dat, self.don_gia_ctxd, self.tong_gia_xay_tho, self.tong_gia_hoan_thien, self.username, self.time, self.dia_chi])


# ID TICKET CHUNG CU
class Id_ticket_CC(db.Model):
    __tablename__ = "id_ticket_chung_cu"
    id_ticket = db.Column('id_ticket', String, nullable = False, primary_key = True)
    ten_du_an = db.Column('ten_du_an', String, nullable = False)
    dien_tich = db.Column('dien_tich', String, nullable = False)
    loai_dien_tich = db.Column('loai_dien_tich', String, nullable = False)
    don_gia = db.Column('don_gia', String, nullable = False)
    tong_gia = db.Column('tong_gia', String, nullable = False)
    username = db.Column('username', String, nullable = False)
    time = db.Column('time', String, nullable = False)
    dia_chi = db.Column('dia_chi', String, nullable = False)

    def __init__(self, id_ticket, ten_du_an, dien_tich, loai_dien_tich, don_gia, tong_gia, username, time, dia_chi):
        self.id_ticket = id_ticket
        self.ten_du_an = ten_du_an
        self.dien_tich = dien_tich
        self.loai_dien_tich = loai_dien_tich
        self.don_gia = don_gia
        self.tong_gia = tong_gia
        self.username = username
        self.time = time
        self.dia_chi = dia_chi


    def __repr__(self):
        return str([self.id_ticket, self.ten_du_an, self.dien_tich, self.loai_dien_tich, self.don_gia, self.tong_gia, self.username, self.time, self.dia_chi])


# ID TICKET QUY HOACH
class Id_ticket_quy_hoach(db.Model):
    __tablename__ = "id_ticket_quy_hoach"
    id_ticket = db.Column('id_ticket', String, nullable = False, primary_key = True)
    dia_chi = db.Column('dia_chi', String, nullable = False)
    vi_tri = db.Column('vi_tri', String, nullable = False)
    ket_qua = db.Column('ket_qua', String, nullable = False)
    username = db.Column('username', String, nullable = False)
    time = db.Column('time', String, nullable = False)
    def __init__(self, id_ticket, dia_chi, vi_tri, ket_qua, username, time):
        self.id_ticket = id_ticket
        self.dia_chi = dia_chi
        self.vi_tri = vi_tri
        self.ket_qua = ket_qua
        self.username = username
        self.time = time

    def __repr__(self):
        return str([self.id_ticket, self.dia_chi, self.vi_tri, self.ket_qua, self.username, self.time])


# KHUNG GIA UY BAN
class Khung_gia_uy_ban(db.Model):
    __tablename__ = "Khung_gia_uy_ban"
    thanh_pho = db.Column('thanh_pho', String, primary_key = True, nullable = False)
    quan_huyen = db.Column('quan_huyen', String, primary_key = True, nullable = False)
    tuyen_duong = db.Column('tuyen_duong', String, primary_key = True, nullable = False)
    doan_tu_den = db.Column('doan_tu_den', String, primary_key = True, nullable = False)
    VT1 = db.Column('VT1', String, primary_key = True, nullable = False)
    VT2 = db.Column('VT2', String, primary_key = True, nullable = False)
    VT3 = db.Column('VT3', String, primary_key = True, nullable = False)
    VT4 = db.Column('VT4', String, primary_key = True, nullable = False)
    VT5 = db.Column('VT5', String, primary_key = True, nullable = False)
    def __init__(self, thanh_pho,quan_huyen,tuyen_duong,doan_tu_den,VT1,VT2,VT3,VT4,VT5):
        self.thanh_pho
        self.quan_huyen
        self.tuyen_duong
        self.doan_tu_den
        self.VT1
        self.VT2
        self.VT3
        self.VT4
        self.VT5
    def __repr__(self):
        return str([self.thanh_pho, self.quan_huyen, self.tuyen_duong, self.doan_tu_den, self.VT1, self.VT2, self.VT3, self.VT4, self.VT5])


# DATA MB
class Data_MB(db.Model):
    __tablename__ = "Data_MB"
    Tinh_thanh = db.Column('Tinh_thanh', String, primary_key = True, nullable = False)
    Quan = db.Column('Quan', String, primary_key = True, nullable = False)
    Duong = db.Column('Duong', String, primary_key = True, nullable = False)
    Doan_duong = db.Column('Doan_duong', String, primary_key = True, nullable = False)
    Vi_tri = db.Column('Vi_tri', String, primary_key = True, nullable = False)
    Gia_UBND = db.Column('Gia_UBND', String, primary_key = True, nullable = False)
    Gia_thi_truong = db.Column('Gia_thi_truong', String, primary_key = True, nullable = False)
    Thong_tin_quy_hoach = db.Column('Thong_tin_quy_hoach', String, primary_key = True, nullable = False)
    Dia_chi = db.Column('Dia_chi', String, primary_key = True, nullable = False)
    Mien = db.Column('Mien', String, primary_key = True, nullable = False)

    def __init__(self, Tinh_thanh, Quan, Duong, Doan_duong, Vi_tri, Gia_UBND, Gia_thi_truong, Thong_tin_quy_hoach, Dia_chi, Mien):
        self.Tinh_thanh
        self.Quan
        self.Duong
        self.Doan_duong
        self.Vi_tri
        self.Gia_UBND
        self.Gia_thi_truong
        self.Thong_tin_quy_hoach
        self.Dia_chi
        self.Mien
    def __repr__(self):
        return str([self.Tinh_thanh, self.Quan, self.Duong, self.Doan_duong, self.Vi_tri, self.Gia_UBND, self.Gia_thi_truong, self.Thong_tin_quy_hoach, self.Dia_chi, self.Mien])


# DATA CHUNG CU
class Data_chung_cu(db.Model):
    __tablename__ = "data_chung_cu"
    ten_du_an = db.Column('ten_du_an', String, primary_key = True, nullable = False)
    ten_toa_duong_day_khu = db.Column('ten_toa_duong_day_khu', String, primary_key = True, nullable = False)
    ten_tang_loai_nha = db.Column('ten_tang_loai_nha', String, primary_key = True, nullable = False)
    ma_can = db.Column('ma_can', String, primary_key = True, nullable = False)
    dien_tich = db.Column('dien_tich', String, primary_key = True, nullable = False)
    loai_dien_tich = db.Column('loai_dien_tich', String, primary_key = True, nullable = False)
    don_gia = db.Column('don_gia', String, primary_key = True, nullable = False)
    dia_chi = db.Column('dia_chi', String, primary_key = True, nullable = False)

    def __init__(self, ten_du_an, ten_toa_duong_day_khu, ten_tang_loai_nha, ma_can, dien_tich, loai_dien_tich, don_gia, dia_chi):
        self.ten_du_an
        self.ten_toa_duong_day_khu
        self.ten_tang_loai_nha
        self.ma_can
        self.dien_tich
        self.loai_dien_tich
        self.don_gia
        self.dia_chi
    def __repr__(self):
        return str([self.ten_du_an, self.ten_toa_duong_day_khu, self.ten_tang_loai_nha, self.ma_can, self.dien_tich, self.loai_dien_tich, self.don_gia, self.dia_chi])


# BDS BIET THU
class BDS_biet_thu(db.Model):
    __tablename__ = "bds_lien_ke_bt"
    ten_du_an = db.Column('ten_du_an', String, primary_key = True, nullable = False)
    ten_duong = db.Column('ten_duong', String, primary_key = True, nullable = False)
    ten_tang = db.Column('ten_tang', String, primary_key = True, nullable = False)
    ma_can = db.Column('ma_can', String, primary_key = True, nullable = False)
    dien_tich_dat = db.Column('dien_tich_dat', String, primary_key = True, nullable = False)
    dien_tich_san_xay_dung = db.Column('dien_tich_san_xay_dung', String, primary_key = True, nullable = False)
    tong_gia_tri_xay_tho = db.Column('tong_gia_tri_xay_tho', String, primary_key = True, nullable = False)
    tong_gia_tri_hoan_thien = db.Column('tong_gia_tri_hoan_thien', String, primary_key = True, nullable = False)
    don_gia_dat = db.Column('don_gia_dat', String, primary_key = True, nullable = False)
    don_gia_ctxd = db.Column('don_gia_ctxd', String, primary_key = True, nullable = False)
    dia_chi = db.Column('dia_chi', String, primary_key = True, nullable = False)
    def __init__(self, ten_du_an, ten_duong, ten_tang, ma_can, dien_tich_dat, dien_tich_san_xay_dung, tong_gia_tri_xay_tho, tong_gia_tri_hoan_thien, don_gia_dat, don_gia_ctxd, dia_chi):
        self.ten_du_an
        self.ten_duong
        self.ten_tang
        self.ma_can
        self.dien_tich_dat
        self.dien_tich_san_xay_dung
        self.tong_gia_tri_xay_tho
        self.tong_gia_tri_hoan_thien
        self.don_gia_dat
        self.don_gia_ctxd
        self.dia_chi
    def __repr__(self):
        return str([self.ten_du_an, self.ten_duong, self.ten_tang, self.ma_can, self.dien_tich_dat, self.dien_tich_san_xay_dung, self.tong_gia_tri_xay_tho, self.tong_gia_tri_hoan_thien, self.don_gia_dat, self.don_gia_ctxd, self.dia_chi])


# YEU TO
class Yeu_to(db.Model):
    __tablename__ = "yeu_to"
    yeu_to = db.Column('yeu_to', String, primary_key = True, nullable = False)
    ti_le = db.Column('ti_le', String, primary_key = True, nullable = False)
    mien = db.Column('mien', String, primary_key = True, nullable = False)
    vi_tri = db.Column('vi_tri', String, primary_key = True, nullable = False)
    phan_loai = db.Column('phan_loai', String, primary_key = True, nullable = False)
    def __init__(self, yeu_to, ti_le, mien, vi_tri, phan_loai):
        self.yeu_to
        self.ti_le
        self.mien
        self.vi_tri
        self.phan_loai
    def __repr__(self):
        return str([self.yeu_to, self.ti_le, self.mien, self.vi_tri, self.phan_loai])


# MAT TIEN
class Mat_tien(db.Model):
    __tablename__ = "mat_tien"
    mat_tien = db.Column('mat_tien', String, primary_key = True, nullable = False)
    ti_le = db.Column('ti_le', String, primary_key = True, nullable = False)
    mien = db.Column('mien', String, primary_key = True, nullable = False)
    vi_tri = db.Column('vi_tri', String, primary_key = True, nullable = False)
    def __init__(self, mat_tien, ti_le, mien, vi_tri):
        self.mat_tien
        self.ti_le
        self.mien
        self.vi_tri
    def __repr__(self):
        return str([self.mat_tien, self.ti_le, self.mien, self.vi_tri])


# QUY MO
class Quy_mo(db.Model):
    __tablename__ = "quy_mo"
    quy_mo = db.Column('quy_mo', String, primary_key = True, nullable = False)
    ti_le = db.Column('ti_le', String, primary_key = True, nullable = False)
    mien = db.Column('mien', String, primary_key = True, nullable = False)
    vi_tri = db.Column('vi_tri', String, primary_key = True, nullable = False)
    def __init__(self, quy_mo, ti_le, mien, vi_tri):
        self.quy_mo
        self.ti_le
        self.mien
        self.vi_tri
    def __repr__(self):
        return str([self.quy_mo, self.ti_le, self.mien, self.vi_tri])


# HINH DANG
class Hinh_dang(db.Model):
    __tablename__ = "hinh_dang"
    hinh_dang = db.Column('hinh_dang', String, primary_key = True, nullable = False)
    ti_le = db.Column('ti_le', String, primary_key = True, nullable = False)
    mien = db.Column('mien', String, primary_key = True, nullable = False)
    vi_tri = db.Column('vi_tri', String, primary_key = True, nullable = False)
    def __init__(self, hinh_dang, ti_le, mien, vi_tri):
        self.hinh_dang
        self.ti_le
        self.mien
        self.vi_tri
    def __repr__(self):
        return str([self.hinh_dang, self.ti_le, self.mien, self.vi_tri])


# DO RONG NGO
class Do_rong_ngo(db.Model):
    __tablename__ = "do_rong_ngo"
    Tinh_thanh = db.Column('Tinh_thanh', String, primary_key = True, nullable = False)
    vi_tri = db.Column('vi_tri', String, primary_key = True, nullable = False)
    khoang_cach = db.Column('khoang_cach', String, primary_key = True, nullable = False)
    ti_le = db.Column('ti_le', String, primary_key = True, nullable = False)
    mien = db.Column('mien', String, primary_key = True, nullable = False)
    
    def __init__(self, Tinh_thanh, vi_tri, khoang_cach, ti_le, mien):
        self.Tinh_thanh
        self.vi_tri
        self.khoang_cach        
        self.ti_le
        self.mien
    def __repr__(self):
        return str([self.Tinh_thanh, self.vi_tri, self.khoang_cach , self.ti_le, self.mien])


# KHOANG CACH TRUC CHINH
class Khoang_cach_truc(db.Model):
    __tablename__ = "khoang_cach_den_truc_chinh"
    Tinh_thanh = db.Column('Tinh_thanh', String, primary_key = True, nullable = False)
    vi_tri = db.Column('vi_tri', String, primary_key = True, nullable = False)
    khoang_cach = db.Column('khoang_cach', String, primary_key = True, nullable = False)
    ti_le = db.Column('ti_le', String, primary_key = True, nullable = False)
    mien = db.Column('mien', String, primary_key = True, nullable = False)
    
    def __init__(self, Tinh_thanh, vi_tri, khoang_cach, ti_le, mien):
        self.Tinh_thanh
        self.vi_tri
        self.khoang_cach        
        self.ti_le
        self.mien
    def __repr__(self):
        return str([self.Tinh_thanh, self.vi_tri, self.khoang_cach , self.ti_le, self.mien])


#DAC DIEM VI TRI
class Dac_diem_VT(db.Model):
    __tablename__ = "dac_diem_vi_tri"
    thanh_pho = db.Column('thanh_pho', String, primary_key = True, nullable = False)
    vi_tri = db.Column('vi_tri', String, primary_key = True, nullable = False)
    dac_diem = db.Column('dac_diem', String, primary_key = True, nullable = False)
    def __init__(self, thanh_pho, vi_tri, dac_diem):
        self.thanh_pho
        self.vi_tri
        self.dac_diem
    def __repr__(self):
        return str([self.thanh_pho, self.vi_tri, self.dac_diem])


# ROA
# ROA THO CU
class ROA_tho_cu(db.Model):
    __tablename__ = "roa_tho_cu"
    Tinh_thanh = db.Column('Tinh_thanh', String, primary_key = True, nullable = False)
    Quan = db.Column('Quan', String, primary_key = True, nullable = False)
    Duong = db.Column('Duong', String, primary_key = True, nullable = False)
    Doan_duong = db.Column('Doan_duong', String, primary_key = True)
    Vi_tri = db.Column('Vi_tri', String, primary_key = True, nullable = False)
    dia_chi = db.Column('dia_chi', String, primary_key = True, nullable = False)
    roa1 = db.Column('roa1', String, primary_key = True)
    roa2 = db.Column('roa2', String, primary_key = True)
    roa3 = db.Column('roa3', String, primary_key = True)
    roa4 = db.Column('roa4', String, primary_key = True)
    roa5 = db.Column('roa5', String, primary_key = True)
    roa6 = db.Column('roa6', String, primary_key = True)
    roa7 = db.Column('roa7', String, primary_key = True)
    roa8 = db.Column('roa8', String, primary_key = True)
    def __init__(self, Tinh_thanh, Quan, Duong, Doan_duong, Vi_tri, dia_chi, roa1, roa2, roa3, roa4, roa5, roa6, roa7, roa8):
        self.Tinh_thanh = Tinh_thanh
        self.Quan = Quan
        self.Duong = Duong
        self.Doan_duong = Doan_duong
        self.Vi_tri = Vi_tri
        self.dia_chi = dia_chi
        self.roa1 = roa1
        self.roa2 = roa2
        self.roa3 = roa3
        self.roa4 = roa4
        self.roa5 = roa5
        self.roa6 = roa6
        self.roa7 = roa7
        self.roa8 = roa8
    def __repr__(self):
        return str([self.Tinh_thanh, self.Quan, self.Duong, self.Doan_duong, self.Vi_tri, self.dia_chi, self.roa1, self.roa2, self.roa3, self.roa4, self.roa5, self.roa6, self.roa7, self.roa8])

# ROA CHUNG CU
class ROA_chung_cu(db.Model):
    __tablename__ = "roa_chung_cu"
    ten_du_an = db.Column('ten_du_an', String, primary_key = True, nullable = False)
    ten_toa_duong_day_khu = db.Column('ten_toa_duong_day_khu', String, primary_key = True, nullable = False)
    ten_tang_loai_nha = db.Column('ten_tang_loai_nha', String, primary_key = True, nullable = False)
    ma_can = db.Column('ma_can', String, primary_key = True, nullable = False)
    dia_chi = db.Column('dia_chi', String, primary_key = True, nullable = False)

    roa1 = db.Column('roa1', String, primary_key = True)
    roa2 = db.Column('roa2', String, primary_key = True)
    roa3 = db.Column('roa3', String, primary_key = True)
    roa4 = db.Column('roa4', String, primary_key = True)
    roa5 = db.Column('roa5', String, primary_key = True)
    roa6 = db.Column('roa6', String, primary_key = True)
    roa7 = db.Column('roa7', String, primary_key = True)
    roa8 = db.Column('roa8', String, primary_key = True)
    def __init__(self, ten_du_an, ten_toa_duong_day_khu, ten_tang_loai_nha, ma_can, dia_chi, roa1, roa2, roa3, roa4, roa5, roa6, roa7, roa8):
        self.ten_du_an = ten_du_an
        self.ten_toa_duong_day_khu = ten_toa_duong_day_khu
        self.ten_tang_loai_nha = ten_tang_loai_nha
        self.ma_can = ma_can
        self.dia_chi = dia_chi
        self.roa1 = roa1
        self.roa2 = roa2
        self.roa3 = roa3
        self.roa4 = roa4
        self.roa5 = roa5
        self.roa6 = roa6
        self.roa7 = roa7
        self.roa8 = roa8
    def __repr__(self):
        return str([self.ten_du_an, self.ten_toa_duong_day_khu, self.ten_tang_loai_nha, self.ma_can, self.dia_chi, self.roa1, self.roa2, self.roa3, self.roa4, self.roa5, self.roa6, self.roa7, self.roa8])

# ROA BIET THU
class ROA_biet_thu(db.Model):
    __tablename__ = "roa_biet_thu"
    ten_du_an = db.Column('ten_du_an', String, primary_key = True, nullable = False)
    ten_duong = db.Column('ten_duong', String, primary_key = True, nullable = False)
    ten_tang = db.Column('ten_tang', String, primary_key = True, nullable = False)
    ma_can = db.Column('ma_can', String, primary_key = True, nullable = False)
    dia_chi = db.Column('dia_chi', String, primary_key = True, nullable = False)
    roa1 = db.Column('roa1', String, primary_key = True, nullable = True)
    roa2 = db.Column('roa2', String, primary_key = True, nullable = True)
    roa3 = db.Column('roa3', String, primary_key = True, nullable = True)
    roa4 = db.Column('roa4', String, primary_key = True, nullable = True)
    roa5 = db.Column('roa5', String, primary_key = True, nullable = True)
    roa6 = db.Column('roa6', String, primary_key = True, nullable = True)
    roa7 = db.Column('roa7', String, primary_key = True, nullable = True)
    roa8 = db.Column('roa8', String, primary_key = True, nullable = True)
    def __init__(self, ten_du_an, ten_duong, ten_tang, ma_can, dia_chi, roa1, roa2, roa3, roa4, roa5, roa6, roa7, roa8):
        self.ten_du_an = ten_du_an
        self.ten_duong = ten_duong
        self.ten_tang = ten_tang
        self.ma_can = ma_can
        self.dia_chi = dia_chi
        self.roa1 = roa1
        self.roa2 = roa2
        self.roa3 = roa3
        self.roa4 = roa4
        self.roa5 = roa5
        self.roa6 = roa6
        self.roa7 = roa7
        self.roa8 = roa8
    def __repr__(self):
        return str([self.ten_du_an, self.ten_duong, self.ten_tang, self.ma_can, self.dia_chi, self.roa1, self.roa2, self.roa3, self.roa4, self.roa5, self.roa6, self.roa7, self.roa8])

# db.create_all()