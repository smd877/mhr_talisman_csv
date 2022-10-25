"""OpenCVを使ってMHRのお守りを確認するツール."""
import cv2
import numpy
import const
from datetime import datetime


def get_capture(device_target):
    """OpenCVの初期化."""
    # コンストラクタ 引数に数値を入れたらデバイスID、パスを入れたら動画/画像。
    if device_target is None:
        device_target = const.DEVICE_TARGET
    cap = cv2.VideoCapture(device_target)
    # パラメータ設定 フレームの幅と高さを指定する。(デフォルトはフルHDにする)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, const.CAP_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, const.CAP_HEIGHT)
    return cap


def trim_img(img, points):
    """画像をトリミング＆グレースケール＆二値化する."""
    # トリミング用画像 元画像の [高さ上部位置: 高さ下部位置, 幅左位置: 幅右位置]
    trim_img = img[points[1]: points[1] + points[3], points[0]: points[0] + points[2]]
    # トリミングした画像をグレースケールする
    gray_img = cv2.cvtColor(trim_img, cv2.COLOR_BGR2GRAY)
    # グレースケールした画像を二値化する
    ret, thresh_img = cv2.threshold(gray_img, 165, 255, cv2.THRESH_BINARY)
    return thresh_img


def get_templates():
    """判定用のテンプレート画像を取得する."""
    templates = {}
    img = read_image("tmpl_skill_names.png")
    templates['names'] = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = read_image("tmpl_skill_lvs.png")
    templates['lvs'] = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = read_image("tmpl_slots.png")
    templates['slots'] = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return templates


def collect_images(img):
    """判定用の画像を収集する."""
    imgs = {}
    # 各種必要な画像をトリミングして確保する
    imgs['skill1_name'] = trim_img(img, const.POINTS_SKILL1_NAME)
    imgs['skill1_lv'] = trim_img(img, const.POINTS_SKILL1_LV)
    imgs['skill2_name'] = trim_img(img, const.POINTS_SKILL2_NAME)
    imgs['skill2_lv'] = trim_img(img, const.POINTS_SKILL2_LV)
    imgs['slot1'] = trim_img(img, const.POINTS_SLOT_1)
    imgs['slot2'] = trim_img(img, const.POINTS_SLOT_2)
    imgs['slot3'] = trim_img(img, const.POINTS_SLOT_3)
    return imgs


def get_result(templates, imgs):
    """アイテムのデータ判定を行う."""
    # skill1
    str_skill1_name = judge_skill_name(get_maxLoc(imgs['skill1_name'], templates['names']))
    str_skill1_lv = judge_skill_lv(get_maxLoc(imgs['skill1_lv'], templates['lvs']))
    # skill2
    str_skill2_name = judge_skill_name(get_maxLoc(imgs['skill2_name'], templates['names']))
    str_skill2_lv = judge_skill_lv(get_maxLoc(imgs['skill2_lv'], templates['lvs']))
    # skill2のレベルが0ならスキル名は空
    if str_skill2_lv == '0':
        str_skill2_name = ''
    # slot
    str_slot1 = judge_slot(get_maxLoc(imgs['slot1'], templates['slots']))
    str_slot2 = judge_slot(get_maxLoc(imgs['slot2'], templates['slots']))
    str_slot3 = judge_slot(get_maxLoc(imgs['slot3'], templates['slots']))
    # 結果をカンマ区切りで出力する
    ret = []
    ret.append(str_skill1_name)
    ret.append(str_skill1_lv)
    ret.append(str_skill2_name)
    ret.append(str_skill2_lv)
    ret.append(str_slot1)
    ret.append(str_slot2)
    ret.append(str_slot3)
    return ','.join(ret)


def get_maxLoc(target, template):
    """物体検出した位置を返却."""
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    return maxLoc


def judge_slot(loc):
    """判定 スロット."""
    ret_x = (loc[0] // 40) - 1
    if ret_x == -1:
        return ''
    else:
        return str(ret_x)


def judge_skill_lv(loc):
    """判定 スキルレベル."""
    ret_y = loc[1] // 25
    return str(ret_y)


def judge_skill_name(loc):
    """判定 スキル名."""
    ret_x = loc[0] // 250
    ret_y = loc[1] // 38
    return const.SKILL_NAMES[ret_x][ret_y]


def scale_adjust(img):
    """画像サイズの調整."""
    # 倍率が違う場合はベースに合うよう拡大縮小する
    if img is None:
        # Noneの場合は判定出来ないのでそのまま返却
        return img
    if img.shape[0] == const.BASE_HEIGHT:
        # 高さが同じなので入力の画像をそのまま返却
        return img
    scale = const.BASE_HEIGHT / img.shape[0]
    return cv2.resize(img, (int(scale * img.shape[1]), int(scale * img.shape[0])))


def check_loop(device_target=None):
    """確認処理."""
    # テンプレートを取得
    templates = get_templates()
    # キャプチャオブジェクト取得
    cap = get_capture(device_target)
    # 重複確認用 スキルが重複していたら出力しない
    skill_list = []
    # 前回解析結果
    last_ret = ''
    # 重複回数
    same_time = 0
    # ループ処理
    while True:
        # readにより取得結果とフレーム画像を取得
        ret, frame = cap.read()
        if not ret:
            # False なら処理中断
            break
        img = scale_adjust(frame)
        imgs = collect_images(img)
        ret = get_result(templates, imgs)
        if ret not in skill_list:
            print(ret)
            skill_list.append(ret)
            same_time = 0
        if ret == last_ret:
            same_time += 1
        if same_time > 100:
            break
        last_ret = ret
    print('終了')


def read_image(path):
    """画像を読み込む."""
    return cv2.imread(path)


def write_image(path, img):
    """画像を保存する."""
    cv2.imwrite(path, img)


def write_image_burst(cap, points, times):
    """times回数分連続で画像キャプチャする."""
    for _ in range(times):
        ret, frame = cap.read()
        if not ret:
            break
        str_now = datetime.now().strftime('%H_%M_%S_%f')[:-3]
        img = trim_img(frame, points)
        write_image(const.PATH_TEMPORARY.format(str_now), img)


def create_blank_image(path, width, height):
    """黒色の画像を作成する."""
    img = numpy.zeros((height, width))
    write_image(path, img)


def concat_images(targets, output_path, is_vertical=True):
    """スキル名の一覧画像を作成する."""
    target_list = []
    # 対象画像達を読み込んでいく
    for input_path in targets:
        target_list.append(read_image(input_path))
    # 読み込んだ画像達を連結する is_vertical Trueは縦並び Falseは横並び
    concat_img = cv2.vconcat(target_list) if is_vertical else cv2.hconcat(target_list)
    write_image(output_path, concat_img)


def add_mark(img, points):
    """画像に矩形を書き込む."""
    cv2.rectangle(img, (points[0], points[1]), (points[0] + points[2], points[1] + points[3]), (0, 255, 0))


def add_marks(img):
    """画像に矩形を書き込む(判定箇所全部)."""
    add_mark(img, const.POINTS_SKILL1_NAME)
    add_mark(img, const.POINTS_SKILL2_NAME)
    add_mark(img, const.POINTS_SKILL1_LV)
    add_mark(img, const.POINTS_SKILL2_LV)
    add_mark(img, const.POINTS_SLOT_1)
    add_mark(img, const.POINTS_SLOT_2)
    add_mark(img, const.POINTS_SLOT_3)
