
import qrcode

tglogin_name = "tguserlogin.jpg"
def creat_qr(text):
    '''实例化QRCode生成qr对象'''
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.clear()
    # 传入数据
    qr.add_data(text)
    qr.make(fit=True)
    # 生成二维码
    img = qr.make_image()
    # 保存二维码
    img.save(tglogin_name)