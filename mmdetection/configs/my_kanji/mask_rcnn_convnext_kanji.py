# 継承するベースとなる設定ファイル
_base_ = '../convnext/mask-rcnn_convnext-t-p4-w7_fpn_amp-ms-crop-3x_coco.py'

# あなたのカスタム設定（これらの設定がベースの設定を上書きします）
dataset_type = 'COCODataset'
classes = ('kanji',)

data_root = 'data/kanji/'

data = dict(
    train=dict(
        type=dataset_type,
        classes=classes,
        ann_file=data_root + 'train/output.json',
        img_prefix=data_root + 'train/images/'),
    val=dict(
        type=dataset_type,
        classes=classes,
        ann_file=data_root + 'val/output.json',
        img_prefix=data_root + 'val/images/'),
    test=dict(
        type=dataset_type,
        classes=classes,
        ann_file=data_root + 'val/output.json',
        img_prefix=data_root + 'val/images/')
)

# 継承したモデルのクラス数部分を上書き
model = dict(
    roi_head=dict(
        bbox_head=dict(num_classes=1),
        mask_head=dict(num_classes=1)
    )
)